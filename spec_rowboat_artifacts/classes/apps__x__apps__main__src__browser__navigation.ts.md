# apps/x/apps/main/src/browser/navigation.ts

**File:** apps/x/apps/main/src/browser/navigation.ts  
**Language:** typescript

## Purpose
Normalize a navigation target string into a valid URL or search query.

## Interfaces
### `normalizeNavigationTarget` (function)
```
normalizeNavigationTarget(target: string) -> string
```
**Intent:** Ensure the navigation target is a valid URL or convert it into a search query URL if it lacks a scheme.

**Inputs:**
- target: string — the navigation target to normalize
**Outputs:**
- string — a valid URL or search query URL
**Raises:**
- Error: when the target is empty or uses a disallowed URL scheme

## Flagged idioms
- Regular expressions are used to validate and identify URL patterns.

## Behavioral notes
- The function throws an error for empty targets or disallowed schemes like 'javascript:'.
- If the target looks like a host and lacks a scheme, 'http://' or 'https://' is prepended based on the host type.
- Targets not matching any URL pattern are converted into a Google search query URL.
