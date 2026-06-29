"""
assemble_document node: renders the final reimplementation spec document
from all collected analysis data.
"""

import json
from collections import defaultdict

from state_schema import PipelineState

from pipeline.prompts.prompts import ASSEMBLE_PROMPT
from pipeline.llm import call_llm_text


def _build_inventory(state: PipelineState) -> str:
    files = state.get("files", [])
    languages = state.get("languages_detected", [])
    entry_points = state.get("entry_points", [])
    dep_manifest = state.get("dependency_manifest", {})

    # Group SOURCE files by language; non-source files are summarised, not dumped
    # (listing hundreds of configs/docs adds noise and isn't part of the spec).
    by_lang: dict[str, list[str]] = defaultdict(list)
    non_source = 0
    for fm in files:
        if fm.language:
            by_lang[fm.language].append(fm.path)
        else:
            non_source += 1

    lines = []
    lines.append(f"Languages detected: {', '.join(languages) or 'none'}")
    lines.append(f"Total files: {len(files)} ({non_source} non-source)")
    lines.append("")

    for lang, paths in sorted(by_lang.items()):
        lines.append(f"## {lang} ({len(paths)} files)")
        for p in sorted(paths)[:20]:  # Cap display to 20 per language
            lines.append(f"  - {p}")
        if len(paths) > 20:
            lines.append(f"  ... and {len(paths) - 20} more")
        lines.append("")

    if entry_points:
        lines.append("Entry points:")
        for ep in entry_points:
            lines.append(f"  - {ep}")
        lines.append("")

    if dep_manifest:
        lines.append("Dependency manifests:")
        for manifest_path, manifest_data in dep_manifest.items():
            lines.append(f"  {manifest_path} ({manifest_data.get('type', 'unknown')}):")
            deps = manifest_data.get("dependencies", [])
            for dep in deps[:10]:
                lines.append(f"    - {dep}")
            if len(deps) > 10:
                lines.append(f"    ... and {len(deps) - 10} more")
        lines.append("")

    # Internal module dependencies — resolved deterministically from imports.
    module_summaries = state.get("module_summaries", [])
    edges = [(m.name, m.collaborators) for m in module_summaries if m.collaborators]
    if edges:
        lines.append("Module dependencies (resolved from imports):")
        for name, collabs in sorted(edges):
            lines.append(f"  - {name} → {', '.join(collabs)}")
        lines.append("")

    # External package dependencies — third-party packages only (stdlib excluded).
    from pipeline.nodes.ingest import is_third_party
    external: set[str] = set()
    for ua in state.get("unit_analyses", []):
        external.update(d for d in ua.external_deps if is_third_party(d))
    for manifest_data in dep_manifest.values():
        external.update(d for d in manifest_data.get("dependencies", []) if is_third_party(d))
    if external:
        lines.append("External package dependencies:")
        for dep in sorted(external)[:40]:
            lines.append(f"  - {dep}")
        lines.append("")

    return "\n".join(lines)


def _build_interface_reference(state: PipelineState) -> str:
    """Complete, deterministic per-interface documentation (ground truth).

    Every public interface is documented here with its intent, inputs, outputs,
    and errors — so coverage doesn't depend on the LLM (or RAG trimming) echoing
    each one back in prose. This is what guarantees every interface is documented.
    """
    units = [ua for ua in state.get("unit_analyses", []) if ua.interfaces]
    if not units:
        return ""
    lines = [
        "## Interface Reference",
        "",
        "_Complete per-interface documentation extracted from the source (ground truth)._",
        "",
    ]
    for ua in sorted(units, key=lambda u: u.path):
        lines.append(f"### `{ua.path}`")
        for i in ua.interfaces:
            sig = f" — `{i.signature}`" if i.signature else ""
            lines.append(f"- **{i.name}** ({i.kind}){sig}")
            if i.intent:
                lines.append(f"  - Intent: {i.intent}")
            if i.inputs:
                lines.append(f"  - Inputs: {', '.join(i.inputs)}")
            if i.outputs:
                lines.append(f"  - Outputs: {', '.join(i.outputs)}")
            if i.raises:
                lines.append(f"  - Raises: {', '.join(i.raises)}")
            if i.side_effects:
                lines.append(f"  - Side effects: {', '.join(i.side_effects)}")
        lines.append("")
    return "\n".join(lines)


def _insert_diagram(doc: str, diagram: str) -> str:
    """Insert the Mermaid diagram into the assembled doc deterministically.

    The diagram is grounded and syntax-sensitive, so we splice it in ourselves
    rather than asking the LLM to reproduce it. Placed right after the first
    'Architecture' heading; appended as its own section if none is found.
    """
    if not diagram:
        return doc
    block = f"\n### Architecture Diagram\n\n{diagram}\n"
    lines = doc.splitlines()
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("#") and "architecture" in line.lower() and "diagram" not in line.lower():
            lines.insert(i + 1, block)
            return "\n".join(lines)
    return doc.rstrip() + "\n\n## Architecture Diagram\n" + block


def assemble_document(state: PipelineState) -> dict:
    validation_gaps = state.get("validation_gaps", [])
    review_findings = state.get("review_findings", [])
    revision_count = state.get("revision_count", 0)

    guidance_parts = []
    if review_findings:
        guidance_parts.append(
            "CRITICAL — the previous draft contained unsupported claims / hallucinations. "
            "Remove or correct every one of these; do NOT invent classes, interfaces, return "
            "values, or architecture that the analysis does not contain:\n"
            + "\n".join(f"- {f}" for f in review_findings)
        )
    if validation_gaps:
        guidance_parts.append(
            "Address these coverage gaps from the previous review:\n"
            + "\n".join(f"- {gap}" for gap in validation_gaps)
        )
    gaps_guidance = "\n\n".join(guidance_parts)

    inventory = _build_inventory(state)

    from pipeline.rag import select_context

    module_summaries = state.get("module_summaries", [])
    modules_data = [
        {
            "name": m.name,
            "responsibility": m.responsibility,
            "public_surface": m.public_surface,
            "collaborators": m.collaborators,
        }
        for m in module_summaries
    ]
    modules_records = [
        {
            "id": m.module_id,
            "full": json.dumps(md, indent=2),
            "compact": f"{m.name}: {(m.responsibility or '')[:120]}",
        }
        for m, md in zip(module_summaries, modules_data)
    ]
    modules_ctx, _ = select_context(
        json.dumps(modules_data, indent=2), modules_records,
        query="module responsibilities, architecture, public interfaces, behavioral spec",
    )

    data_schemas = state.get("data_schemas", [])
    schemas_data = [
        {
            "name": s.name,
            "description": s.description,
            "json_schema": s.json_schema,
        }
        for s in data_schemas
    ]

    cross_cutting = state.get("cross_cutting")
    if cross_cutting:
        cc_data = {
            "error_handling": cross_cutting.error_handling,
            "config": cross_cutting.config,
            "logging": cross_cutting.logging,
            "auth": cross_cutting.auth,
            "concurrency": cross_cutting.concurrency,
            "external_integrations": cross_cutting.external_integrations,
        }
    else:
        cc_data = {}

    behavioral_tests = state.get("behavioral_tests", [])
    tests_data = [
        {
            "target_interface": t.target_interface,
            "given": t.given,
            "when": t.when,
            "then": t.then,
        }
        for t in behavioral_tests
    ]
    tests_records = [
        {
            "id": f"test_{i}",
            "full": json.dumps(td, indent=2),
            "compact": f"{td['target_interface']}: {td['given'][:60]}",
        }
        for i, td in enumerate(tests_data)
    ]
    tests_ctx, _ = select_context(
        json.dumps(tests_data, indent=2), tests_records,
        query="acceptance tests covering the main public interfaces and behaviors",
    )

    system_overview = state.get("system_overview", "")

    prompt = ASSEMBLE_PROMPT.format(
        prior_lessons=state.get("prior_lessons", ""),
        gaps_guidance=gaps_guidance,
        inventory=inventory,
        system_overview=system_overview,
        modules_json=modules_ctx,
        schemas_json=json.dumps(schemas_data, indent=2),
        cross_cutting_json=json.dumps(cc_data, indent=2),
        tests_json=tests_ctx,
    )

    doc_text = call_llm_text(prompt)
    doc_text = _insert_diagram(doc_text, state.get("architecture_diagram", ""))

    interface_reference = _build_interface_reference(state)
    if interface_reference:
        doc_text = doc_text.rstrip() + "\n\n" + interface_reference

    return {
        "draft_document": doc_text,
        "revision_count": revision_count + 1,
    }
