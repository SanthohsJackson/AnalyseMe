# apps/x/apps/renderer/src/lib/relative-time.ts

**File:** apps/x/apps/renderer/src/lib/relative-time.ts  
**Language:** typescript

## Purpose
Format a timestamp into a compact relative time string for display purposes.

## Interfaces
### `formatRelativeTime` (function)
```
formatRelativeTime(ts: string) -> string
```
**Intent:** Convert a timestamp into a human-readable relative time format like 'just now', '5 m', '3 h', etc., or return an empty string if the timestamp is invalid.

**Inputs:**
- ts: string — the timestamp to format
**Outputs:**
- string — a compact relative time description or an empty string for invalid timestamps

## Behavioral notes
- Returns an empty string for invalid timestamps, allowing callers to handle defaults.
