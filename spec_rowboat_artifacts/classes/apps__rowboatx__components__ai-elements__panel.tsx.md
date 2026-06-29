# apps/rowboatx/components/ai-elements/panel.tsx

**File:** apps/rowboatx/components/ai-elements/panel.tsx  
**Language:** typescript

## Purpose
Define a Panel component that wraps a primitive panel with additional styling.

## Interfaces
### `Panel` (function)
```
Panel({ className, ...props }: PanelProps)
```
**Intent:** Render a styled panel component by combining additional class names with a primitive panel component.

**Inputs:**
- className: any — additional class names to apply
- ...props: any — other properties to pass to the PanelPrimitive
**Outputs:**
- JSX.Element — a styled panel component

## External dependencies
- @/lib/utils
- @xyflow/react
- react

## Flagged idioms
- Spread operator: used to pass additional props to the PanelPrimitive component

## Behavioral notes
- The cn function is used to combine class names, which suggests a utility for conditional class name application.
