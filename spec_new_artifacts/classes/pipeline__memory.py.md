# pipeline/memory.py

**File:** pipeline/memory.py  
**Language:** python

## Purpose
Manage and persistently store cross-run memory logs for code-to-spec analysis, focusing on hallucination tracking.

## Interfaces
### `RunMemory` (class)
```
RunMemory(path: str | os.PathLike | None = None, max_entries: int | None = 50)
```
**Intent:** Initialize a RunMemory instance with a specified log file path and maximum entry count.

**Inputs:**
- path: str | os.PathLike | None — the file path for storing memory logs
- max_entries: int | None — maximum number of entries to retain

### `__init__` (method)
```
__init__(self, path: str | os.PathLike | None = None, max_entries: int | None = 50) -> None
```
**Intent:** Set up the RunMemory instance with a path for the log file and a limit on the number of entries.

**Inputs:**
- path: str | os.PathLike | None — the file path for storing memory logs
- max_entries: int | None — maximum number of entries to retain

### `store_run` (method)
```
store_run(self, repo_path: str, model: str, languages: list[str], unit_count: int, hallucinations: list[str], reflection: str = "") -> None
```
**Intent:** Append a new run entry to the memory log, capturing details of the analysis and any hallucinations.

**Inputs:**
- repo_path: str — path to the repository
- model: str — model used for analysis
- languages: list[str] — languages involved in the analysis
- unit_count: int — number of units analyzed
- hallucinations: list[str] — list of hallucinations caught
- reflection: str — optional reflection notes
**Raises:**
- OSError: when file operations fail
**Side effects:**
- Writes to the memory log file

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
**Intent:** Retrieve and format lessons from past runs of a specific repository to prevent repeated hallucinations.

**Inputs:**
- repo_path: str — path to the repository
- n: int — number of past entries to retrieve
**Outputs:**
- str — formatted lessons from past runs

### `_rotate` (method)
```
_rotate(self, blocks: list[str]) -> list[str]
```
**Intent:** Ensure the log does not exceed the maximum number of entries by removing the oldest ones.

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
- Use of Path from pathlib for file path operations, ensuring cross-platform compatibility.
- Atomic file write using a temporary file and replace to prevent data corruption.

## Behavioral notes
- The memory log is append-only and uses a specific HTML comment as a delimiter to separate entries.
- The system is designed to be best-effort, meaning it will not interrupt the main process if logging fails.
