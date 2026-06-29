# Stage: Completeness Review

**Pass:** 2  
**Result:** GAPS — refining

## Questions for the next analysis pass
### pipeline/rag.py
- The code defines 'RAGIndex' but it is not documented anywhere for this file — capture its purpose, inputs, outputs, and side effects.
- Document the side effects of the 'retrieve' method.
- Clarify the outputs of the 'clear' method.

### pipeline/memory.py
- The code defines 'RunMemory' but it is not documented anywhere for this file — capture its purpose, inputs, outputs, and side effects.
- Clarify the outputs of the 'get_past_context' method.

### cli/main.py::PipelineBuffer
- The code defines '_load_env' but it is not documented anywhere for this file — capture its purpose, inputs, outputs, and side effects.
- The code defines 'analyse' but it is not documented anywhere for this file — capture its purpose, inputs, outputs, and side effects.
- The code defines 'analyze' but it is not documented anywhere for this file — capture its purpose, inputs, outputs, and side effects.
- The code defines 'chat' but it is not documented anywhere for this file — capture its purpose, inputs, outputs, and side effects.
- The code defines 'clear_cache_cmd' but it is not documented anywhere for this file — capture its purpose, inputs, outputs, and side effects.
- The code defines 'menu' but it is not documented anywhere for this file — capture its purpose, inputs, outputs, and side effects.
- The code defines 'run_chat' but it is not documented anywhere for this file — capture its purpose, inputs, outputs, and side effects.

### main.py
- Identify and document all functions and classes present in main.py, including their intents, inputs, outputs, and side effects.

### run.sh
- Identify and document all commands and their purposes in run.sh, including any side effects or outputs.

### pipeline/cache.py
- Clarify the outputs of the 'clear' function.
