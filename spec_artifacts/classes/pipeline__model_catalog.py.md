# pipeline/model_catalog.py

**File:** pipeline/model_catalog.py  
**Language:** python

## Purpose
Manage and provide configurations for different model providers and their options.

## Interfaces
### `list_providers` (function)
```
list_providers() -> list[tuple[str, str]]
```
**Intent:** Retrieve a list of available model providers and their display labels.

**Outputs:**
- list[tuple[str, str]] — list of provider keys and their labels

### `provider_config` (function)
```
provider_config(provider: str) -> dict
```
**Intent:** Fetch the configuration for a specified provider, defaulting to 'ollama' if not found.

**Inputs:**
- provider: str — the key of the provider to retrieve configuration for
**Outputs:**
- dict — configuration details of the specified provider

### `get_model_options` (function)
```
get_model_options(provider: str) -> list[tuple[str, str]]
```
**Intent:** Retrieve available model options for a given provider.

**Inputs:**
- provider: str — the key of the provider to retrieve model options for
**Outputs:**
- list[tuple[str, str]] — list of model options for the specified provider

### `default_model` (function)
```
default_model(provider: str) -> str
```
**Intent:** Get the default model identifier for a specified provider.

**Inputs:**
- provider: str — the key of the provider to retrieve the default model for
**Outputs:**
- str — default model identifier for the specified provider

## External dependencies
- __future__

## Flagged idioms
- Use of dictionary to map provider keys to their configurations and options.

## Behavioral notes
- The function 'provider_config' defaults to 'ollama' configuration if the specified provider is not found.
