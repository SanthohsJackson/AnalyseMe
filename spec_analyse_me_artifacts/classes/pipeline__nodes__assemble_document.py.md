# pipeline/nodes/assemble_document.py

**File:** pipeline/nodes/assemble_document.py  
**Language:** python

## Purpose
Render a reimplementation specification document from collected analysis data.

## Interfaces
### `_build_inventory` (function)
```
_build_inventory(state: PipelineState) -> str
```
**Intent:** Generate a textual inventory of the project's files, languages, entry points, and dependencies.

**Inputs:**
- state: PipelineState — the current pipeline state containing analysis data
**Outputs:**
- str — a formatted inventory of files, languages, entry points, and dependencies

### `_insert_diagram` (function)
```
_insert_diagram(doc: str, diagram: str) -> str
```
**Intent:** Insert a Mermaid diagram into the document after the 'Architecture' heading or append it as a new section.

**Inputs:**
- doc: str — the document text to modify
- diagram: str — the diagram to insert
**Outputs:**
- str — the document text with the diagram inserted

### `assemble_document` (function)
```
assemble_document(state: PipelineState) -> dict
```
**Intent:** Compile a draft document from analysis data, including inventory, modules, schemas, and tests.

**Inputs:**
- state: PipelineState — the current pipeline state containing analysis data
**Outputs:**
- dict — containing the draft document and updated revision count

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
- Use of defaultdict to group files by language efficiently

## Behavioral notes
- The _insert_diagram function ensures the diagram is placed correctly without relying on LLM output.
