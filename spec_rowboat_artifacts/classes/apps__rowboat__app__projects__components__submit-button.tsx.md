# apps/rowboat/app/projects/components/submit-button.tsx

**File:** apps/rowboat/app/projects/components/submit-button.tsx  
**Language:** typescript

## Purpose
Render a submit button with a loading state for a form in a React component.

## Interfaces
### `Submit` (function)
```
Submit()
```
**Intent:** Display a submit button that shows a loading message when a form is pending submission.

**Side effects:**
- Renders a React component

## External dependencies
- react-dom
- clsx
- lucide-react
- @/app/styles/design-tokens
- @/components/ui/button

## Flagged idioms
- Using hooks like useFormStatus to manage component state in React.

## Behavioral notes
- The button shows a loading indicator when the form is pending.
