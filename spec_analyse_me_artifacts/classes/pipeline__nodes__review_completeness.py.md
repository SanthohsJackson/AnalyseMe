# pipeline/nodes/review_completeness.py

**File:** pipeline/nodes/review_completeness.py  
**Language:** python

## Purpose
Review the completeness of unit analyses by identifying structural gaps and performing a qualitative review.

## Interfaces
### `review_completeness` (function)
```
review_completeness(state: PipelineState) -> dict
```
**Intent:** Identify missing interfaces and empty intents in unit analyses, and generate questions for further analysis.

**Inputs:**
- state: PipelineState — the current state of the pipeline including unit analyses and repo path
**Outputs:**
- dict — containing analysis questions, completeness status, and pass number

## Internal dependencies
- pipeline/llm.py
- pipeline/parsers/tree_sitter_parser.py
- pipeline/prompts/prompts.py
- state_schema.py

## External dependencies
- json
- os
- collections

## Flagged idioms
- Use of defaultdict to group unit analyses by file path for comparison.

## Behavioral notes
- The function increments the analysis pass count each time it is called.
- It handles exceptions during LLM calls gracefully, ensuring deterministic gaps are still addressed.
