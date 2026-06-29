# pipeline/nodes/reduce_modules.py

**File:** pipeline/nodes/reduce_modules.py  
**Language:** python

## Purpose
Group unit analyses by directory and synthesize a ModuleSummary for each group.

## Interfaces
### `reduce_modules` (function)
```
reduce_modules(state: PipelineState) -> dict
```
**Intent:** Groups unit analyses by directory and synthesizes a ModuleSummary for each group.

**Inputs:**
- state: PipelineState — the pipeline state containing unit analyses
**Outputs:**
- dict — a dictionary containing module summaries

## Internal dependencies
- pipeline/llm.py
- pipeline/prompts/prompts.py
- state_schema.py

## External dependencies
- json
- os
- collections

## Flagged idioms
- defaultdict: used to group unit analyses by directory

## Behavioral notes
- The function attempts to call an LLM to generate a responsibility description, falling back to a deterministic description if the call fails.
