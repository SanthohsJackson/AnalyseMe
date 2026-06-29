# apps/x/packages/core/src/config/rowboat.ts

**File:** apps/x/packages/core/src/config/rowboat.ts  
**Language:** typescript

## Purpose
Fetch and cache the Rowboat API configuration.

## Interfaces
### `getRowboatConfig` (function)
```
getRowboatConfig() -> Promise<z.infer<typeof RowboatApiConfig>>
```
**Intent:** Retrieve the Rowboat API configuration from a remote source and cache it for future use.

**Outputs:**
- Promise<z.infer<typeof RowboatApiConfig>> — the parsed configuration data
**Side effects:**
- network: fetches configuration from an external API
- global state: updates the cached variable

## Internal dependencies
- ./env.js

## External dependencies
- zod
- @x/shared/dist/rowboat-account.js

## Flagged idioms
- Caching: uses a global variable to store the fetched configuration to avoid redundant network requests.

## Behavioral notes
- The function fetches data only if it is not already cached.
