# cli/main.py::PipelineBuffer

**File:** cli/main.py  
**Language:** python

## Purpose
Manage and track the state of a pipeline execution, including messages, node statuses, and artifacts.

## Interfaces
### `PipelineBuffer` (class)
```
PipelineBuffer(max_messages: int = 100)
```
**Intent:** Encapsulates the mutable state shared between the stream loop and the display renderer.

**Inputs:**
- max_messages: int — maximum number of messages to retain in the buffer

### `__init__` (method)
```
__init__(self, max_messages: int = 100)
```
**Intent:** Initialize the PipelineBuffer with default values and structures for tracking pipeline execution.

**Inputs:**
- max_messages: int — maximum number of messages to retain
**Side effects:**
- Initializes the message buffer and node status tracking.

### `add_message` (method)
```
add_message(self, msg_type: str, content: str) -> None
```
**Intent:** Add a new message to the buffer with a timestamp.

**Inputs:**
- msg_type: str — type of the message
- content: str — content of the message
**Side effects:**
- Appends a timestamped message to the message buffer.

### `set_node` (method)
```
set_node(self, node_id: str, status: str) -> None
```
**Intent:** Update the status of a specific node in the pipeline.

**Inputs:**
- node_id: str — identifier of the node
- status: str — new status of the node
**Side effects:**
- Updates the status of a node and sets it as the current node if in progress.

### `complete_node` (method)
```
complete_node(self, node_id: str) -> None
```
**Intent:** Mark a node as completed by updating its status.

**Inputs:**
- node_id: str — identifier of the node
**Side effects:**
- Marks a node as completed.

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
- Use of 'deque' for efficient message buffering with a maximum length.

## Behavioral notes
- The 'node_status' dictionary is initialized with 'pending' status for all nodes, indicating a default state before processing begins.
