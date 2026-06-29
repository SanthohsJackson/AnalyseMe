# apps/rowboat/lib/utils.ts

**File:** apps/rowboat/lib/utils.ts  
**Language:** typescript

## Purpose
Combine class names using clsx and merge them with Tailwind CSS styles.

## Interfaces
### `cn` (function)
```
cn(...inputs: ClassValue[])
```
**Intent:** Combine and merge class names for use with Tailwind CSS.

**Inputs:**
- inputs: ClassValue[] — a list of class values to be combined and merged
**Outputs:**
- string — the merged class names

## External dependencies
- clsx
- tailwind-merge

## Flagged idioms
- Use of spread operator to handle variable number of arguments.
