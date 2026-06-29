# apps/rowboat/app/styles/pane-effects.ts

**File:** apps/rowboat/app/styles/pane-effects.ts  
**Language:** typescript

## Purpose
Generate a list of CSS classes based on the active state of elements.

## Interfaces
### `getPaneClasses` (function)
```
getPaneClasses(isActive: boolean, otherIsActive: boolean) => string[]
```
**Intent:** Determine the CSS classes to apply to a pane based on its active state and the active state of another pane.

**Inputs:**
- isActive: boolean — indicates if the current pane is active
- otherIsActive: boolean — indicates if another pane is active
**Outputs:**
- string[] — array of CSS class strings
