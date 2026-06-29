# pipeline/artifacts.py

**File:** pipeline/artifacts.py  
**Language:** python

## Purpose
Render pipeline outputs to human-readable Markdown for documentation purposes.

## Interfaces
### `render_class_spec` (function)
```
render_class_spec(ua) -> str
```
**Intent:** Generate a Markdown document detailing the specifications of a unit analysis.

**Inputs:**
- ua: UnitAnalysis — the unit analysis object to render
**Outputs:**
- str — Markdown representation of the unit analysis

### `render_stage_doc` (function)
```
render_stage_doc(node_id: str, update: dict) -> str | None
```
**Intent:** Create a Markdown document summarizing the results of a pipeline stage based on its state update.

**Inputs:**
- node_id: str — identifier for the pipeline stage
- update: dict — state update information for the stage
**Outputs:**
- str | None — Markdown document for the stage or None if not applicable

### `write_text` (function)
```
write_text(path: Path, content: str) -> None
```
**Intent:** Helper function to write text content to a file.

**Inputs:**
- path: Path — the file path to write to
- content: str — the text content to write
**Outputs:**
- None
**Side effects:**
- Writes content to a file at the specified path

## External dependencies
- json
- __future__
- pathlib

## Flagged idioms
- Use of type annotations for function signatures to enhance code clarity and type checking.

## Behavioral notes
- The `render_stage_doc` function returns None if the update is not a dictionary or if the node_id does not match any known stages.
