# apps/x/apps/renderer/src/lib/google-credentials-store.ts

**File:** apps/x/apps/renderer/src/lib/google-credentials-store.ts  
**Language:** typescript

## Purpose
Manage Google credentials by storing, retrieving, and clearing them.

## Interfaces
### `getGoogleCredentials` (function)
```
getGoogleCredentials() -> GoogleCredentials | null
```
**Intent:** Retrieve the currently stored Google credentials.

**Outputs:**
- GoogleCredentials | null — the current stored credentials or null if none are set

### `setGoogleCredentials` (function)
```
setGoogleCredentials(clientId: string, clientSecret: string) -> void
```
**Intent:** Store new Google credentials if both clientId and clientSecret are provided and non-empty.

**Inputs:**
- clientId: string — the Google client ID
- clientSecret: string — the Google client secret
**Side effects:**
- Updates the global credentials variable with new values if both are non-empty after trimming

### `clearGoogleCredentials` (function)
```
clearGoogleCredentials() -> void
```
**Intent:** Clear the stored Google credentials.

**Side effects:**
- Sets the global credentials variable to null

## Flagged idioms
- Use of a global variable to store state across function calls

## Behavioral notes
- The setGoogleCredentials function trims whitespace from inputs before storing them.
