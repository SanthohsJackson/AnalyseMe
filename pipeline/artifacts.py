"""
Render pipeline outputs to human-readable Markdown.

Used by the CLI to (a) persist a per-stage doc and a per-class spec to disk,
and (b) show them in the interactive viewer. Pure functions, no I/O here
except the small `write_text` helper.
"""

from __future__ import annotations

import json
from pathlib import Path


# ---------------------------------------------------------------------------
# Per-class (per-unit) spec
# ---------------------------------------------------------------------------

def render_class_spec(ua) -> str:
    """Render a single UnitAnalysis into a Markdown spec for that class/file."""
    lines: list[str] = []
    lines.append(f"# {ua.unit_id}")
    lines.append("")
    lines.append(f"**File:** {ua.path}  ")
    lines.append(f"**Language:** {ua.language}")
    lines.append("")
    lines.append("## Purpose")
    lines.append(ua.purpose or "_(none extracted)_")
    lines.append("")

    if ua.interfaces:
        lines.append("## Interfaces")
        for iface in ua.interfaces:
            lines.append(f"### `{iface.name}` ({iface.kind})")
            if iface.signature:
                lines.append(f"```\n{iface.signature}\n```")
            lines.append(f"**Intent:** {iface.intent or '—'}")
            lines.append("")
            if iface.inputs:
                lines.append("**Inputs:**")
                lines.extend(f"- {x}" for x in iface.inputs)
            if iface.outputs:
                lines.append("**Outputs:**")
                lines.extend(f"- {x}" for x in iface.outputs)
            if iface.raises:
                lines.append("**Raises:**")
                lines.extend(f"- {x}" for x in iface.raises)
            if iface.side_effects:
                lines.append("**Side effects:**")
                lines.extend(f"- {x}" for x in iface.side_effects)
            lines.append("")

    if ua.internal_deps:
        lines.append("## Internal dependencies")
        lines.extend(f"- {d}" for d in ua.internal_deps)
        lines.append("")
    if ua.external_deps:
        lines.append("## External dependencies")
        lines.extend(f"- {d}" for d in ua.external_deps)
        lines.append("")
    if ua.idioms:
        lines.append("## Flagged idioms")
        lines.extend(f"- {d}" for d in ua.idioms)
        lines.append("")
    if ua.behavioral_notes:
        lines.append("## Behavioral notes")
        lines.extend(f"- {d}" for d in ua.behavioral_notes)
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Per-stage docs
# ---------------------------------------------------------------------------

def render_stage_doc(node_id: str, update: dict) -> str | None:
    """Render a Markdown doc for a completed stage from its state update.

    Returns None when there is nothing meaningful to render for this update.
    """
    if not isinstance(update, dict):
        return None

    if node_id == "ingest":
        files = update.get("files", [])
        langs = update.get("languages_detected", [])
        eps = update.get("entry_points", [])
        deps = update.get("dependency_manifest", {})
        lines = ["# Stage: Ingestion", "",
                 f"**Files found:** {len(files)}  ",
                 f"**Languages:** {', '.join(langs) or 'none'}", ""]
        if eps:
            lines += ["## Entry points", *[f"- {e}" for e in eps], ""]
        if deps:
            lines.append("## Dependency manifests")
            for path, data in deps.items():
                d = data.get("dependencies", [])
                lines.append(f"- **{path}** ({data.get('type', '?')}): {len(d)} deps")
            lines.append("")
        lines.append("## Files")
        for f in files:
            lines.append(f"- `{f.path}` — {f.kind.value}{' / ' + f.language if f.language else ''}")
        return "\n".join(lines)

    if node_id == "route_units":
        units = update.get("units_to_analyze", [])
        lines = ["# Stage: Routing", "", f"**Units queued for analysis:** {len(units)}", ""]
        for u in units:
            flag = " (large)" if u.get("large_file") else ""
            lines.append(f"- `{u.get('path')}` [{u.get('language')}]{flag}")
        return "\n".join(lines)

    if node_id == "reduce_modules":
        mods = update.get("module_summaries", [])
        lines = ["# Stage: Module Reduction", "", f"**Modules:** {len(mods)}", ""]
        for m in mods:
            lines.append(f"## {m.name}")
            lines.append(m.responsibility or "")
            if m.public_surface:
                lines.append("**Public surface:** " + ", ".join(m.public_surface))
            if m.collaborators:
                lines.append("**Collaborators:** " + ", ".join(m.collaborators))
            lines.append("")
        return "\n".join(lines)

    if node_id == "review_completeness":
        questions = update.get("analysis_questions", {}) or {}
        complete = update.get("analysis_complete")
        ap = update.get("analysis_pass", 0)
        lines = ["# Stage: Completeness Review", "",
                 f"**Pass:** {ap}  ",
                 f"**Result:** {'COMPLETE ✓' if complete else 'GAPS — refining'}", ""]
        if questions:
            lines.append("## Questions for the next analysis pass")
            for uid, qs in questions.items():
                lines.append(f"### {uid}")
                lines.extend(f"- {q}" for q in qs)
                lines.append("")
        else:
            lines.append("_All units fully captured; no further passes needed._")
        return "\n".join(lines)

    if node_id == "synthesize_system":
        overview = update.get("system_overview", "")
        return f"# Stage: System Synthesis\n\n{overview}" if overview else None

    if node_id == "extract_architecture":
        schemas = update.get("data_schemas", [])
        cc = update.get("cross_cutting")
        lines = ["# Stage: Architecture", "", "## Data schemas"]
        for s in schemas:
            lines.append(f"### {s.name}")
            lines.append(s.description or "")
            if s.json_schema:
                lines.append("```json")
                lines.append(json.dumps(s.json_schema, indent=2))
                lines.append("```")
            lines.append("")
        if cc is not None:
            lines.append("## Cross-cutting concerns")
            for field in ("error_handling", "config", "logging", "auth", "concurrency"):
                val = getattr(cc, field, "")
                if val:
                    lines.append(f"- **{field}:** {val}")
            if cc.external_integrations:
                lines.append("- **external_integrations:** " + ", ".join(cc.external_integrations))
        return "\n".join(lines)

    if node_id == "generate_tests":
        tests = update.get("behavioral_tests", [])
        lines = ["# Stage: Test Generation", "", f"**Acceptance tests:** {len(tests)}", ""]
        for t in tests:
            lines.append(f"### {t.target_interface}")
            lines.append(f"- **Given:** {t.given}")
            lines.append(f"- **When:** {t.when}")
            lines.append(f"- **Then:** {t.then}")
            lines.append("")
        return "\n".join(lines)

    if node_id == "generate_diagram":
        diagram = update.get("architecture_diagram", "")
        return f"# Stage: Architecture Diagram\n\n{diagram}" if diagram else None

    if node_id == "assemble_document":
        draft = update.get("draft_document", "")
        return f"# Stage: Assembly (draft)\n\n{draft}" if draft else None

    if node_id == "review_consistency":
        findings = update.get("review_findings", [])
        passed = update.get("review_passed")
        lines = ["# Stage: Consistency Review (anti-hallucination)", "",
                 f"**Result:** {'PASSED ✓' if passed else 'FINDINGS ✗'}", ""]
        if findings:
            lines.append("## Findings")
            lines.extend(f"- {f}" for f in findings)
        else:
            lines.append("_No inconsistencies found — the document is grounded in the analysis._")
        return "\n".join(lines)

    if node_id == "validate":
        passed = update.get("validation_passed")
        gaps = update.get("validation_gaps", [])
        lines = ["# Stage: Validation (coverage critic)", "",
                 f"**Result:** {'PASSED ✓' if passed else 'GAPS ✗'}", ""]
        if gaps:
            lines.append("## Coverage gaps")
            lines.extend(f"- {g}" for g in gaps)
        return "\n".join(lines)

    return None


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
