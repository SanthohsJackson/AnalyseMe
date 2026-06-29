# apps/rowboatx/components/ai-elements/controls.tsx

**File:** apps/rowboatx/components/ai-elements/controls.tsx  
**Language:** typescript

## Purpose
Provide a styled wrapper around the ControlsPrimitive component with additional class names.

## Interfaces
### `Controls` (function)
```
Controls({ className, ...props }: ControlsProps)
```
**Intent:** Render the ControlsPrimitive component with custom styling and additional properties.

**Inputs:**
- className: any — additional class names to apply
- props: ControlsProps — additional properties to pass to ControlsPrimitive

## External dependencies
- @/lib/utils
- @xyflow/react
- react

## Flagged idioms
- Destructuring props to separate className and spread the rest, allowing flexible component customization.

## Behavioral notes
- The cn function is used to concatenate class names, including conditional styles for child buttons.
