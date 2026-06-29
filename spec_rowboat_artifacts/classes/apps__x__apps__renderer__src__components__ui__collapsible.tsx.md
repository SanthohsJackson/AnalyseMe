# apps/x/apps/renderer/src/components/ui/collapsible.tsx

**File:** apps/x/apps/renderer/src/components/ui/collapsible.tsx  
**Language:** typescript

## Purpose
Provide collapsible UI components using Radix UI's Collapsible primitives.

## Interfaces
### `Collapsible` (function)
```
Collapsible(props: React.ComponentProps<typeof CollapsiblePrimitive.Root>)
```
**Intent:** Render a collapsible root component with the given properties.

**Inputs:**
- props: React.ComponentProps<typeof CollapsiblePrimitive.Root> — properties passed to the Collapsible component
**Outputs:**
- JSX.Element — a Collapsible component

### `CollapsibleTrigger` (function)
```
CollapsibleTrigger(props: React.ComponentProps<typeof CollapsiblePrimitive.CollapsibleTrigger>)
```
**Intent:** Render a trigger component for the collapsible with the given properties.

**Inputs:**
- props: React.ComponentProps<typeof CollapsiblePrimitive.CollapsibleTrigger> — properties passed to the CollapsibleTrigger component
**Outputs:**
- JSX.Element — a CollapsibleTrigger component

### `CollapsibleContent` (function)
```
CollapsibleContent(props: React.ComponentProps<typeof CollapsiblePrimitive.CollapsibleContent>)
```
**Intent:** Render the content area of a collapsible component with the given properties.

**Inputs:**
- props: React.ComponentProps<typeof CollapsiblePrimitive.CollapsibleContent> — properties passed to the CollapsibleContent component
**Outputs:**
- JSX.Element — a CollapsibleContent component

## External dependencies
- @radix-ui/react-collapsible

## Flagged idioms
- Spread operator is used to pass all received props to the underlying component, allowing for flexible prop management.

## Behavioral notes
- Each component adds a data-slot attribute to the rendered element, which can be used for styling or testing purposes.
