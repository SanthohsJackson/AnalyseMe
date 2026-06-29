# pipeline/memory.py

**File:** pipeline/memory.py  
**Language:** python

## Purpose
Maintain a persistent log of past code-to-spec analysis runs to prevent repeated hallucinations.

## Interfaces
### `__init__` (method)
```
__init__(self, path: str | os.PathLike | None = None, max_entries: int | None = 50)
```
**Intent:** Initialize the RunMemory object with a specified file path and maximum number of entries to store.

**Inputs:**
- path: str | os.PathLike | None — the file path for storing memory
- max_entries: int | None — maximum number of entries to retain
**Side effects:**
- Initializes the RunMemory object with a specified path and entry limit.

### `store_run` (method)
```
store_run(self, repo_path: str, model: str, languages: list[str], unit_count: int, hallucinations: list[str], reflection: str = "") -> None
```
**Intent:** Append a new analysis run entry to the memory log, capturing hallucinations and reflections.

**Inputs:**
- repo_path: str — path to the repository
- model: str — model used for analysis
- languages: list[str] — languages involved in the analysis
- unit_count: int — number of units analyzed
- hallucinations: list[str] — list of hallucinations caught
- reflection: str — optional reflection notes
**Raises:**
- OSError: if there is an issue with file operations
**Side effects:**
- Writes a new entry to the markdown memory file, rotating entries if necessary.

### `_load_blocks` (method)
```
_load_blocks(self) -> list[str]
```
**Intent:** Load and return all log entries from the memory file.

**Outputs:**
- list[str] — list of log entries

### `get_past_context` (method)
```
get_past_context(self, repo_path: str, n: int = 3) -> str
```
**Intent:** Retrieve and format lessons from past runs of a specific repository to prevent repeated hallucinations in future analyses.

**Inputs:**
- repo_path: str — path to the repository
- n: int — number of past entries to consider
**Outputs:**
- str — formatted lessons from past runs

### `_rotate` (method)
```
_rotate(self, blocks: list[str]) -> list[str]
```
**Intent:** Ensure the number of log entries does not exceed the maximum allowed by removing the oldest entries.

**Inputs:**
- blocks: list[str] — list of log entries
**Outputs:**
- list[str] — rotated list of log entries

## External dependencies
- os
- __future__
- datetime
- pathlib

## Flagged idioms
- Use of HTML comments as delimiters to ensure safe separation of log entries.

## Behavioral notes
- The memory log is append-only and uses atomic file operations to prevent corruption.
