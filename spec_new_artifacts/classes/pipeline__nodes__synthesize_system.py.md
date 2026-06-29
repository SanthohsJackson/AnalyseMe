# pipeline/nodes/synthesize_system.py

**File:** pipeline/nodes/synthesize_system.py  
**Language:** python

## Purpose
Generate a system-level overview from module summaries within a pipeline.

## Interfaces
### `synthesize_system` (function)
```
synthesize_system(state: PipelineState) -> dict
```
**Intent:** Aggregate module summaries into a comprehensive system overview using a language model.

**Inputs:**
- state: PipelineState — the current state containing module summaries and repo path
**Outputs:**
- dict — containing the system overview as 'system_overview'

## Internal dependencies
- pipeline/llm.py
- pipeline/prompts/prompts.py
- pipeline/rag.py
- state_schema.py

## External dependencies
- json
- os
- state_schema

## Flagged idioms
- Use of list comprehensions for data transformation
- JSON serialization for structured data representation

## Behavioral notes
- The function uses a language model to generate the system overview based on a formatted prompt.
