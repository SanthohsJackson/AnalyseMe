"""
Route units node: create unit descriptors for fan-out analysis.
Populates units_to_analyze in state so conditional edges can emit Send().

Large files are split into one unit per top-level class (plus a module-level
unit for the top-level/non-class code) so their content is never truncated.
"""

import os

from state_schema import FileKind, PipelineState
from pipeline.parsers.tree_sitter_parser import extract_class_spans

LOC_LARGE_THRESHOLD = 500


def _file_units(file_meta, repo_path: str, max_parallelism: int) -> list[dict]:
    """Return one or more unit descriptors for a single source file."""
    path = file_meta.path
    base = {
        "path": path,
        "language": file_meta.language,
        "repo_path": repo_path,
        "max_parallelism": max_parallelism,
        # Deterministic internal deps (resolved at ingest); all units of a split
        # file share the file's resolved dependencies.
        "internal_deps": file_meta.depends_on,
    }

    # Small file → a single whole-file unit (unchanged behaviour)
    if file_meta.loc <= LOC_LARGE_THRESHOLD:
        return [{**base, "unit_id": path, "unit_kind": "file", "large_file": False}]

    # Large file → try to split into per-class units
    spans = extract_class_spans(os.path.join(repo_path, path))
    if not spans:
        # No detectable classes (e.g. a big functional file) → whole file
        return [{**base, "unit_id": path, "unit_kind": "file", "large_file": True}]

    units: list[dict] = []
    for s in spans:
        units.append({
            **base,
            "unit_id": f"{path}::{s['name']}",
            "unit_kind": "class",
            "class_name": s["name"],
            "slice_start": s["start_byte"],
            "slice_end": s["end_byte"],
            "large_file": True,
        })
    # Module-level unit: the file with class bodies elided (imports + top-level code)
    units.append({
        **base,
        "unit_id": f"{path}::<module>",
        "unit_kind": "module",
        "elide": [[s["start_byte"], s["end_byte"]] for s in spans],
        "large_file": True,
    })
    return units


def route_units(state: PipelineState) -> dict:
    files = state.get("files", [])
    repo_path = state["repo_path"]
    skip_tests = state.get("skip_tests", True)
    max_parallelism = int(state.get("max_parallelism", 8) or 8)
    max_files = state.get("max_files", None)
    if max_files is not None:
        max_files = int(max_files)  # guard against accidental string from CLI

    # Pick eligible source files, smallest first (faster early feedback)
    eligible = [
        fm for fm in files
        if fm.kind == FileKind.SOURCE and fm.language is not None
        and not (skip_tests and fm.kind == FileKind.TEST)
    ]
    eligible.sort(key=lambda fm: fm.loc)

    if max_files:
        eligible = eligible[:max_files]

    units: list[dict] = []
    for fm in eligible:
        units.extend(_file_units(fm, repo_path, max_parallelism))

    split = sum(1 for u in units if u.get("unit_kind") in ("class", "module"))
    print(f"[route_units] {len(units)} units queued ({len(eligible)} files, {split} from large-file splits)")
    return {"units_to_analyze": units}
