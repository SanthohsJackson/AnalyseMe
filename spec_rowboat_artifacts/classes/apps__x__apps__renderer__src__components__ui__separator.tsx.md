# apps/x/apps/renderer/src/components/ui/separator.tsx

**File:** apps/x/apps/renderer/src/components/ui/separator.tsx  
**Language:** typescript

## Purpose
Render a styled separator component using Radix UI's SeparatorPrimitive.

## Interfaces
### `Separator` (function)
```
Separator({ className, orientation = 'horizontal', decorative = true, ...props }: React.ComponentProps<typeof SeparatorPrimitive.Root>)
```
**Intent:** Render a customizable separator line that can be oriented horizontally or vertically.

**Inputs:**
- className: string — additional CSS classes to apply
- orientation: string — the orientation of the separator, defaults to 'horizontal'
- decorative: boolean — whether the separator is purely decorative, defaults to true
- ...props: React.ComponentProps<typeof SeparatorPrimitive.Root> — additional props passed to the SeparatorPrimitive.Root component
**Outputs:**
- JSX.Element — a styled separator component

## Internal dependencies
- @/lib/utils

## External dependencies
- react
- @radix-ui/react-separator

## Flagged idioms
- Destructuring with default values: provides default values for orientation and decorative properties.

## Behavioral notes
- The className is combined with default styles using the cn utility function.
