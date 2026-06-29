# pipeline/nodes/assemble_document.py

**File:** pipeline/nodes/assemble_document.py  
**Language:** python

## Purpose
Render the final reimplementation spec document from collected analysis data.

## Interfaces
### `_build_inventory` (function)
```
_build_inventory(state: PipelineState) -> str
```
**Intent:** Generate a detailed inventory report of files, languages, entry points, and dependencies from the pipeline state.

**Inputs:**
- state: PipelineState — the current pipeline state containing analysis data
**Outputs:**
- str — a formatted inventory report

### `_build_interface_index` (function)
```
_build_interface_index(state: PipelineState) -> str
```
**Intent:** Create a comprehensive index of all public interfaces extracted from the source code.

**Inputs:**
- state: PipelineState — the current pipeline state containing analysis data
**Outputs:**
- str — a formatted index of public interfaces

### `_insert_diagram` (function)
```
_insert_diagram(doc: str, diagram: str) -> str
```
**Intent:** Insert a Mermaid diagram into the document at a specific location or append it if no suitable location is found.

**Inputs:**
- doc: str — the document to insert the diagram into
- diagram: str — the diagram to be inserted
**Outputs:**
- str — the document with the diagram inserted

### `assemble_document` (function)
```
assemble_document(state: PipelineState) -> dict
```
**Intent:** Assemble the final document by integrating various components like inventory, interfaces, and diagrams based on the pipeline state.

**Inputs:**
- state: PipelineState — the current pipeline state containing analysis data
**Outputs:**
- dict — the assembled document data

## Internal dependencies
- pipeline/llm.py
- pipeline/prompts/prompts.py
- pipeline/rag.py
- state_schema.py

## External dependencies
- json
- collections
- state_schema

## Flagged idioms
- defaultdict — used to group files by language efficiently

## Behavioral notes
- The _build_inventory function limits the display of file paths to 20 per language.
- The _insert_diagram function appends the diagram if no 'Architecture' heading is found.
