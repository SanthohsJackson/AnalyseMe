# pipeline/nodes/review_consistency.py

**File:** pipeline/nodes/review_consistency.py  
**Language:** python

## Purpose
Review a draft document for consistency against deterministic ground truth.

## Interfaces
### `_build_ground_truth` (function)
```
_build_ground_truth(state: PipelineState) -> str
```
**Intent:** Assemble a comprehensive set of verifiable facts from the pipeline state to ensure document consistency.

**Inputs:**
- state: PipelineState — the current pipeline state containing analyses and dependencies
**Outputs:**
- str — JSON string of the assembled ground truth facts

### `_strip_deterministic` (function)
```
_strip_deterministic(doc: str) -> str
```
**Intent:** Remove deterministic content from the document to focus the review on model-generated prose.

**Inputs:**
- doc: str — the draft document to process
**Outputs:**
- str — the document with deterministic content removed

### `review_consistency` (function)
```
review_consistency(state: PipelineState) -> dict
```
**Intent:** Review the draft document for consistency against the assembled ground truth and report findings.

**Inputs:**
- state: PipelineState — the current pipeline state containing the draft document and analyses
**Outputs:**
- dict — results of the consistency review including pass status and findings

## Internal dependencies
- pipeline/llm.py
- pipeline/prompts/prompts.py
- state_schema.py

## External dependencies
- json
- re

## Flagged idioms
- Use of regular expressions to manipulate and split strings.

## Behavioral notes
- The function _build_ground_truth ensures that all relevant facts are included to prevent false hallucinations during review.
- The review_consistency function handles exceptions gracefully, ensuring the pipeline continues even if the review agent fails.
