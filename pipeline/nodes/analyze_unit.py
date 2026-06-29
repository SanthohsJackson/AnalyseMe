"""
analyze_unit node: receives a single unit descriptor (via Send fan-out),
reads the file, extracts structure with tree-sitter, then calls LLM for
intent/semantic analysis.
"""

import json
import os
import threading
import traceback

from state_schema import UnitAnalysis, UnitAnalysisResult

from pipeline.parsers.tree_sitter_parser import parse_file
from pipeline.prompts.prompts import ANALYZE_UNIT_PROMPT
from pipeline.llm import call_llm_structured

# ---- Concurrency semaphore: bound parallel LLM calls so the fan-out doesn't
# overwhelm Ollama at medium/large scale. Sized from max_parallelism, created
# once per process and reused across the run (and the refinement loop). ----
_SEM_LOCK = threading.Lock()
_SEM_STATE: dict = {"sem": None, "size": None}


def _get_semaphore(size: int) -> threading.BoundedSemaphore:
    size = max(1, int(size or 1))
    with _SEM_LOCK:
        if _SEM_STATE["sem"] is None or _SEM_STATE["size"] != size:
            _SEM_STATE["sem"] = threading.BoundedSemaphore(size)
            _SEM_STATE["size"] = size
        return _SEM_STATE["sem"]


def _elide(source_bytes: bytes, ranges: list) -> str:
    """Return the file with the given byte ranges replaced by a marker."""
    parts, pos = [], 0
    for s, e in sorted(ranges):
        parts.append(source_bytes[pos:s].decode("utf-8", errors="replace"))
        parts.append("\n/* ... (class body analysed as a separate unit) ... */\n")
        pos = e
    parts.append(source_bytes[pos:].decode("utf-8", errors="replace"))
    return "".join(parts)


def _select_source(state: dict) -> tuple[str, str]:
    """Return (snippet, focus_note) for this unit based on its kind."""
    full_path = os.path.join(state.get("repo_path", ""), state.get("path", ""))
    with open(full_path, "rb") as f:
        source_bytes = f.read()

    kind = state.get("unit_kind", "file")
    if kind == "class":
        snippet = source_bytes[state["slice_start"]:state["slice_end"]].decode("utf-8", errors="replace")
        note = (
            f"\n\nSCOPE: This unit is ONE class extracted from a larger file: "
            f"'{state.get('class_name')}'. Document ONLY this class and its members; ignore anything "
            f"outside it. The structure above describes the whole file, so it may list siblings that are "
            f"NOT part of this unit — do not document those."
        )
        return snippet[:16000], note
    if kind == "module":
        snippet = _elide(source_bytes, state.get("elide", []))
        note = (
            "\n\nSCOPE: This unit is the MODULE-LEVEL view of a large file (class bodies elided and "
            "analysed separately — the elision markers show where). Document only top-level/module "
            "declarations: imports, module-level functions, constants, and configuration. Do NOT "
            "document the elided class members; they are covered by their own units."
        )
        return snippet[:16000], note
    # whole file
    return source_bytes.decode("utf-8", errors="replace")[:8000], ""


def analyze_unit(state: dict) -> dict:
    """
    state here is a unit descriptor dict (not full PipelineState).
    Keys: unit_id, path, language, repo_path, unit_kind, max_parallelism, ...
    Returns: {"unit_analyses": [UnitAnalysis], "map_errors": []}
    """
    unit_id = state.get("unit_id", "unknown")
    rel_path = state.get("path", "")
    language = state.get("language", "unknown")
    repo_path = state.get("repo_path", "")
    questions = state.get("questions", [])  # gaps from a previous completeness pass
    # Internal deps resolved deterministically at ingest (imports -> repo files);
    # we trust these over anything the model guesses.
    internal_deps = state.get("internal_deps", [])

    full_path = os.path.join(repo_path, rel_path)

    try:
        # Deterministic structure extraction (whole file)
        structure = parse_file(full_path)

        # Source slice depends on unit kind (whole file / single class / module-level)
        source_snippet, focus_note = _select_source(state)

        prompt = ANALYZE_UNIT_PROMPT.format(
            path=unit_id,
            language=language,
            structure=json.dumps(structure, indent=2),
            source=source_snippet,
        ) + focus_note

        if questions:
            prompt += (
                "\n\nREFINEMENT PASS: A previous analysis of this same unit left the gaps below. Produce a "
                "COMPLETE analysis again (the full JSON object), keeping everything already captured and "
                "additionally resolving each gap. Answer only from the source above — if the code does not "
                "support an answer, say so in the relevant field rather than inventing one. Gaps:\n"
                + "\n".join(f"- {q}" for q in questions)
            )

        # Bound concurrent LLM calls. Structured output validates the response
        # against UnitAnalysisResult and drops any keys the model invented.
        sem = _get_semaphore(state.get("max_parallelism", 8))
        with sem:
            result: UnitAnalysisResult = call_llm_structured(prompt, UnitAnalysisResult)

        unit_analysis = UnitAnalysis(
            unit_id=unit_id,
            path=rel_path,
            language=language,
            purpose=result.purpose,
            interfaces=result.interfaces,
            internal_deps=internal_deps,        # deterministic, not the model's guess
            external_deps=result.external_deps,
            idioms=result.idioms,
            behavioral_notes=result.behavioral_notes,
        )

        return {"unit_analyses": [unit_analysis], "map_errors": []}

    except Exception as exc:
        error_str = f"[{unit_id}] {type(exc).__name__}: {exc}\n{traceback.format_exc()}"
        return {"unit_analyses": [], "map_errors": [error_str]}
