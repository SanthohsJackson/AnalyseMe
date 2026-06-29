# apps/rowboatx/components/ui/progress.tsx

**File:** apps/rowboatx/components/ui/progress.tsx  
**Language:** typescript

## Purpose
Render a progress bar component using Radix UI's Progress primitives.

## Interfaces
### `Progress` (function)
```
Progress({ className, value, ...props }: React.ComponentProps<typeof ProgressPrimitive.Root>)
```
**Intent:** Render a progress bar with a customizable appearance and progress value.

**Inputs:**
- className: string — additional CSS classes to apply
- value: number — the current progress value
- ...props: React.ComponentProps<typeof ProgressPrimitive.Root> — additional properties for the ProgressPrimitive.Root component

## Internal dependencies
- @/lib/utils

## External dependencies
- react
- @radix-ui/react-progress

## Flagged idioms
- Destructuring props to pass additional properties to a component, allowing for flexible component customization.

## Behavioral notes
- The progress indicator's position is dynamically set using inline styles based on the 'value' prop.
