"""
review_consistency node: the anti-hallucination review agent.

Grounds the assembled draft against the deterministic analysis (the actual
classes, interfaces, and dependencies tree-sitter + the unit analyses found)
and flags any claim in the document that the ground truth does not support.
This catches the small local model inventing architecture that isn't there.
"""

import json
import re

from state_schema import FileKind, PipelineState

from pipeline.prompts.prompts import REVIEW_PROMPT
from pipeline.llm import call_llm_json

# File kinds whose paths the document may legitimately reference. Generated docs
# (DOC) and the pipeline's own output artifacts are excluded so they don't bloat
# ground truth, but real source/config/build files are all included.
_REFERENCEABLE_KINDS = {FileKind.SOURCE, FileKind.CONFIG, FileKind.BUILD}


def _build_ground_truth(state: PipelineState) -> str:
    """Assemble the verifiable facts the spec must stay consistent with.

    Must be COMPLETE: the reviewer flags anything not found here, so a missing
    real name or behavioural fact becomes a false "hallucination". We list every
    file, module, schema, external dep, the cross-cutting facts, and each
    interface WITH its intent/outputs/raises — so behavioural claims (tests,
    intents, error handling) are verifiable, not just names.
    """
    unit_analyses = state.get("unit_analyses", [])
    dep_manifest = state.get("dependency_manifest", {})
    files = state.get("files", [])

    interfaces = []
    for ua in unit_analyses:
        for iface in ua.interfaces:
            if not iface.name:
                continue
            interfaces.append({
                "id": f"{ua.path}::{iface.name} ({iface.kind})",
                "intent": iface.intent,
                "outputs": iface.outputs,
                "raises": iface.raises,
            })

    external = {
        dep for manifest in dep_manifest.values()
        for dep in manifest.get("dependencies", [])
    }
    for ua in unit_analyses:
        external.update(ua.external_deps)

    cc = state.get("cross_cutting")
    cross_cutting = {
        "error_handling": getattr(cc, "error_handling", ""),
        "logging": getattr(cc, "logging", ""),
        "concurrency": getattr(cc, "concurrency", ""),
        "auth": getattr(cc, "auth", ""),
        "config": getattr(cc, "config", ""),
        "external_integrations": getattr(cc, "external_integrations", []),
    } if cc else {}

    facts: dict = {
        "languages": state.get("languages_detected", []),
        "entry_points": state.get("entry_points", []),
        "file_count": len(files),
        # Every source/config/build file — referencing any of these is grounded.
        "all_files": sorted(fm.path for fm in files if fm.kind in _REFERENCEABLE_KINDS),
        "dependency_manifests": sorted(dep_manifest.keys()),
        "modules": [
            {"name": m.name, "responsibility": m.responsibility, "public_surface": m.public_surface}
            for m in state.get("module_summaries", [])
        ],
        "data_schemas": sorted({s.name for s in state.get("data_schemas", []) if s.name}),
        "cross_cutting": cross_cutting,
        "interfaces": interfaces,
        "external_dependencies": sorted(external),
    }
    return json.dumps(facts, indent=2)


# Phrases that mark a "finding" as a statement of absence — never a hallucination.
_ABSENCE_PHRASES = (
    "none specified", "not specified", "none provided", "no interfaces",
    "no side effects", "no errors", "no specific", "unspecified",
    "not detailed", "n/a", ": none", "are none", "none.",
)


def _dep_name(s: str) -> str:
    """Package name with any version specifier / extras stripped: 'langsmith>=0.1' -> 'langsmith'."""
    return re.split(r"[<>=!~\[\] (]", s.strip(" '\""), 1)[0].strip().lower()


def _norm(t: str) -> str:
    return t.strip().strip(".,;:'\"()`").lower()


def _is_symbol_like(t: str) -> bool:
    """True for tokens that look like code symbols (not plain English words):
    snake_case, CamelCase, dotted/slashed paths, or *.py files."""
    return "_" in t or "/" in t or t.endswith(".py") or bool(re.search(r"[a-z][A-Z]", t))


def _collect_known_symbols(state: PipelineState) -> set[str]:
    """Every real symbol/file/module name the document may reference (lowercased)."""
    known: set[str] = set()
    for ua in state.get("unit_analyses", []):
        p = ua.path.lower()
        base = p.rsplit("/", 1)[-1]
        known.update({p, base, base.rsplit(".", 1)[0]})
        for iface in ua.interfaces:
            if iface.name:
                known.add(iface.name.lower())
    for s in state.get("data_schemas", []):
        if s.name:
            known.add(s.name.lower())
    for m in state.get("module_summaries", []):
        name = m.name.lower()
        known.update({name, name.rsplit("/", 1)[-1]})
        for sym in m.public_surface:        # entries look like "add (function)"
            known.add(sym.split(" ", 1)[0].lower())
    return known


# Words that mark a quoted entity as an inventory statistic, not a real symbol.
_STAT_WORDS = ("file", "files", "line", "lines", "count", "non-source", "loc")

# A finding is an EXISTENCE claim (the only kind we deterministically override)
# when it asserts something simply isn't there. We never override relationship or
# behaviour claims — a capable reviewer is trusted for those.
_EXISTENCE_PHRASES = (
    "not present", "not in ground truth", "does not exist", "not found",
    "no such", "not listed", "absent from", "not part of",
)


def _entity_grounded(entity: str, known: set[str], known_deps: set[str]) -> bool:
    """True if a quoted "claimed-fake" entity is actually real (so flagging it is wrong)."""
    n = _norm(entity)
    if not n:
        return True
    # Inventory counts/stats: "10 non-source", "480 files", "Total Files: 414".
    if any(ch.isdigit() for ch in n) and any(w in n for w in _STAT_WORDS):
        return True
    if n[:1].isdigit():
        return True
    # Identifier-ish tokens in the entity (code symbols or package names).
    tokens = re.findall(r"[\w.\-/]+", entity)
    checkable = [t for t in tokens if _is_symbol_like(t) or _dep_name(t) in known_deps]
    if not checkable:
        return False  # pure prose — can't verify, leave it for review
    return all(_norm(t) in known or _dep_name(t) in known_deps for t in checkable)


def _filter_findings(findings: list[str], state: PipelineState) -> list[str]:
    """Drop findings that the ground truth provably contradicts.

    Small reviewer models emit false positives even when the fact is present —
    flagging a dependency that IS in the manifest, a stated absence, an inventory
    count, or a list of methods that ARE all real. This deterministic pass
    removes those so they don't trigger a pointless re-assembly revision.
    CONTRADICTION findings are never dropped (those are conflicts, not existence).
    """
    known_deps: set[str] = set()
    for manifest in state.get("dependency_manifest", {}).values():
        known_deps.update(_dep_name(d) for d in manifest.get("dependencies", []))
    for ua in state.get("unit_analyses", []):
        known_deps.update(_dep_name(d) for d in ua.external_deps)
    known = _collect_known_symbols(state)

    kept = []
    for f in findings:
        low = f.lower()
        # Never second-guess contradictions (wrong type/signature/behaviour).
        if low.lstrip().startswith("contradiction"):
            kept.append(f)
            continue
        # 1. statements of absence are not hallucinations
        if any(p in low for p in _ABSENCE_PHRASES):
            continue
        # Only override the reviewer on pure EXISTENCE claims. Relationship and
        # behaviour findings ("X calls Y", "X returns Z") are left for the model —
        # suppressing those by name-matching would hide real issues.
        if any(p in low for p in _EXISTENCE_PHRASES):
            # 2. quoted-entity rule: every entity quoted as "fake" is actually a
            #    real dependency, symbol, or an inventory count.
            quoted = re.findall(r"'([^']+)'", f) or re.findall(r'"([^"]+)"', f)
            if quoted and all(_entity_grounded(e, known, known_deps) for e in quoted):
                continue
            # 3. or every code-symbol it names is real (a genuine existence
            #    hallucination introduces an unknown name, which stays).
            symbols = [_norm(t) for t in re.findall(r"[\w./\-]+", f) if _is_symbol_like(t)]
            symbols = [t for t in symbols if t]
            if symbols and all(t in known for t in symbols):
                continue
        kept.append(f)
    return kept


def _strip_deterministic(doc: str) -> str:
    """Remove content that is generated deterministically from ground truth, so
    the reviewer fact-checks only the model's prose. Mermaid diagrams and the
    appended Interface Index are grounded by construction and must not be flagged.
    """
    doc = re.sub(r"```mermaid.*?```", "[architecture diagram — generated, omitted]", doc, flags=re.DOTALL)
    doc = re.split(r"\n#{1,3}\s+Interface (Index|Reference)", doc)[0]
    return doc


def review_consistency(state: PipelineState) -> dict:
    draft_document = state.get("draft_document", "")
    unit_analyses = state.get("unit_analyses", [])

    # Nothing to ground against — can't meaningfully review, pass with a note.
    if not unit_analyses:
        return {
            "review_passed": True,
            "review_findings": [
                "Review skipped: no unit analyses available to ground the document."
            ],
        }

    ground_truth = _build_ground_truth(state)
    reviewable = _strip_deterministic(draft_document)

    # Ground truth must NOT be truncated — a cut-off list makes the reviewer flag
    # real names as hallucinations. gemma-class models have large contexts, so we
    # allow a generous budget and only guard against a pathological repo.
    prompt = REVIEW_PROMPT.format(
        ground_truth=ground_truth[:60000],
        document=reviewable[:16000],
    )

    try:
        raw = call_llm_json(prompt)
        findings = raw.get("findings", []) or []
    except Exception as exc:
        # If the reviewer itself fails, don't block the pipeline — surface it.
        return {
            "review_passed": True,
            "review_findings": [f"Review agent LLM call failed: {exc}"],
        }

    # Drop findings the ground truth provably contradicts (small-model noise).
    findings = _filter_findings(findings, state)

    # The document is grounded iff no real findings remain.
    return {
        "review_passed": not findings,
        "review_findings": findings,
    }
