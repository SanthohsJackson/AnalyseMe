# apps/x/packages/core/src/auth/provider-client-id.ts

**File:** apps/x/packages/core/src/auth/provider-client-id.ts  
**Language:** typescript

## Purpose
Manage provider client ID overrides using a Map to store, retrieve, check, and clear overrides.

## Interfaces
### `setProviderClientIdOverride` (function)
```
setProviderClientIdOverride(provider: string, clientId: string): void
```
**Intent:** Sets a client ID override for a specific provider if the client ID is not empty after trimming.

**Inputs:**
- provider: string — the provider for which the client ID is set
- clientId: string — the client ID to set for the provider
**Side effects:**
- Modifies the providerClientIdOverrides map by setting a trimmed client ID for the given provider

### `getProviderClientIdOverride` (function)
```
getProviderClientIdOverride(provider: string): string | undefined
```
**Intent:** Retrieves the client ID override for a specific provider.

**Inputs:**
- provider: string — the provider for which to retrieve the client ID
**Outputs:**
- string | undefined — the client ID associated with the provider, or undefined if not set

### `hasProviderClientIdOverride` (function)
```
hasProviderClientIdOverride(provider: string): boolean
```
**Intent:** Checks if a client ID override exists for a specific provider.

**Inputs:**
- provider: string — the provider to check for a client ID override
**Outputs:**
- boolean — true if a client ID override exists for the provider, false otherwise

### `clearProviderClientIdOverride` (function)
```
clearProviderClientIdOverride(provider: string): void
```
**Intent:** Clears the client ID override for a specific provider.

**Inputs:**
- provider: string — the provider for which to clear the client ID override
**Side effects:**
- Modifies the providerClientIdOverrides map by deleting the entry for the given provider

## Flagged idioms
- Use of Map to manage key-value pairs for provider client ID overrides

## Behavioral notes
- Client IDs are trimmed before being set, ensuring no leading or trailing whitespace.
