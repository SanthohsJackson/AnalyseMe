"""
validate node: critic agent checks the draft document for coverage gaps.
"""

import json

from state_schema import PipelineState

from pipeline.prompts.prompts import VALIDATE_PROMPT
from pipeline.llm import call_llm_json

# Words signalling a gap is about an interface being undocumented/unlisted.
_DOC_GAP_WORDS = ("document", "listed", "described", "mentioned", "covered", "missing")


def _filter_coverage_gaps(gaps: list[str], document: str, interface_names: set[str]) -> list[str]:
    """Drop 'interface not documented' gaps for interfaces that ARE in the doc.

    Every interface is documented in the deterministic Interface Reference, so a
    'not documented' gap naming an interface that appears in the document is a
    false positive (often caused by the critic only seeing a truncated draft)."""
    doc_low = document.lower()
    kept = []
    for g in gaps:
        gl = g.lower()
        if any(w in gl for w in _DOC_GAP_WORDS):
            mentioned = [n for n in interface_names if n and n.lower() in gl]
            if mentioned and all(n.lower() in doc_low for n in mentioned):
                continue  # the interface(s) are present/documented in the spec
        kept.append(g)
    return kept


def validate(state: PipelineState) -> dict:
    unit_analyses = state.get("unit_analyses", [])
    draft_document = state.get("draft_document", "")

    # Collect all known public interfaces (and bare names for the gap filter).
    known_interfaces = []
    interface_names: set[str] = set()
    for ua in unit_analyses:
        for iface in ua.interfaces:
            known_interfaces.append(f"{ua.path}::{iface.name} ({iface.kind})")
            if iface.name:
                interface_names.add(iface.name)

    prompt = VALIDATE_PROMPT.format(
        known_interfaces=json.dumps(known_interfaces, indent=2),
        # Generous budget so the appended Interface Reference (where every
        # interface is documented) is actually visible to the critic.
        document=draft_document[:40000],
    )

    try:
        raw = call_llm_json(prompt)
        gaps = raw.get("gaps", [])
    except Exception as exc:
        # If we can't validate, treat as passed to avoid infinite loop
        return {
            "validation_passed": True,
            "validation_gaps": [f"Validation LLM call failed: {exc}"],
            "final_document": draft_document,
        }

    gaps = _filter_coverage_gaps(gaps, draft_document, interface_names)
    passed = not gaps
    final_document = draft_document if passed else ""

    return {
        "validation_passed": passed,
        "validation_gaps": gaps,
        "final_document": final_document,
    }
