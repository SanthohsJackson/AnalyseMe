# apps/rowboat/components/ui/horizontal-divider.tsx

**File:** apps/rowboat/components/ui/horizontal-divider.tsx  
**Language:** typescript

## Purpose
Render a horizontal divider with optional custom styling.

## Interfaces
### `HorizontalDivider` (function)
```
HorizontalDivider({ className }: HorizontalDividerProps)
```
**Intent:** Render a styled horizontal divider with optional additional CSS classes.

**Inputs:**
- className: string — optional additional CSS classes for styling
**Outputs:**
- JSX.Element — a styled div element

### `HorizontalDividerProps` (class)
```
interface HorizontalDividerProps
```
**Intent:** Define the properties for the HorizontalDivider component.

**Inputs:**
- className?: string — optional CSS class names

## External dependencies
- clsx

## Flagged idioms
- Use of clsx for conditional className concatenation: simplifies dynamic class name management.
