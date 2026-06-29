# pipeline/nodes/review_consistency.py

**File:** pipeline/nodes/review_consistency.py  
**Language:** python

## Purpose
Review and validate a draft document against a deterministic ground truth to prevent hallucinations.

## Interfaces
### `_build_ground_truth` (function)
```
_build_ground_truth(state: PipelineState) -> str
```
**Intent:** Assemble a JSON representation of the verifiable facts from the pipeline state to ensure document consistency.

**Inputs:**
- state: PipelineState — the current pipeline state containing analyses and dependencies
**Outputs:**
- str — JSON string of the assembled ground truth facts

### `review_consistency` (function)
```
review_consistency(state: PipelineState) -> dict
```
**Intent:** Evaluate the draft document against the ground truth to identify unsupported claims and ensure consistency.

**Inputs:**
- state: PipelineState — the current pipeline state containing the draft document and analyses
**Outputs:**
- dict — result of the review with pass status and findings

## Internal dependencies
- pipeline/llm.py
- pipeline/prompts/prompts.py
- state_schema.py

## External dependencies
- json
- state_schema

## Flagged idioms
- Use of JSON for structured data representation and communication with LLM.

## Behavioral notes
- If no unit analyses are available, the review is skipped with a note.
- The review process is resilient to LLM call failures, defaulting to a pass with an error message.
