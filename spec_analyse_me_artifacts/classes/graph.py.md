# graph.py

**File:** graph.py  
**Language:** python

## Purpose
Facilitate the construction and execution of a code-to-spec pipeline using a state graph.

## Interfaces
### `route_to_units` (function)
```
route_to_units(state: PipelineState) -> list[Send]
```
**Intent:** Generate a list of Send objects for each unit descriptor to be analyzed.

**Inputs:**
- state: PipelineState — the current state of the pipeline
**Outputs:**
- list[Send] — a list of Send objects for each unit descriptor

### `should_refine_analysis` (function)
```
should_refine_analysis(state: PipelineState)
```
**Intent:** Determine whether to re-analyze flagged units or proceed to module reduction.

**Inputs:**
- state: PipelineState — the current state of the pipeline
**Outputs:**
- list[Send] or str — Send objects for re-analysis or 'reduce_modules' to proceed

### `should_revise` (function)
```
should_revise(state: PipelineState) -> str
```
**Intent:** Decide whether to loop back for revisions or end the process based on validation and review results.

**Inputs:**
- state: PipelineState — the current state of the pipeline
**Outputs:**
- str — 'assemble_document' to loop back or END to finish

### `build_graph` (function)
```
build_graph(checkpointer=None)
```
**Intent:** Construct and compile the state graph for the code-to-spec pipeline.

**Inputs:**
- checkpointer: optional — a checkpointing mechanism
**Outputs:**
- StateGraph — the compiled state graph for the pipeline

## Internal dependencies
- pipeline/nodes/analyze_unit.py
- pipeline/nodes/assemble_document.py
- pipeline/nodes/extract_architecture.py
- pipeline/nodes/generate_diagram.py
- pipeline/nodes/generate_tests.py
- pipeline/nodes/ingest.py
- pipeline/nodes/reduce_modules.py
- pipeline/nodes/review_completeness.py
- pipeline/nodes/review_consistency.py
- pipeline/nodes/route_units.py
- pipeline/nodes/synthesize_system.py
- pipeline/nodes/validate.py
- state_schema.py

## Flagged idioms
- Conditional edges in state graphs to manage flow based on state conditions.

## Behavioral notes
- The pipeline allows for a maximum of two revisions before finalizing the document.
