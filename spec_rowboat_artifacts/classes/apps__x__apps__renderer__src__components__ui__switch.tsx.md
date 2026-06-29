# apps/x/apps/renderer/src/components/ui/switch.tsx

**File:** apps/x/apps/renderer/src/components/ui/switch.tsx  
**Language:** typescript

## Purpose
Render a customizable switch component using Radix UI's SwitchPrimitive.

## Interfaces
### `Switch` (function)
```
Switch({ className, ...props }: React.ComponentProps<typeof SwitchPrimitive.Root>)
```
**Intent:** Render a switch component with customizable styles and behavior, leveraging Radix UI's SwitchPrimitive.

**Inputs:**
- className: any — additional class names for styling
- ...props: any — additional properties passed to the SwitchPrimitive.Root component

## Internal dependencies
- @/lib/utils

## External dependencies
- react
- @radix-ui/react-switch

## Flagged idioms
- Spread operator: used to pass additional props to the component.

## Behavioral notes
- The component uses conditional class names based on the switch's state (checked/unchecked).
