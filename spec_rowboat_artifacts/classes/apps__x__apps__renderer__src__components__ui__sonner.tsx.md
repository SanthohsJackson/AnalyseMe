# apps/x/apps/renderer/src/components/ui/sonner.tsx

**File:** apps/x/apps/renderer/src/components/ui/sonner.tsx  
**Language:** typescript

## Purpose
Provide a customized toaster component using icons from lucide-react and styles from sonner.

## Interfaces
### `Toaster` (function)
```
Toaster(props: ToasterProps)
```
**Intent:** Render a toaster component with specific icons and styles for different notification types.

**Inputs:**
- props: ToasterProps — properties to pass to the Sonner component

## External dependencies
- lucide-react
- sonner

## Flagged idioms
- Spread operator in props: allows passing all received props to the Sonner component.

## Behavioral notes
- The component uses CSS variables for styling, which allows for easy theming and customization.
