# pipeline/memory.py

**File:** pipeline/memory.py  
**Language:** python

## Purpose
Manage and persistently store cross-run memory logs for code-to-spec analysis.

## Interfaces
### `RunMemory` (class)
```
RunMemory(path: str | os.PathLike | None = None, max_entries: int | None = 50)
```
**Intent:** Initialize a RunMemory instance with a specified path and maximum number of entries.

**Inputs:**
- path: str | os.PathLike | None — the file path for storing memory logs
- max_entries: int | None — maximum number of entries to retain

### `__init__` (method)
```
__init__(self, path: str | os.PathLike | None = None, max_entries: int | None = 50) -> None
```
**Intent:** Set up the memory log file path and entry limit for the RunMemory instance.

**Inputs:**
- self: RunMemory instance
- path: str | os.PathLike | None — the file path for storing memory logs
- max_entries: int | None — maximum number of entries to retain

### `store_run` (method)
```
store_run(self, repo_path: str, model: str, languages: list[str], unit_count: int, hallucinations: list[str], reflection: str = "") -> None
```
**Intent:** Append a new run entry to the memory log, capturing details of the analysis and any hallucinations.

**Inputs:**
- self: RunMemory instance
- repo_path: str — path to the repository
- model: str — model used for analysis
- languages: list[str] — languages involved in the analysis
- unit_count: int — number of units analyzed
- hallucinations: list[str] — hallucinations caught during analysis
- reflection: str — optional reflection notes
**Side effects:**
- Writes to the memory log file

### `_load_blocks` (method)
```
_load_blocks(self) -> list[str]
```
**Intent:** Load and return all memory log blocks from the file.

**Inputs:**
- self: RunMemory instance
**Outputs:**
- list[str] — list of memory log blocks

### `get_past_context` (method)
```
get_past_context(self, repo_path: str, n: int = 3) -> str
```
**Intent:** Retrieve and format lessons from past runs of a specific repository to prevent repeated hallucinations.

**Inputs:**
- self: RunMemory instance
- repo_path: str — path to the repository
- n: int — number of past entries to retrieve
**Outputs:**
- str — formatted lessons from past runs

### `_rotate` (method)
```
_rotate(self, blocks: list[str]) -> list[str]
```
**Intent:** Ensure the memory log does not exceed the maximum number of entries by removing the oldest ones.

**Inputs:**
- self: RunMemory instance
- blocks: list[str] — list of memory log blocks
**Outputs:**
- list[str] — rotated list of memory log blocks

## External dependencies
- os
- __future__
- datetime
- pathlib

## Flagged idioms
- Use of HTML comments as delimiters to ensure safe separation of log entries.
- Atomic file writes using temporary files to prevent data corruption.

## Behavioral notes
- The memory log is append-only and uses a specific delimiter to separate entries.
- The system is designed to be best-effort, meaning it will not raise errors if logging fails.
