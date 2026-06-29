# pipeline/vectordb.py

**File:** pipeline/vectordb.py  
**Language:** python

## Purpose
Provide a vector store interface for RAG over a codebase using pgvector and Ollama embeddings.

## Interfaces
### `get_conn_string` (function)
```
get_conn_string() -> str
```
**Intent:** Retrieve the PostgreSQL connection string from environment variables or use a default.

**Outputs:**
- str — the connection string for the PostgreSQL database

### `get_embeddings` (function)
```
get_embeddings()
```
**Intent:** Determine and return the appropriate embeddings provider based on environment variables.

**Outputs:**
- Embeddings object — either OpenAIEmbeddings or OllamaEmbeddings

### `collection_for` (function)
```
collection_for(repo_path: str) -> str
```
**Intent:** Generate a unique collection name for a repository based on its path.

**Inputs:**
- repo_path: str — the path to the repository
**Outputs:**
- str — a stable, unique collection name

### `get_store` (function)
```
get_store(collection: str, embed_meta: dict | None = None)
```
**Intent:** Return a PGVector store for a given collection, creating it if necessary.

**Inputs:**
- collection: str — the name of the collection
- embed_meta: dict | None — metadata about the embeddings
**Outputs:**
- PGVector — the vector store for the collection

### `_provider_from_dim` (function)
```
_provider_from_dim(dim: int) -> dict | None
```
**Intent:** Map an embedding dimension to a likely provider and model.

**Inputs:**
- dim: int — the dimension of the embedding
**Outputs:**
- dict | None — provider and model information

### `collection_embed_config` (function)
```
collection_embed_config(collection: str) -> dict | None
```
**Intent:** Determine the embeddings configuration for a collection, using metadata or vector dimensions.

**Inputs:**
- collection: str — the name of the collection
**Outputs:**
- dict | None — provider and model information
**Raises:**
- Exception: when database operations fail

### `_raw_conn_string` (function)
```
_raw_conn_string() -> str
```
**Intent:** Convert the connection string to a format suitable for psycopg.

**Outputs:**
- str — the raw connection string for psycopg

### `check_connection` (function)
```
check_connection() -> tuple[bool, str]
```
**Intent:** Check the database connection and provide diagnostics if unreachable.

**Outputs:**
- tuple[bool, str] — connection status and message
**Raises:**
- Exception: when database connection fails

### `list_collections` (function)
```
list_collections() -> list[str]
```
**Intent:** List existing collections in the database, optionally with row counts.

**Outputs:**
- list[str] — names of existing collections
**Raises:**
- Exception: when database operations fail

## External dependencies
- hashlib
- os
- re
- psycopg
- __future__
- langchain_openai
- langchain_ollama
- langchain_postgres

## Flagged idioms
- Use of environment variables to configure behavior
- Use of hashlib for generating unique identifiers

## Behavioral notes
- The connection string defaults to a local PostgreSQL instance if not set in the environment.
- Embeddings default to Ollama if no provider is specified.
