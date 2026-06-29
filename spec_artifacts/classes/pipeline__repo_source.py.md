# pipeline/repo_source.py

**File:** pipeline/repo_source.py  
**Language:** python

## Purpose
Resolve a repository source to a local directory, handling both local paths and git URLs.

## Interfaces
### `is_git_url` (function)
```
is_git_url(source: str) -> bool
```
**Intent:** Determine if a given source string is a valid git URL.

**Inputs:**
- source: str — the source string to check
**Outputs:**
- bool — True if the source is a git URL, False otherwise

### `_clone_dir_name` (function)
```
_clone_dir_name(url: str) -> str
```
**Intent:** Generate a stable directory name from a git URL for cloning purposes.

**Inputs:**
- url: str — the git URL to process
**Outputs:**
- str — a stable, filesystem-safe directory name derived from the URL

### `_normalize_url` (function)
```
_normalize_url(url: str) -> str
```
**Intent:** Normalize a git URL, converting shorthand forms to full URLs.

**Inputs:**
- url: str — the URL to normalize
**Outputs:**
- str — the normalized URL

### `resolve_repo_source` (function)
```
resolve_repo_source(source: str, log=print, force_fresh: bool = False) -> str
```
**Intent:** Resolve a source to a local directory, cloning git URLs if necessary.

**Inputs:**
- source: str — the source to resolve
- log: callable — function to log messages
- force_fresh: bool — whether to force a fresh clone
**Outputs:**
- str — the local directory path for the resolved source
**Raises:**
- ValueError: when the source is neither a directory nor a recognized git URL
- RuntimeError: when git clone fails
**Side effects:**
- Creates directories under ~/.code-to-spec/clones
- May remove existing directories if force_fresh is True
- Runs git commands to clone or update repositories

## External dependencies
- re
- subprocess
- shutil
- __future__
- pathlib

## Flagged idioms
- Use of regular expressions to match and validate git URLs
- Use of subprocess to execute shell commands for git operations

## Behavioral notes
- The function resolve_repo_source will reuse existing clones unless force_fresh is True.
- The function _clone_dir_name ensures directory names are stable and filesystem-safe.
