"""
synthesize_system node: rolls up module summaries into a system-level overview.
"""

import json
import os

from state_schema import PipelineState

from pipeline.prompts.prompts import SYNTHESIZE_SYSTEM_PROMPT
from pipeline.llm import call_llm_text


def synthesize_system(state: PipelineState) -> dict:
    module_summaries = state.get("module_summaries", [])
    repo_name = os.path.basename(state.get("repo_path", "unknown"))

    modules_data = [
        {
            "module_id": m.module_id,
            "name": m.name,
            "responsibility": m.responsibility,
            "public_surface": m.public_surface,
            "collaborators": m.collaborators,
        }
        for m in module_summaries
    ]

    # Phase 7 RAG: full context when it fits, retrieval when the repo is large.
    from pipeline.rag import select_context

    full_json = json.dumps(modules_data, indent=2)
    records = [
        {
            "id": m.module_id,
            "full": json.dumps(md, indent=2),
            "compact": f"{m.name}: {(m.responsibility or '')[:120]}",
        }
        for m, md in zip(module_summaries, modules_data)
    ]
    modules_ctx, _ = select_context(
        full_json, records,
        query="overall system architecture, data flow, module boundaries, key design decisions",
    )

    entry_points = state.get("entry_points", [])
    languages = state.get("languages_detected", [])

    prompt = SYNTHESIZE_SYSTEM_PROMPT.format(
        repo_name=repo_name,
        languages=", ".join(languages) or "unknown",
        entry_points="\n".join(f"- {ep}" for ep in entry_points) or "- (none detected)",
        modules_json=modules_ctx,
    )

    system_overview = call_llm_text(prompt)
    return {"system_overview": system_overview}
