# pipeline/nodes/review_consistency.py

**File:** pipeline/nodes/review_consistency.py  
**Language:** python

## Purpose
Review and ensure the consistency of a draft document against deterministic ground truth.

## Interfaces
### `_build_ground_truth` (function)
```
_build_ground_truth(state: PipelineState) -> str
```
**Intent:** Assemble a comprehensive set of verifiable facts to ensure the draft document's consistency.

**Inputs:**
- state: PipelineState — the current pipeline state containing analyses and dependencies
**Outputs:**
- str — JSON string of verifiable facts

### `_dep_name` (function)
```
_dep_name(s: str) -> str
```
**Intent:** Extract the package name from a dependency string, removing version specifiers.

**Inputs:**
- s: str — dependency string with version specifier
**Outputs:**
- str — package name without version specifier

### `_norm` (function)
```
_norm(t: str) -> str
```
**Intent:** Normalize a string by stripping punctuation and converting to lowercase.

**Inputs:**
- t: str — text to normalize
**Outputs:**
- str — normalized text

### `_is_symbol_like` (function)
```
_is_symbol_like(t: str) -> bool
```
**Intent:** Determine if a token resembles a code symbol based on naming conventions.

**Inputs:**
- t: str — token to check
**Outputs:**
- bool — whether the token resembles a code symbol

### `_collect_known_symbols` (function)
```
_collect_known_symbols(state: PipelineState) -> set[str]
```
**Intent:** Collect all known symbols from the pipeline state that the document may reference.

**Inputs:**
- state: PipelineState — the current pipeline state
**Outputs:**
- set[str] — set of known symbols

### `_filter_findings` (function)
```
_filter_findings(findings: list[str], state: PipelineState) -> list[str]
```
**Intent:** Filter out findings that are contradicted by the ground truth.

**Inputs:**
- findings: list[str] — list of findings to filter
- state: PipelineState — the current pipeline state
**Outputs:**
- list[str] — filtered list of findings

### `_strip_deterministic` (function)
```
_strip_deterministic(doc: str) -> str
```
**Intent:** Remove deterministic content from the document to focus on model-generated prose.

**Inputs:**
- doc: str — document to process
**Outputs:**
- str — document with deterministic content removed

### `review_consistency` (function)
```
review_consistency(state: PipelineState) -> dict
```
**Intent:** Review the draft document for consistency against the ground truth.

**Inputs:**
- state: PipelineState — the current pipeline state
**Outputs:**
- dict — review results indicating consistency status

## Internal dependencies
- pipeline/llm.py
- pipeline/prompts/prompts.py
- state_schema.py

## External dependencies
- json
- re

## Flagged idioms
- Use of regular expressions for string manipulation and pattern matching

## Behavioral notes
- The function _build_ground_truth relies on the completeness of the state to avoid false hallucination flags.
