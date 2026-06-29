"""
LangGraph StateGraph wiring for the code-to-spec pipeline.
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Send

from state_schema import PipelineState
from pipeline.nodes.ingest import ingest
from pipeline.nodes.route_units import route_units
from pipeline.nodes.analyze_unit import analyze_unit
from pipeline.nodes.review_completeness import review_completeness
from pipeline.nodes.reduce_modules import reduce_modules
from pipeline.nodes.synthesize_system import synthesize_system
from pipeline.nodes.extract_architecture import extract_architecture
from pipeline.nodes.generate_tests import generate_tests
from pipeline.nodes.generate_diagram import generate_diagram
from pipeline.nodes.assemble_document import assemble_document
from pipeline.nodes.review_consistency import review_consistency
from pipeline.nodes.validate import validate

MAX_REVISIONS = 2


def route_to_units(state: PipelineState) -> list[Send]:
    """Conditional edge: fan out one Send per unit descriptor."""
    units = state.get("units_to_analyze", [])
    return [Send("analyze_unit", unit) for unit in units]


def should_refine_analysis(state: PipelineState):
    """After completeness review: re-analyze flagged units, or move on.

    Returns either a list of Send() (re-analyse the flagged units with their
    questions) or the string "reduce_modules" to proceed.
    """
    questions = state.get("analysis_questions", {})
    max_passes = state.get("max_analysis_passes", 0)
    current_pass = state.get("analysis_pass", 0)

    if not questions or current_pass > max_passes:
        return "reduce_modules"

    descriptors = {d["unit_id"]: d for d in state.get("units_to_analyze", [])}
    sends = []
    for unit_id, qs in questions.items():
        desc = descriptors.get(unit_id)
        if desc and qs:
            refined = dict(desc)
            refined["questions"] = qs
            sends.append(Send("analyze_unit", refined))
    return sends or "reduce_modules"


def should_revise(state: PipelineState) -> str:
    """Conditional edge after validate: loop back to assemble or end.

    The document is only accepted when BOTH the coverage critic (validate)
    and the anti-hallucination reviewer (review_consistency) pass.
    """
    coverage_ok = state.get("validation_passed", False)
    grounded_ok = state.get("review_passed", False)
    if coverage_ok and grounded_ok:
        return END
    if state.get("revision_count", 0) >= MAX_REVISIONS:
        # Exceeded revision limit — emit the best draft we have
        return END
    return "assemble_document"


def build_graph(checkpointer=None):
    builder = StateGraph(PipelineState)

    # Register nodes
    builder.add_node("ingest", ingest)
    builder.add_node("route_units", route_units)
    builder.add_node("analyze_unit", analyze_unit)
    builder.add_node("review_completeness", review_completeness)
    builder.add_node("reduce_modules", reduce_modules)
    builder.add_node("synthesize_system", synthesize_system)
    builder.add_node("extract_architecture", extract_architecture)
    builder.add_node("generate_tests", generate_tests)
    builder.add_node("generate_diagram", generate_diagram)
    builder.add_node("assemble_document", assemble_document)
    builder.add_node("review_consistency", review_consistency)
    builder.add_node("validate", validate)

    # Linear edges
    builder.add_edge(START, "ingest")
    builder.add_edge("ingest", "route_units")

    # Fan-out: route_units → [Send × N] → analyze_unit
    builder.add_conditional_edges("route_units", route_to_units, ["analyze_unit"])

    # Fan-in: after all analyze_unit branches complete → completeness review
    builder.add_edge("analyze_unit", "review_completeness")

    # Completeness loop: re-analyse flagged units (with questions) or proceed
    builder.add_conditional_edges(
        "review_completeness",
        should_refine_analysis,
        ["analyze_unit", "reduce_modules"],
    )

    builder.add_edge("reduce_modules", "synthesize_system")
    builder.add_edge("synthesize_system", "extract_architecture")
    builder.add_edge("extract_architecture", "generate_tests")
    builder.add_edge("generate_tests", "generate_diagram")
    builder.add_edge("generate_diagram", "assemble_document")

    # Assembled draft → anti-hallucination review → coverage critic
    builder.add_edge("assemble_document", "review_consistency")
    builder.add_edge("review_consistency", "validate")

    # Critic loop or end (requires both review_passed and validation_passed)
    builder.add_conditional_edges(
        "validate",
        should_revise,
        {END: END, "assemble_document": "assemble_document"},
    )

    return builder.compile(checkpointer=checkpointer)
