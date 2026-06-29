"""
reduce_modules node: groups unit analyses by directory and synthesizes
a ModuleSummary for each group.
"""

import json
import os
from collections import defaultdict

from state_schema import ModuleSummary, PipelineState

from pipeline.prompts.prompts import REDUCE_MODULES_PROMPT
from pipeline.llm import call_llm_json


def reduce_modules(state: PipelineState) -> dict:
    unit_analyses = state.get("unit_analyses", [])

    # Group by directory (module)
    groups: dict[str, list] = defaultdict(list)
    for ua in unit_analyses:
        module_dir = os.path.dirname(ua.path) or "."
        groups[module_dir].append(ua)

    module_summaries: list[ModuleSummary] = []

    for module_name, units in groups.items():
        # Build lightweight summary for each unit (no raw source)
        units_data = [
            {
                "unit_id": u.unit_id,
                "path": u.path,
                "language": u.language,
                "purpose": u.purpose,
                "interfaces": [
                    {
                        "name": i.name,
                        "kind": i.kind,
                        "signature": i.signature,
                        "intent": i.intent,
                        "inputs": i.inputs,
                        "outputs": i.outputs,
                        "raises": i.raises,
                        "side_effects": i.side_effects,
                    }
                    for i in u.interfaces
                ],
                "internal_deps": u.internal_deps,
                "external_deps": u.external_deps,
                "idioms": u.idioms,
                "behavioral_notes": u.behavioral_notes,
            }
            for u in units
        ]

        module_id = module_name.replace(os.sep, "_").replace(".", "_").replace("/", "_")

        # Deterministic public surface: the real interfaces these units expose.
        public_surface = sorted({
            f"{i.name} ({i.kind})"
            for u in units for i in u.interfaces if i.name
        })

        # Deterministic collaborators: other module directories this one imports.
        collaborators = sorted({
            os.path.dirname(dep) or "."
            for u in units for dep in u.internal_deps
            if (os.path.dirname(dep) or ".") != module_name
        })

        # Grounded fallback responsibility built from the actual unit purposes.
        purposes = [u.purpose.strip() for u in units if u.purpose and u.purpose.strip()]
        if len(units) == 1:
            fallback = purposes[0] if purposes else f"Contains {units[0].path}."
        else:
            fallback = (
                f"Groups {len(units)} unit(s): "
                + "; ".join(purposes[:5]) if purposes
                else f"Groups {len(units)} unit(s) under {module_name}."
            )

        # LLM provides the prose responsibility only; everything else is grounded.
        try:
            raw = call_llm_json(REDUCE_MODULES_PROMPT.format(
                module_name=module_name,
                units_json=json.dumps(units_data, indent=2),
            ))
            responsibility = (raw.get("responsibility") or "").strip()
        except Exception:
            responsibility = ""

        if not responsibility:
            responsibility = fallback

        module_summaries.append(ModuleSummary(
            module_id=module_id,
            name=module_name,
            responsibility=responsibility,
            public_surface=public_surface,
            collaborators=collaborators,
            unit_ids=[u.unit_id for u in units],
        ))

    return {"module_summaries": module_summaries}
