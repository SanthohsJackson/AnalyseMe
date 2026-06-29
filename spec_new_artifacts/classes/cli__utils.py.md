# cli/utils.py

**File:** cli/utils.py  
**Language:** python

## Purpose
Provide a set of interactive prompts for configuring a repository analysis pipeline.

## Interfaces
### `ask_repo_path` (function)
```
ask_repo_path() -> str
```
**Intent:** Prompt the user for a repository path or URL and validate the input.

**Outputs:**
- str — the validated repository path or URL
**Side effects:**
- Exits the program if no repository is provided

### `_valid` (function)
```
_valid(val: str) -> bool | str
```
**Intent:** Validate whether the input is a valid directory path or git URL.

**Inputs:**
- val: str — the input value to validate
**Outputs:**
- bool | str — True if valid, error message if not

### `ask_output_file` (function)
```
ask_output_file() -> str
```
**Intent:** Prompt the user for the name of the output file, defaulting to 'spec.md'.

**Outputs:**
- str — the name of the output file

### `ask_provider` (function)
```
ask_provider() -> str
```
**Intent:** Prompt the user to select an LLM provider from a list of available options.

**Outputs:**
- str — the selected LLM provider

### `ask_model` (function)
```
ask_model(provider: str) -> str
```
**Intent:** Prompt the user to select a model for the given provider, with options for custom input.

**Inputs:**
- provider: str — the selected LLM provider
**Outputs:**
- str — the selected model for the provider
**Side effects:**
- Warns if the provider's API key is missing

### `ask_ollama_model` (function)
```
ask_ollama_model() -> str
```
**Intent:** Fetch and prompt the user to select an Ollama model, with an option for custom input.

**Outputs:**
- str — the selected Ollama model

### `ask_max_files` (function)
```
ask_max_files() -> int | None
```
**Intent:** Prompt the user to set a file cap for limiting LLM calls on large repositories.

**Outputs:**
- int | None — the file cap or None for no cap

### `ask_skip_tests` (function)
```
ask_skip_tests() -> bool
```
**Intent:** Prompt the user to decide whether to skip test files during analysis.

**Outputs:**
- bool — whether to skip test files

### `ask_analysis_passes` (function)
```
ask_analysis_passes() -> int
```
**Intent:** Prompt the user to specify the number of analysis refinement passes.

**Outputs:**
- int — the number of analysis refinement passes

## Internal dependencies
- pipeline/model_catalog.py
- pipeline/repo_source.py

## External dependencies
- os
- questionary
- requests
- pathlib
- rich.console

## Flagged idioms
- Use of questionary for interactive CLI prompts
- Use of rich.console for styled console output

## Behavioral notes
- ask_repo_path exits the program if no input is provided.
- ask_model warns if the provider's API key is missing.
