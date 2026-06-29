# apps/rowboatx/components/ui/collapsible.tsx

**File:** apps/rowboatx/components/ui/collapsible.tsx  
**Language:** typescript

## Purpose
Provide React components for collapsible UI elements using Radix UI primitives.

## Interfaces
### `Collapsible` (function)
```
Collapsible(props: React.ComponentProps<typeof CollapsiblePrimitive.Root>)
```
**Intent:** Render a collapsible root element using Radix UI's CollapsiblePrimitive.

**Inputs:**
- props: React.ComponentProps<typeof CollapsiblePrimitive.Root> — properties passed to the CollapsiblePrimitive.Root component
**Outputs:**
- JSX.Element — a collapsible root element

### `CollapsibleTrigger` (function)
```
CollapsibleTrigger(props: React.ComponentProps<typeof CollapsiblePrimitive.CollapsibleTrigger>)
```
**Intent:** Render a trigger element for the collapsible component using Radix UI's CollapsiblePrimitive.

**Inputs:**
- props: React.ComponentProps<typeof CollapsiblePrimitive.CollapsibleTrigger> — properties passed to the CollapsiblePrimitive.CollapsibleTrigger component
**Outputs:**
- JSX.Element — a collapsible trigger element

### `CollapsibleContent` (function)
```
CollapsibleContent(props: React.ComponentProps<typeof CollapsiblePrimitive.CollapsibleContent>)
```
**Intent:** Render the content area of a collapsible component using Radix UI's CollapsiblePrimitive.

**Inputs:**
- props: React.ComponentProps<typeof CollapsiblePrimitive.CollapsibleContent> — properties passed to the CollapsiblePrimitive.CollapsibleContent component
**Outputs:**
- JSX.Element — a collapsible content element

## External dependencies
- @radix-ui/react-collapsible

## Flagged idioms
- Spread operator is used to pass all received props to the underlying Radix UI components, allowing for flexible component customization.

## Behavioral notes
- Each component adds a data-slot attribute to the rendered element, which can be used for styling or testing purposes.
