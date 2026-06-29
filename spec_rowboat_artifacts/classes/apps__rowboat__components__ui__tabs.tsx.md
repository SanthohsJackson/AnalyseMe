# apps/rowboat/components/ui/tabs.tsx

**File:** apps/rowboat/components/ui/tabs.tsx  
**Language:** typescript

## Purpose
Provide a React component wrapper for HeroTabs with additional class name handling.

## Interfaces
### `Tabs` (function)
```
Tabs: React.ForwardRefExoticComponent<React.ComponentPropsWithoutRef<typeof HeroTabs> & React.RefAttributes<HTMLDivElement>>
```
**Intent:** Wrap the HeroTabs component to allow additional class names and ref forwarding.

**Inputs:**
- className: string — additional class names to apply
- props: React.ComponentPropsWithoutRef<typeof HeroTabs> — props to pass to HeroTabs
- ref: React.Ref<HTMLDivElement> — ref to be forwarded to the HeroTabs component

## Internal dependencies
- ../../lib/utils

## External dependencies
- react
- @heroui/react

## Flagged idioms
- React.forwardRef: used to forward refs to the underlying HeroTabs component, allowing parent components to access the DOM node.

## Behavioral notes
- The cn function is used to concatenate class names, ensuring 'w-full' is always applied.
