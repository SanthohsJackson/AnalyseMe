# pipeline/indexer.py

**File:** pipeline/indexer.py  
**Language:** python

## Purpose
Index a completed run into a vector database for retrieval-augmented generation (RAG).

## Interfaces
### `_chunk` (function)
```
_chunk(text: str, size: int = 1400, overlap: int = 150) -> list[str]
```
**Intent:** Split a given text into chunks of a specified size with overlap to facilitate processing without external dependencies.

**Inputs:**
- text: str — the text to be chunked
- size: int — the maximum size of each chunk
- overlap: int — the number of overlapping characters between chunks
**Outputs:**
- list[str] — list of text chunks

### `_split_spec_sections` (function)
```
_split_spec_sections(spec: str) -> list[tuple[str, str]]
```
**Intent:** Divide a specification document into sections based on top-level headings for structured processing.

**Inputs:**
- spec: str — the specification text to be split
**Outputs:**
- list[tuple[str, str]] — list of tuples containing section titles and bodies

### `index_run` (function)
```
index_run(repo_path: str, class_docs: dict[str, str], spec_text: str, log=print) -> tuple[str, int]
```
**Intent:** Embed and store code and specifications from a repository into a vector database for later retrieval.

**Inputs:**
- repo_path: str — the path to the repository
- class_docs: dict[str, str] — dictionary of class documentation
- spec_text: str — the specification text
- log: callable — logging function, defaults to print
**Outputs:**
- tuple[str, int] — the collection name and document count
**Side effects:**
- Reads files from the filesystem
- Logs messages
- Interacts with a vector database

## Internal dependencies
- pipeline/vectordb.py

## External dependencies
- os
- re
- langchain_core.documents

## Flagged idioms
- Use of environment variables to configure embedding provider and model
- Chunking text with overlap to ensure continuity across boundaries

## Behavioral notes
- The function index_run reads files directly from the filesystem, which may fail if files are missing or inaccessible.
- The embedding provider and model are determined by environment variables, allowing for flexible configuration.
