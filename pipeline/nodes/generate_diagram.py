"""
generate_diagram node: build Mermaid architecture diagrams from the analysis.

All diagrams are deterministic and grounded — no LLM is involved, so nothing can
be hallucinated:
  1. Module dependency graph — nodes are real modules, edges are resolved imports
     (FileMeta.depends_on -> module collaborators).
  2. External integrations — services the system talks to, from cross_cutting.
  3. Data model — the extracted data_schemas and the references between them.
"""

import os
import re

from state_schema import PipelineState
from pipeline.nodes.ingest import _STDLIB

# Keep the module graph readable: above this many modules we render the most-
# connected ones and note the truncation rather than emit an unreadable hairball.
MAX_NODES = 60


def _node_id(name: str) -> str:
    """A stable, Mermaid-safe node id for an arbitrary name."""
    safe = "".join(c if c.isalnum() else "_" for c in name)
    return f"m_{safe or 'x'}"


def _module_label(name: str) -> str:
    return "(root)" if name in (".", "") else name


def _clean_label(text: str, limit: int = 40) -> str:
    """Strip characters that break Mermaid labels and truncate."""
    out = text.replace('"', "'").replace("\n", " ").replace("|", "/").strip()
    return (out[:limit] + "…") if len(out) > limit else out


# ---------------------------------------------------------------------------
# 1. Module dependency graph
# ---------------------------------------------------------------------------

def _module_graph(modules, entry_points) -> str | None:
    if not modules:
        return None
    names = {m.name for m in modules}

    edges: set[tuple[str, str]] = set()
    for m in modules:
        for collab in m.collaborators:
            if collab in names and collab != m.name:
                edges.add((m.name, collab))

    # Rank by connectedness so truncation keeps the structurally important modules.
    degree: dict[str, int] = {m.name: 0 for m in modules}
    for src, dst in edges:
        degree[src] += 1
        degree[dst] += 1
    ranked = sorted(names, key=lambda n: (-degree.get(n, 0), n))
    truncated = len(ranked) > MAX_NODES
    keep = set(ranked[:MAX_NODES])
    edges = {(s, d) for (s, d) in edges if s in keep and d in keep}

    entry_dirs = {os.path.dirname(ep) or "." for ep in entry_points}

    lines = ["```mermaid", "graph LR"]
    for name in sorted(keep):
        lines.append(f'    {_node_id(name)}["{_module_label(name)}"]')
    for src, dst in sorted(edges):
        lines.append(f"    {_node_id(src)} --> {_node_id(dst)}")
    for name in sorted(keep & entry_dirs):
        lines.append(f"    style {_node_id(name)} fill:#cce5ff,stroke:#004085,stroke-width:2px")
    lines.append("```")

    note = "_Entry-point modules are highlighted. Edges are resolved imports between modules._"
    if truncated:
        note += f"\n\n_Showing the {MAX_NODES} most-connected of {len(names)} modules._"
    return "\n".join(lines) + "\n\n" + note


# ---------------------------------------------------------------------------
# 2. External integrations
# ---------------------------------------------------------------------------

def _lib_key(name: str) -> str:
    """Normalise a package/module/service name for library matching."""
    base = re.split(r"[<>=!~\[ .]", name.strip().strip(" '\""), 1)[0]
    return base.replace("-", "_").lower()


def _integrations_graph(cross_cutting, system_label: str, exclude: set[str]) -> str | None:
    integrations = getattr(cross_cutting, "external_integrations", None) or []
    if not integrations:
        return None

    sys_id = "sys_system"
    lines = ["```mermaid", "graph LR", f'    {sys_id}["{_clean_label(system_label, 30)}"]']
    seen: set[str] = set()
    for item in integrations:
        # Items follow "service: how it's used"; the part before ':' is the service.
        service, _, detail = str(item).partition(":")
        service = service.strip() or str(item).strip()
        # Safety net: skip entries that are actually libraries/stdlib, not services.
        if _lib_key(service) in exclude:
            continue
        sid = _node_id(service)
        if sid in seen:
            continue
        seen.add(sid)
        lines.append(f'    {sid}(["{_clean_label(service, 30)}"])')
        if detail.strip():
            lines.append(f'    {sys_id} -->|"{_clean_label(detail)}"| {sid}')
        else:
            lines.append(f"    {sys_id} --> {sid}")
    if not seen:  # everything was a library/stdlib — no real services to show
        return None
    for sid in seen:
        lines.append(f"    style {sid} fill:#fff3cd,stroke:#856404")
    lines.append("```")
    return "\n".join(lines) + "\n\n_External services the system integrates with (rounded nodes)._"


# ---------------------------------------------------------------------------
# 3. Data model (from extracted schemas)
# ---------------------------------------------------------------------------

def _member_name(name: str) -> str:
    return "".join(c if (c.isalnum() or c == "_") else "_" for c in str(name)) or "field"


def _field_type(prop) -> str:
    """Human-readable type for a JSON-schema property."""
    if not isinstance(prop, dict):
        return "any"
    if "$ref" in prop:
        return str(prop["$ref"]).split("/")[-1]
    t = prop.get("type", "any")
    if t == "array":
        items = prop.get("items", {})
        if isinstance(items, dict):
            if "$ref" in items:
                return str(items["$ref"]).split("/")[-1] + "[]"
            return f"{items.get('type', 'any')}[]"
        return "array"
    return str(t)


def _refs(prop) -> set[str]:
    """Schema names this property references (via $ref or a matching type)."""
    targets: set[str] = set()
    if not isinstance(prop, dict):
        return targets
    if "$ref" in prop:
        targets.add(str(prop["$ref"]).split("/")[-1])
    t = prop.get("type")
    if isinstance(t, str):
        targets.add(t)
    items = prop.get("items")
    if isinstance(items, dict):
        if "$ref" in items:
            targets.add(str(items["$ref"]).split("/")[-1])
        it = items.get("type")
        if isinstance(it, str):
            targets.add(it)
    return targets


def _data_model(data_schemas) -> str | None:
    if not data_schemas:
        return None

    # Map sanitized class id -> original name, and a lowercase lookup for ref matching.
    classes = {s.name: _member_name(s.name) for s in data_schemas if s.name}
    if not classes:
        return None
    by_lower = {name.lower(): name for name in classes}

    lines = ["```mermaid", "classDiagram"]
    relations: set[tuple[str, str, str]] = set()

    for s in data_schemas:
        if not s.name:
            continue
        cid = classes[s.name]
        props = (s.json_schema or {}).get("properties", {})
        if isinstance(props, dict) and props:
            lines.append(f"    class {cid} {{")
            for fname, prop in props.items():
                ftype = _field_type(prop)
                lines.append(f"        +{ftype} {_member_name(fname)}")
                # A field references another schema if that schema's name appears
                # as a token in its type (e.g. 'list[Interface]' -> Interface),
                # or via an explicit $ref/items.
                referenced = {str(t).lower() for t in _refs(prop)}
                referenced |= set(re.findall(r"[A-Za-z_][\w]*", ftype.lower()))
                for other_lower, other_name in by_lower.items():
                    if other_name != s.name and other_lower in referenced:
                        relations.add((cid, classes[other_name], _member_name(fname)))
            lines.append("    }")
        else:
            lines.append(f"    class {cid}")

    for src, dst, field in sorted(relations):
        lines.append(f"    {src} --> {dst} : {field}")
    lines.append("```")
    return "\n".join(lines) + "\n\n_Data entities from the extracted schemas; arrows show references between them._"


# ---------------------------------------------------------------------------

def generate_diagram(state: PipelineState) -> dict:
    repo_name = os.path.basename(str(state.get("repo_path", "")).rstrip("/")) or "System"

    sections: list[str] = []
    module_graph = _module_graph(state.get("module_summaries", []), state.get("entry_points", []))
    if module_graph:
        sections.append("#### Module Dependencies\n\n" + module_graph)

    # Libraries/stdlib must never appear as "services" in the integrations graph.
    exclude = set(_STDLIB)
    for manifest in state.get("dependency_manifest", {}).values():
        exclude.update(_lib_key(d) for d in manifest.get("dependencies", []))
    for ua in state.get("unit_analyses", []):
        exclude.update(_lib_key(d) for d in ua.external_deps)

    integrations = _integrations_graph(state.get("cross_cutting"), repo_name, exclude)
    if integrations:
        sections.append("#### External Integrations\n\n" + integrations)

    data_model = _data_model(state.get("data_schemas", []))
    if data_model:
        sections.append("#### Data Model\n\n" + data_model)

    return {"architecture_diagram": "\n\n".join(sections)}
