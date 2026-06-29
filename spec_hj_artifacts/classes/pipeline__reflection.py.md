# pipeline/reflection.py

**File:** pipeline/reflection.py  
**Language:** python

## Purpose
Generate a concise reflection on a completed spec run for future reference.

## Interfaces
### `reflect_on_run` (function)
```
reflect_on_run(repo_name: str, languages: list[str], unit_count: int, hallucinations: list[str]) -> str
```
**Intent:** Create a brief, plain-text reflection on the analysis of a code repository, highlighting key aspects and lessons for future runs.

**Inputs:**
- repo_name: str — the name of the repository being analyzed
- languages: list[str] — the programming languages used in the repository
- unit_count: int — the number of units analyzed
- hallucinations: list[str] — a list of hallucinations identified during the analysis
**Outputs:**
- str — a concise reflection or an empty string on failure

## Internal dependencies
- pipeline/llm.py

## Flagged idioms
- Use of f-strings for prompt construction — enhances readability and maintainability of string formatting.

## Behavioral notes
- Returns an empty string if an exception occurs during the call to call_llm_text.
