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
**Intent:** Compile a compact list of verifiable facts from the pipeline state to ensure document consistency.

**Inputs:**
- state: PipelineState — the current pipeline state containing analyses and manifests
**Outputs:**
- str — a JSON string of verifiable facts

### `review_consistency` (function)
```
review_consistency(state: PipelineState) -> dict
```
**Intent:** Check the draft document against the ground truth and report any inconsistencies.

**Inputs:**
- state: PipelineState — the current pipeline state containing the draft document and analyses
**Outputs:**
- dict — results of the consistency review, including findings

## Internal dependencies
- pipeline/llm.py
- pipeline/prompts/prompts.py
- state_schema.py

## External dependencies
- json
- state_schema

## Flagged idioms
- Use of f-strings for concise string formatting in Python.

## Behavioral notes
- The function review_consistency will pass the review if no unit analyses are available, indicating a skipped review.
