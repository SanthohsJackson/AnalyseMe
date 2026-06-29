# cli.py

**File:** cli.py  
**Language:** python

## Purpose
Provide a command-line interface for the Analyse Me pipeline to analyze code repositories and generate language-agnostic specifications.

## Interfaces
### `main` (function)
```
main(repo: str, out: str, provider: str, model: str | None, ollama_url: str, max_parallelism: int, max_files: int | None, skip_tests: bool, analysis_passes: int, thread_id: str | None, langsmith_project: str | None, no_cache: bool, clear_cache: bool)
```
**Intent:** Ingest a codebase and produce a language-agnostic reimplementation spec, handling caching, tracing, and repository resolution.

**Inputs:**
- repo: str — Local path OR git URL to analyze
- out: str — Output file path
- provider: str — LLM provider
- model: str | None — Model id
- ollama_url: str — Ollama base URL
- max_parallelism: int — Max parallel analyze_unit calls
- max_files: int | None — Cap number of source files analyzed
- skip_tests: bool — Skip test files
- analysis_passes: int — Completeness-refinement passes
- thread_id: str | None — Resume a previous run by thread ID
- langsmith_project: str | None — LangSmith project name for tracing
- no_cache: bool — Disable the on-disk LLM response cache
- clear_cache: bool — Delete all cached LLM responses before running
**Raises:**
- SystemExit: when API key environment variable is not set
- SystemExit: when repository cannot be resolved
**Side effects:**
- Sets environment variables for LLM provider and model
- Clears LLM cache if specified
- Prints status and progress messages
- Writes the generated specification to a file

## Internal dependencies
- graph.py
- pipeline/cache.py
- pipeline/memory.py
- pipeline/model_catalog.py
- pipeline/reflection.py
- pipeline/repo_source.py

## External dependencies
- os
- uuid
- click
- pathlib
- langgraph.checkpoint.memory
- graph

## Flagged idioms
- Use of Click for command-line interface parsing and handling
- Environment variable management for configuration

## Behavioral notes
- The function handles both local paths and git URLs for repositories.
- It supports caching and tracing mechanisms for LLM responses.
