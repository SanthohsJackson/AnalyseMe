# apps/rowboatx/components/ui/skeleton.tsx

**File:** apps/rowboatx/components/ui/skeleton.tsx  
**Language:** typescript

## Purpose
Render a skeleton loading component with customizable styles.

## Interfaces
### `Skeleton` (function)
```
Skeleton({ className, ...props }: React.ComponentProps<'div'>)
```
**Intent:** Provide a visual placeholder for content that is loading, using a pulsing animation and customizable styles.

**Inputs:**
- className: string — additional CSS classes to apply
- ...props: React.ComponentProps<'div'> — additional properties for the div element
**Side effects:**
- Renders a div element with specified properties and styles

## External dependencies
- @/lib/utils

## Flagged idioms
- React component pattern: using props to pass down attributes and styles to a div element

## Behavioral notes
- The component uses a pulsing animation to indicate loading state.
