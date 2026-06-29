# pipeline/cache.py

**File:** pipeline/cache.py  
**Language:** python

## Purpose
Provide a content-addressed on-disk cache for deterministic LLM calls.

## Interfaces
### `enabled` (function)
```
enabled() -> bool
```
**Intent:** Check if the cache is enabled based on environment variables.

**Outputs:**
- bool — whether the cache is enabled

### `cache_dir` (function)
```
cache_dir() -> Path
```
**Intent:** Determine and ensure the existence of the cache directory.

**Outputs:**
- Path — the directory path for the cache
**Side effects:**
- Creates the cache directory if it does not exist

### `make_key` (function)
```
make_key(*parts: str) -> str
```
**Intent:** Generate a stable cache key from given parts.

**Inputs:**
- parts: str — components to hash into a key
**Outputs:**
- str — a SHA-256 hash of the input parts

### `get` (function)
```
get(key: str)
```
**Intent:** Retrieve a cached value by its key, if available.

**Inputs:**
- key: str — the cache key to retrieve
**Outputs:**
- The cached value or None if not found
**Side effects:**
- Reads from the cache file system

### `set` (function)
```
set(key: str, value) -> None
```
**Intent:** Store a value in the cache under a specific key.

**Inputs:**
- key: str — the cache key to store under
- value — the JSON-serializable value to cache
**Side effects:**
- Writes to the cache file system

### `clear` (function)
```
clear() -> int
```
**Intent:** Remove all entries from the cache.

**Outputs:**
- int — the number of cache files removed
**Side effects:**
- Deletes cache files from the file system

## External dependencies
- hashlib
- json
- logging
- os
- pathlib

## Flagged idioms
- Use of environment variables to configure behavior
- Atomic file writes to prevent corruption

## Behavioral notes
- Cache is disabled if environment variable LLM_CACHE is set to a disabled value.
- Cache directory defaults to ./.llm_cache but can be overridden with LLM_CACHE_DIR.
- Cache entries are stored as JSON files named by the SHA-256 hash of their key parts.
