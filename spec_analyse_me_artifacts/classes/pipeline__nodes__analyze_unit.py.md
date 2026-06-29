# pipeline/nodes/analyze_unit.py

**File:** pipeline/nodes/analyze_unit.py  
**Language:** python

## Purpose
Analyze a unit of code to extract its structure and perform semantic analysis using an LLM.

## Interfaces
### `_get_semaphore` (function)
```
_get_semaphore(size: int) -> threading.BoundedSemaphore
```
**Intent:** Create or retrieve a semaphore to control concurrency based on the specified size.

**Inputs:**
- size: int — the desired size of the semaphore
**Outputs:**
- threading.BoundedSemaphore — a semaphore object with the specified size
**Side effects:**
- modifies _SEM_STATE to store the semaphore and its size

### `_elide` (function)
```
_elide(source_bytes: bytes, ranges: list) -> str
```
**Intent:** Replace specified byte ranges in the source with a marker to indicate elided content.

**Inputs:**
- source_bytes: bytes — the source file content
- ranges: list — byte ranges to be replaced
**Outputs:**
- str — the modified source with specified ranges elided

### `_select_source` (function)
```
_select_source(state: dict) -> tuple[str, str]
```
**Intent:** Select and return the relevant source snippet and focus note based on the unit kind.

**Inputs:**
- state: dict — the unit descriptor containing path and kind information
**Outputs:**
- tuple[str, str] — a snippet of the source and a focus note

### `analyze_unit` (function)
```
analyze_unit(state: dict) -> dict
```
**Intent:** Perform structure extraction and semantic analysis on a code unit, returning the analysis results.

**Inputs:**
- state: dict — the unit descriptor with analysis parameters
**Outputs:**
- dict — containing unit analyses and any mapping errors

## Internal dependencies
- pipeline/llm.py
- pipeline/parsers/tree_sitter_parser.py
- pipeline/prompts/prompts.py
- state_schema.py

## External dependencies
- json
- os
- threading
- traceback
- state_schema

## Flagged idioms
- Use of threading.BoundedSemaphore to control concurrency

## Behavioral notes
- The semaphore size is adjusted to be at least 1, ensuring there is always some concurrency control.
