# pipeline/nodes/generate_diagram.py

**File:** pipeline/nodes/generate_diagram.py  
**Language:** python

## Purpose
Generate Mermaid architecture diagrams from pipeline analysis data.

## Interfaces
### `_node_id` (function)
```
_node_id(name: str) -> str
```
**Intent:** Create a stable identifier for a node that is safe to use in Mermaid diagrams.

**Inputs:**
- name: str — the name to convert into a node id
**Outputs:**
- str — a stable, Mermaid-safe node id

### `_module_label` (function)
```
_module_label(name: str) -> str
```
**Intent:** Generate a label for a module, using '(root)' for the root module.

**Inputs:**
- name: str — the module name to label
**Outputs:**
- str — a label for the module

### `_clean_label` (function)
```
_clean_label(text: str, limit: int = 40) -> str
```
**Intent:** Clean and truncate text to make it suitable for use as a Mermaid label.

**Inputs:**
- text: str — the text to clean
- limit: int — maximum length of the label
**Outputs:**
- str — cleaned and possibly truncated label

### `_module_graph` (function)
```
_module_graph(modules, entry_points) -> str | None
```
**Intent:** Generate a Mermaid graph for module dependencies, highlighting entry-point modules.

**Inputs:**
- modules: list — list of module objects
- entry_points: list — list of entry point paths
**Outputs:**
- str | None — Mermaid graph definition or None if no modules

### `_integrations_graph` (function)
```
_integrations_graph(cross_cutting, system_label: str) -> str | None
```
**Intent:** Generate a Mermaid graph for external integrations of the system.

**Inputs:**
- cross_cutting: object — object containing external integrations
- system_label: str — label for the system
**Outputs:**
- str | None — Mermaid graph definition or None if no integrations

### `_member_name` (function)
```
_member_name(name: str) -> str
```
**Intent:** Sanitize a name to be a valid member name in Mermaid class diagrams.

**Inputs:**
- name: str — the name to sanitize
**Outputs:**
- str — sanitized member name

### `_field_type` (function)
```
_field_type(prop) -> str
```
**Intent:** Determine a human-readable type for a JSON-schema property.

**Inputs:**
- prop: dict — JSON-schema property
**Outputs:**
- str — human-readable type description

### `_refs` (function)
```
_refs(prop) -> set[str]
```
**Intent:** Identify schema names referenced by a JSON-schema property.

**Inputs:**
- prop: dict — JSON-schema property
**Outputs:**
- set[str] — set of schema names referenced by the property

### `_data_model` (function)
```
_data_model(data_schemas) -> str | None
```
**Intent:** Generate a Mermaid class diagram for the data model from extracted schemas.

**Inputs:**
- data_schemas: list — list of data schema objects
**Outputs:**
- str | None — Mermaid class diagram or None if no schemas

### `generate_diagram` (function)
```
generate_diagram(state: PipelineState) -> dict
```
**Intent:** Generate architecture diagrams for module dependencies, external integrations, and data models.

**Inputs:**
- state: PipelineState — the pipeline state containing analysis data
**Outputs:**
- dict — dictionary containing the architecture diagram

## Internal dependencies
- state_schema.py

## External dependencies
- os
- state_schema

## Flagged idioms
- Use of f-strings for string formatting to create Mermaid-safe identifiers and labels.

## Behavioral notes
- The module graph truncates to the most-connected modules if there are more than 60.
