"""
review_completeness node: the data-completeness reviewer.

After the map step, this checks whether each unit's analysis actually captured
everything in the code. It combines:
  1. Deterministic structural gaps — tree-sitter finds the real functions/classes
     in each file; any that weren't captured as interfaces become questions.
  2. An LLM qualitative review — flags empty intents, vague purposes, missing
     side-effects, and frames them as questions for the next pass.

The questions are fed back to analyze_unit on the next refinement pass. The
number of passes is bounded by `max_analysis_passes`.
"""

import json
import os

from state_schema import PipelineState

from pipeline.parsers.tree_sitter_parser import parse_file
from pipeline.prompts.prompts import REVIEW_COMPLETENESS_PROMPT
from pipeline.llm import call_llm_json


def review_completeness(state: PipelineState) -> dict:
    unit_analyses = state.get("unit_analyses", [])
    repo_path = state.get("repo_path", "")
    analysis_pass = state.get("analysis_pass", 0) + 1

    if not unit_analyses:
        return {"analysis_questions": {}, "analysis_complete": True, "analysis_pass": analysis_pass}

    # ---- 1. Deterministic structural gaps (grounded, no LLM) ----
    # Group units by real file path so split large-file units (which share a
    # path) are compared as a whole — the union of their captured interfaces vs
    # everything tree-sitter found in the file.
    from collections import defaultdict
    by_path: dict[str, list] = defaultdict(list)
    for ua in unit_analyses:
        by_path[ua.path].append(ua)

    questions: dict[str, list[str]] = {}
    for path, group in by_path.items():
        structure = parse_file(os.path.join(repo_path, path))
        found = {n for n in (structure.get("functions", []) + structure.get("classes", [])) if n}
        captured = {i.name for ua in group for i in ua.interfaces if i.name}
        missing = sorted(found - captured)
        if missing:
            # Attribute the gap to the first unit of this file
            target = group[0].unit_id
            questions.setdefault(target, []).extend(
                f"The code defines '{name}' but it is not documented anywhere for this file — "
                f"capture its purpose, inputs, outputs, and side effects."
                for name in missing
            )
        # Empty-intent interfaces are attributed to their own unit
        for ua in group:
            for i in ua.interfaces:
                if i.name and not (i.intent or "").strip():
                    questions.setdefault(ua.unit_id, []).append(
                        f"Interface '{i.name}' has no intent — explain WHAT it does and WHY."
                    )

    # ---- 2. LLM qualitative review (best-effort) ----
    units_summary = [
        {
            "unit_id": ua.unit_id,
            "path": ua.path,
            "purpose": ua.purpose,
            "interfaces": [
                {"name": i.name, "kind": i.kind, "intent": i.intent,
                 "has_side_effects": bool(i.side_effects), "has_outputs": bool(i.outputs)}
                for i in ua.interfaces
            ],
        }
        for ua in unit_analyses
    ]
    try:
        raw = call_llm_json(REVIEW_COMPLETENESS_PROMPT.format(
            units_json=json.dumps(units_summary, indent=2)[:12000],
        ))
        for uid, qs in (raw.get("questions") or {}).items():
            if qs:
                questions.setdefault(uid, []).extend(q for q in qs if isinstance(q, str))
    except Exception:
        pass  # deterministic gaps still stand

    analysis_complete = len(questions) == 0
    return {
        "analysis_questions": questions,
        "analysis_complete": analysis_complete,
        "analysis_pass": analysis_pass,
    }
