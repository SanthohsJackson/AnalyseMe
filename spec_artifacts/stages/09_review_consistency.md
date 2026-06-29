# Stage: Consistency Review (anti-hallucination)

**Result:** FINDINGS ✗

## Findings
- HALLUCINATION: 'RAGIndex', 'RunMemory', various functions for repository resolution, LLM interaction, and output rendering' in pipeline interfaces — not present in ground truth
- HALLUCINATION: 'Functions for traversing ASTs and extracting class spans' in pipeline/parsers interfaces — not present in ground truth
- HALLUCINATION: 'PipelineBuffer', various functions for user input and pipeline management' in cli interfaces — not present in ground truth
- HALLUCINATION: 'DataSchema' in Data Schemas — not present in ground truth
- HALLUCINATION: 'Semaphore-based approaches' for concurrency — not present in ground truth
- HALLUCINATION: 'Provider configuration functions and prompt templates' for config — not present in ground truth
- HALLUCINATION: 'Memory logging' for logging — not present in ground truth
- HALLUCINATION: 'Tree-sitter for parsing' in integrations — not present in ground truth
- HALLUCINATION: 'Language models for validation and analysis' in integrations — not present in ground truth