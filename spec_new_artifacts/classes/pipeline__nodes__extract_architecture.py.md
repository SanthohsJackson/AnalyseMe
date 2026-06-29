# pipeline/nodes/extract_architecture.py

**File:** pipeline/nodes/extract_architecture.py  
**Language:** python

## Purpose
Derive data schemas and cross-cutting concerns from module summaries.

## Interfaces
### `_aggregate_evidence` (function)
```
_aggregate_evidence(unit_analyses, dep_manifest) -> dict
```
**Intent:** Aggregate cross-cutting evidence from unit analyses and dependency manifests.

**Inputs:**
- unit_analyses: list — analyses of individual units
- dep_manifest: dict — manifest of dependencies
**Outputs:**
- dict — aggregated evidence of cross-cutting concerns

### `extract_architecture` (function)
```
extract_architecture(state: PipelineState) -> dict
```
**Intent:** Extract data schemas and cross-cutting concerns from the pipeline state.

**Inputs:**
- state: PipelineState — the current state of the pipeline
**Outputs:**
- dict — data schemas and cross-cutting concerns

### `_summary` (function)
```
_summary(items: list[str], n: int = 5) -> str
```
**Intent:** Create a summary string from a list of items, limiting the number of items.

**Inputs:**
- items: list[str] — list of strings to summarize
- n: int — maximum number of items to include in the summary
**Outputs:**
- str — summarized string

## Internal dependencies
- pipeline/llm.py
- pipeline/prompts/prompts.py
- pipeline/rag.py
- state_schema.py

## External dependencies
- json

## Flagged idioms
- Use of list comprehensions for concise data transformation
- Use of set for unique collection of external dependencies

## Behavioral notes
- Evidence lists are capped to 20 items to keep prompts bounded.
- Fallback mechanism fills cross-cutting concerns deterministically if model output is empty.
