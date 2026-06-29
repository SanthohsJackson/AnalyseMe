# cli/main.py::<module>

**File:** cli/main.py  
**Language:** python

## Purpose
Provide a rich terminal UI for the Analyse Me pipeline, facilitating user interaction and pipeline execution.

## Interfaces
### `_default` (function)
```
_default(ctx: typer.Context) -> None
```
**Intent:** Invoke the startup menu if no subcommand is provided.

**Inputs:**
- ctx: typer.Context — the context of the Typer application

### `create_layout` (function)
```
create_layout() -> Layout
```
**Intent:** Set up the layout structure for the terminal UI.

**Outputs:**
- Layout — the configured layout for the terminal UI

### `update_display` (function)
```
update_display(layout: Layout) -> None
```
**Intent:** Refresh the terminal UI with the latest pipeline progress and messages.

**Inputs:**
- layout: Layout — the layout to update with current information

### `get_user_selections` (function)
```
get_user_selections() -> dict
```
**Intent:** Collect user input for pipeline configuration through an interactive wizard.

**Outputs:**
- dict — user selections for pipeline configuration

### `step_box` (function)
```
step_box(title: str, hint: str) -> None
```
**Intent:** Display a step box with a title and hint in the terminal UI.

**Inputs:**
- title: str — the title of the step
- hint: str — a hint or description for the step

### `_safe_name` (function)
```
_safe_name(path: str) -> str
```
**Intent:** Convert a unit path into a filename-safe string.

**Inputs:**
- path: str — the unit path to convert
**Outputs:**
- str — a safe filename derived from the path

### `_persist_class_spec` (function)
```
_persist_class_spec(ua) -> None
```
**Intent:** Store the per-class specification in the buffer and on disk.

**Inputs:**
- ua — the unit analysis object

### `_persist_stage_doc` (function)
```
_persist_stage_doc(node_id: str, update: dict) -> None
```
**Intent:** Store the per-stage documentation in the buffer and on disk.

**Inputs:**
- node_id: str — the identifier of the pipeline stage
- update: dict — the update data for the stage

### `_pause` (function)
```
_pause(message: str = 'Press Enter to return to the menu…') -> None
```
**Intent:** Pause execution and wait for user input to continue.

**Inputs:**
- message: str — the message to display during the pause

### `_render_doc` (function)
```
_render_doc(title: str, content: str) -> None
```
**Intent:** Render a markdown document in the terminal UI.

**Inputs:**
- title: str — the title of the document
- content: str — the content of the document

### `interactive_viewer` (function)
```
interactive_viewer(final_doc: str) -> None
```
**Intent:** Allow users to browse through various documents and reports post-pipeline execution.

**Inputs:**
- final_doc: str — the final document to display

### `run_pipeline` (function)
```
run_pipeline(no_cache: bool = False, clear_cache: bool = False) -> None
```
**Intent:** Execute the pipeline with the given configuration and cache settings.

**Inputs:**
- no_cache: bool — whether to disable caching
- clear_cache: bool — whether to clear the cache

## Internal dependencies
- cli/chat.py
- cli/utils.py
- graph.py
- pipeline/artifacts.py
- pipeline/cache.py
- pipeline/indexer.py
- pipeline/llm.py
- pipeline/memory.py
- pipeline/model_catalog.py
- pipeline/reflection.py
- pipeline/repo_source.py
- pipeline/vectordb.py

## External dependencies
- datetime
- os
- time
- uuid
- questionary
- typer
- sys
- collections
- pathlib
- rich
- rich.align
- rich.console
- rich.layout
- rich.live
- rich.markdown
- rich.panel
- rich.rule
- rich.spinner
- rich.table
- rich.text

## Flagged idioms
- Use of Typer for CLI application structure
- Rich library for enhanced terminal UI

## Behavioral notes
- The UI layout is dynamically updated based on pipeline progress and user interactions.
- The interactive viewer allows users to navigate through different stages and documents post-execution.
