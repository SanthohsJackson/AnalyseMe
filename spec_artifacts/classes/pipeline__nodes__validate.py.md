# pipeline/nodes/validate.py

**File:** pipeline/nodes/validate.py  
**Language:** python

## Purpose
Validate a draft document against known interfaces for coverage gaps using a language model.

## Interfaces
### `validate` (function)
```
validate(state: PipelineState) -> dict
```
**Intent:** Checks the draft document for coverage gaps by comparing it against known interfaces and using a language model for validation.

**Inputs:**
- state: PipelineState — the current pipeline state containing unit analyses and draft document
**Outputs:**
- dict — containing validation results, gaps, and final document
**Raises:**
- Exception: when LLM call fails

## Internal dependencies
- pipeline/llm.py
- pipeline/prompts/prompts.py
- state_schema.py

## External dependencies
- json

## Flagged idioms
- Truncating document to 12000 characters for context limitation in LLM call

## Behavioral notes
- If the LLM call fails, the function defaults to passing validation to prevent infinite loops.
