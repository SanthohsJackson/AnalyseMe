# apps/rowboat/hooks/use-click-away.ts

**File:** apps/rowboat/hooks/use-click-away.ts  
**Language:** typescript

## Purpose
Provide a hook to handle click-away events for a given DOM element.

## Interfaces
### `useClickAway` (function)
```
useClickAway(ref: RefObject<HTMLElement | null>, handler: (event: MouseEvent | TouchEvent) => void)
```
**Intent:** Detect clicks or touches outside a specified element and trigger a handler function.

**Inputs:**
- ref: RefObject<HTMLElement | null> — a reference to a DOM element
- handler: (event: MouseEvent | TouchEvent) => void — a function to call when a click-away event occurs
**Side effects:**
- Adds and removes event listeners for 'mousedown' and 'touchstart' on the document

## External dependencies
- react

## Flagged idioms
- useEffect: used to manage side effects in functional components, such as adding and removing event listeners

## Behavioral notes
- The handler is not called if the click or touch event occurs within the referenced element.
