# apps/x/apps/renderer/src/hooks/use-mobile.ts

**File:** apps/x/apps/renderer/src/hooks/use-mobile.ts  
**Language:** typescript

## Purpose
Determine if the current window width is below a mobile breakpoint.

## Interfaces
### `useIsMobile` (function)
```
useIsMobile() -> boolean
```
**Intent:** Provide a boolean indicating whether the current window width is considered mobile.

**Outputs:**
- boolean — true if the window width is less than the mobile breakpoint, false otherwise
**Side effects:**
- Registers and unregisters an event listener on the window's matchMedia object

## External dependencies
- react

## Flagged idioms
- React useEffect: used to manage side effects such as event listeners in functional components

## Behavioral notes
- The function returns false if the window width is exactly equal to the mobile breakpoint.
