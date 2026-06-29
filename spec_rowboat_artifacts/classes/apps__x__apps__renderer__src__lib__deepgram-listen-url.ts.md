# apps/x/apps/renderer/src/lib/deepgram-listen-url.ts

**File:** apps/x/apps/renderer/src/lib/deepgram-listen-url.ts  
**Language:** typescript

## Purpose
Construct a Deepgram WebSocket URL with query parameters.

## Interfaces
### `buildDeepgramListenUrl` (function)
```
buildDeepgramListenUrl(baseWsUrl: string, params: URLSearchParams) -> string
```
**Intent:** Combine a base WebSocket URL with Deepgram-specific query parameters to form a complete URL.

**Inputs:**
- baseWsUrl: string — the base WebSocket URL
- params: URLSearchParams — query parameters to append
**Outputs:**
- string — the complete URL with query parameters

## Flagged idioms
- Use of URL and URLSearchParams to manipulate and construct URLs.
