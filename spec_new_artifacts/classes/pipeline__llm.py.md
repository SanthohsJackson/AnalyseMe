# pipeline/llm.py

**File:** pipeline/llm.py  
**Language:** python

## Purpose
Provide helper functions for interacting with LLMs in a code-to-spec pipeline.

## Interfaces
### `get_provider` (function)
```
get_provider() -> str
```
**Intent:** Retrieve the active LLM provider key from environment variables.

**Outputs:**
- str — the active LLM provider key

### `get_model_id` (function)
```
get_model_id() -> str
```
**Intent:** Resolve the chat model id using environment variables or provider defaults.

**Outputs:**
- str — the resolved chat model id

### `get_llm` (function)
```
get_llm(temperature: float = 0)
```
**Intent:** Instantiate and return an LLM client based on the provider configuration.

**Inputs:**
- temperature: float — the desired temperature setting for the LLM

### `_invoke_with_retry` (function)
```
_invoke_with_retry(llm, messages, max_conn_retries: int = 5)
```
**Intent:** Invoke the LLM with retry logic for transient connection errors.

**Inputs:**
- llm: the LLM client to invoke
- messages: the messages to send to the LLM
- max_conn_retries: int — maximum number of connection retries
**Raises:**
- RuntimeError: when the LLM provider is unreachable after retries
**Side effects:**
- Retries LLM invocation on transient connection errors

### `_extract_json_from_text` (function)
```
_extract_json_from_text(text: str) -> str
```
**Intent:** Extract raw JSON text from a string, removing markdown code fences.

**Inputs:**
- text: str — the text containing JSON
**Outputs:**
- str — the extracted raw JSON text

### `_try_repair_json` (function)
```
_try_repair_json(text: str) -> str
```
**Intent:** Attempt to repair truncated JSON by closing open brackets and braces.

**Inputs:**
- text: str — the potentially truncated JSON text
**Outputs:**
- str — the repaired JSON text

### `call_llm_json` (function)
```
call_llm_json(prompt: str, max_retries: int = 2) -> dict | list
```
**Intent:** Call the LLM and parse a JSON object or array from the response, with caching.

**Inputs:**
- prompt: str — the prompt to send to the LLM
- max_retries: int — maximum number of retries for JSON parsing
**Outputs:**
- dict | list — the parsed JSON object or array
**Raises:**
- ValueError: when valid JSON cannot be obtained after retries
**Side effects:**
- Caches the result of the LLM call

### `_call_llm_json_uncached` (function)
```
_call_llm_json_uncached(prompt: str, max_retries: int = 2) -> dict | list
```
**Intent:** Call the LLM and parse a JSON object or array from the response without caching.

**Inputs:**
- prompt: str — the prompt to send to the LLM
- max_retries: int — maximum number of retries for JSON parsing
**Outputs:**
- dict | list — the parsed JSON object or array
**Raises:**
- ValueError: when valid JSON cannot be obtained after retries

### `call_llm_structured` (function)
```
call_llm_structured(prompt: str, schema, max_retries: int = 2)
```
**Intent:** Call the LLM and return a validated instance of a schema, using structured output.

**Inputs:**
- prompt: str — the prompt to send to the LLM
- schema: the pydantic model schema for validation
- max_retries: int — maximum number of retries
**Side effects:**
- Caches the validated instance of the schema

### `_call_llm_structured_uncached` (function)
```
_call_llm_structured_uncached(prompt: str, schema, max_retries: int = 2)
```
**Intent:** Call the LLM and return a validated instance of a schema without caching.

**Inputs:**
- prompt: str — the prompt to send to the LLM
- schema: the pydantic model schema for validation
- max_retries: int — maximum number of retries

### `call_llm_text` (function)
```
call_llm_text(prompt: str) -> str
```
**Intent:** Call the LLM and return the raw text response, with caching.

**Inputs:**
- prompt: str — the prompt to send to the LLM
**Outputs:**
- str — the raw text response from the LLM
**Side effects:**
- Caches the raw text response

## Internal dependencies
- pipeline/__init__.py
- pipeline/model_catalog.py

## External dependencies
- json
- os
- re
- time
- langchain_core.messages
- langchain_ollama
- langchain_openai

## Flagged idioms
- Use of exponential backoff for retrying LLM invocations on connection errors.
- Use of environment variables to configure LLM provider and model.

## Behavioral notes
- Retries on transient connection errors with exponential backoff.
- Attempts to repair truncated JSON responses before retrying.
