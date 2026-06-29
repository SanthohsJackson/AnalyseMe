# cli/chat.py

**File:** cli/chat.py  
**Language:** python

## Purpose
Provide an interactive chat interface for querying an indexed code repository using a local LLM.

## Interfaces
### `_format_context` (function)
```
_format_context(docs) -> str
```
**Intent:** Format document contents with metadata labels for display.

**Inputs:**
- docs: iterable — collection of document objects with metadata
**Outputs:**
- str — formatted string of document contents with labels

### `_sources_line` (function)
```
_sources_line(docs) -> str
```
**Intent:** Generate a unique list of document tags from metadata for citation.

**Inputs:**
- docs: iterable — collection of document objects with metadata
**Outputs:**
- str — comma-separated list of unique document tags

### `chat_repl` (function)
```
chat_repl(collection: str, k: int = 8) -> None
```
**Intent:** Run an interactive Q&A loop querying an indexed collection with a local LLM.

**Inputs:**
- collection: str — name of the indexed collection to query
- k: int — number of similar documents to retrieve
**Outputs:**
- None
**Side effects:**
- prints to console
- interacts with a vector database
- calls a local LLM

## Internal dependencies
- pipeline/llm.py
- pipeline/prompts/prompts.py
- pipeline/vectordb.py

## External dependencies
- os
- rich.console
- rich.markdown
- rich.panel
- rich.rule

## Flagged idioms
- use of rich library for console output formatting
- use of try-except for error handling during database operations

## Behavioral notes
- The function chat_repl handles user input and output in a loop until an exit command is given.
- The _format_context function limits the formatted context to 18000 characters before passing to the LLM.
