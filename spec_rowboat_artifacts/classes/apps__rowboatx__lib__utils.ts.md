# apps/rowboatx/lib/utils.ts

**File:** apps/rowboatx/lib/utils.ts  
**Language:** typescript

## Purpose
Provide a utility function to merge and conditionally apply CSS class names.

## Interfaces
### `cn` (function)
```
cn(...inputs: ClassValue[])
```
**Intent:** Combine multiple class names into a single string, applying conditional logic and merging rules.

**Inputs:**
- inputs: ClassValue[] — a list of class values to be merged and conditionally applied
**Outputs:**
- string — the merged class names

## External dependencies
- clsx
- tailwind-merge

## Flagged idioms
- Use of spread operator to handle variable number of arguments.
