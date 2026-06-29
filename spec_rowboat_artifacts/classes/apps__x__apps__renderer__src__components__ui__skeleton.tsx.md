# apps/x/apps/renderer/src/components/ui/skeleton.tsx

**File:** apps/x/apps/renderer/src/components/ui/skeleton.tsx  
**Language:** typescript

## Purpose
Render a skeleton loading component with customizable styles.

## Interfaces
### `Skeleton` (function)
```
Skeleton({ className, ...props }: React.ComponentProps<'div'>)
```
**Intent:** Render a div element styled as a skeleton loader, allowing additional styles and properties to be applied.

**Inputs:**
- className: string — additional CSS classes to apply
- ...props: React.ComponentProps<'div'> — other properties to pass to the div

## External dependencies
- @/lib/utils

## Flagged idioms
- Destructuring props in function parameters to easily pass additional properties to a component.

## Behavioral notes
- The component uses a utility function 'cn' to combine CSS class names.
