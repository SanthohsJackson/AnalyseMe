# apps/rowboat/app/loading.tsx

**File:** apps/rowboat/app/loading.tsx  
**Language:** typescript

## Purpose
Render a loading spinner while user data is being fetched.

## Interfaces
### `Loading` (function)
```
Loading()
```
**Intent:** Display a spinner to indicate loading state during data fetching.

**Outputs:**
- JSX.Element — a small spinner component

## External dependencies
- @heroui/react

## Flagged idioms
- React Suspense: used for handling asynchronous data fetching by showing a fallback UI.

## Behavioral notes
- The component is intended to be used with React Suspense for loading states.
