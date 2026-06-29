"""
Code-to-Spec Agent Pipeline — LangGraph State Schema
=====================================================
A pipeline that ingests a codebase, analyzes it into a language-agnostic
intermediate representation (LCIR), and emits a reimplementation spec doc
that can be used to rebuild the system in any target language.

Design notes:
- Deterministic structure extraction (tree-sitter) + LLM for intent only.
- Map-reduce: per-unit analysis fans out, synthesis fans in.
- Fan-in fields use Annotated[..., operator.add] reducers so parallel
  branches concatenate instead of overwrite.
- Checkpointer makes a 100k-line run resumable.
"""

from __future__ import annotations

import operator
from enum import Enum
from typing import Annotated, Optional, TypedDict

from pydantic import BaseModel, Field


def merge_unit_analyses(existing, new):
    """Reducer for unit_analyses: merge by unit_id so a re-analysis of a unit
    *replaces* its previous analysis instead of appending a duplicate. This is
    what makes the multi-pass refinement loop update data in place."""
    by_id: dict = {}
    for ua in (existing or []):
        by_id[ua.unit_id] = ua
    for ua in (new or []):
        by_id[ua.unit_id] = ua  # later analysis wins
    return list(by_id.values())


# ---------------------------------------------------------------------------
# Domain models (the LCIR — Language-Concept Intermediate Representation)
# ---------------------------------------------------------------------------

class FileKind(str, Enum):
    SOURCE = "source"
    TEST = "test"
    CONFIG = "config"
    BUILD = "build"
    DOC = "doc"
    OTHER = "other"


class FileMeta(BaseModel):
    path: str
    language: Optional[str] = None          # detected via extension / tree-sitter
    kind: FileKind = FileKind.OTHER
    loc: int = 0
    imports: list[str] = Field(default_factory=list)   # raw import targets
    depends_on: list[str] = Field(default_factory=list)  # resolved internal paths


class Interface(BaseModel):
    """A public surface element: function, method, class, endpoint, etc."""
    name: str
    signature: str                          # source-language signature (reference)
    kind: str                               # "function" | "class" | "endpoint" | ...
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    raises: list[str] = Field(default_factory=list)
    side_effects: list[str] = Field(default_factory=list)
    intent: str = ""                        # LLM: WHAT and WHY, not HOW


class UnitAnalysis(BaseModel):
    """Output of the map step — one per analyzable unit (file or class)."""
    unit_id: str
    path: str
    language: str
    purpose: str
    interfaces: list[Interface] = Field(default_factory=list)
    internal_deps: list[str] = Field(default_factory=list)
    external_deps: list[str] = Field(default_factory=list)
    idioms: list[str] = Field(default_factory=list)   # language-specific patterns flagged
    behavioral_notes: list[str] = Field(default_factory=list)


class UnitAnalysisResult(BaseModel):
    """Schema for the analyze_unit LLM *response* — the intent fields only.

    Kept separate from UnitAnalysis because unit_id/path/language are filled
    deterministically (not by the model). Used with structured output so the
    model is constrained to these keys and cannot invent top-level fields.
    internal_deps is resolved deterministically downstream and overrides any
    value the model emits here.
    """
    purpose: str = ""
    interfaces: list[Interface] = Field(default_factory=list)
    internal_deps: list[str] = Field(default_factory=list)
    external_deps: list[str] = Field(default_factory=list)
    idioms: list[str] = Field(default_factory=list)
    behavioral_notes: list[str] = Field(default_factory=list)


class ModuleSummary(BaseModel):
    """Output of an intermediate reduce step."""
    module_id: str
    name: str
    responsibility: str
    public_surface: list[str] = Field(default_factory=list)
    collaborators: list[str] = Field(default_factory=list)
    unit_ids: list[str] = Field(default_factory=list)


class DataSchema(BaseModel):
    name: str
    description: str
    json_schema: dict = Field(default_factory=dict)   # language-neutral type description


class CrossCutting(BaseModel):
    error_handling: str = ""
    config: str = ""
    logging: str = ""
    auth: str = ""
    concurrency: str = ""
    external_integrations: list[str] = Field(default_factory=list)


class BehavioralTest(BaseModel):
    """Language-neutral acceptance criterion for reimplementation."""
    target_interface: str
    given: str
    when: str
    then: str


# ---------------------------------------------------------------------------
# Graph state
# ---------------------------------------------------------------------------

class PipelineState(TypedDict, total=False):
    # ---- Inputs / config ----
    repo_path: str
    output_path: str
    max_parallelism: int
    max_files: Optional[int]
    skip_tests: bool
    max_analysis_passes: int           # how many completeness-refinement loops are allowed
    prior_lessons: str                 # injected memory of hallucinations caught on past runs

    # ---- Ingest node outputs ----
    files: list[FileMeta]
    languages_detected: list[str]
    entry_points: list[str]
    dependency_manifest: dict          # parsed package.json / go.mod / etc.

    # ---- Routing ----
    units_to_analyze: list[dict]       # lightweight unit descriptors for Send fan-out

    # ---- MAP (fan-out, parallel). Reducer = merge by unit_id (re-analysis replaces) ----
    unit_analyses: Annotated[list[UnitAnalysis], merge_unit_analyses]
    map_errors: Annotated[list[str], operator.add]    # partial-failure capture

    # ---- Completeness review / multi-pass refinement ----
    analysis_questions: dict           # unit_id -> [questions the next pass must answer]
    analysis_complete: bool            # True when no capture gaps remain
    analysis_pass: int                 # how many completeness reviews have run

    # ---- REDUCE (hierarchical synthesis) ----
    module_summaries: list[ModuleSummary]
    system_overview: str

    # ---- Architecture node outputs ----
    data_schemas: list[DataSchema]
    cross_cutting: CrossCutting
    behavioral_tests: Annotated[list[BehavioralTest], operator.add]
    architecture_diagram: str          # Mermaid diagram built from the resolved module graph

    # ---- Assembly / validation ----
    draft_document: str
    final_document: str
    validation_gaps: list[str]
    validation_passed: bool
    revision_count: int                # guard against infinite critic loops

    # ---- Review agent (anti-hallucination grounding check) ----
    review_findings: list[str]         # claims in the draft not supported by analysis
    review_passed: bool                # True when the draft is grounded in the facts
    artifacts_dir: str                 # where per-stage / per-class docs are written
