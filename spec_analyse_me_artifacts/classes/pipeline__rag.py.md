# pipeline/rag.py

**File:** pipeline/rag.py  
**Language:** python

## Purpose
Facilitate retrieval-augmented generation (RAG) by managing context selection and retrieval from a vector store.

## Interfaces
### `__init__` (method)
```
__init__(self)
```
**Intent:** Initialize the RAGIndex with an in-memory vector store for storing embeddings.

**Side effects:**
- Initializes an in-memory vector store for embeddings

### `add` (method)
```
add(self, items: list[tuple[str, str]]) -> None
```
**Intent:** Add a list of documents to the vector store for future retrieval.

**Inputs:**
- items: list[tuple[str, str]] — list of (id, text) tuples to add to the vector store
**Side effects:**
- Adds documents to the in-memory vector store

### `retrieve` (method)
```
retrieve(self, query: str, k: int)
```
**Intent:** Retrieve the top-k documents from the vector store that are most similar to the query.

**Inputs:**
- query: str — the search query
- k: int — number of top results to retrieve
**Outputs:**
- list of documents matching the query

### `select_context` (function)
```
select_context(full_text: str, records: list[dict], query: str, char_budget: int = RAG_CHAR_BUDGET, k: int = 12) -> tuple[str, bool]
```
**Intent:** Select the appropriate context for a node, using full text if within budget or retrieving relevant items otherwise.

**Inputs:**
- full_text: str — the complete text to consider for context
- records: list[dict] — list of records with 'id', 'full', and 'compact' fields
- query: str — the search query for retrieval
- char_budget: int — maximum character budget for context
- k: int — number of top results to retrieve
**Outputs:**
- tuple[str, bool] — context text and a flag indicating if RAG was used
**Raises:**
- Exception: when embeddings/store are unavailable

## Internal dependencies
- pipeline/vectordb.py

## External dependencies
- os
- __future__
- langchain_core.vectorstores
- langchain_core.documents

## Flagged idioms
- Use of in-memory vector store for efficient retrieval without a database

## Behavioral notes
- Switches to retrieval mode when character budget is exceeded.
- Degrades gracefully to a compact view if embeddings are unavailable.
