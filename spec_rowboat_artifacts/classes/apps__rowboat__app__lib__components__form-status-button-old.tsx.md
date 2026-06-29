# apps/rowboat/app/lib/components/form-status-button-old.tsx

**File:** apps/rowboat/app/lib/components/form-status-button-old.tsx  
**Language:** typescript

## Purpose
Render a button component that reflects the form's submission status.

## Interfaces
### `FormStatusButton` (function)
```
FormStatusButton({ props }: { props: ButtonProps })
```
**Intent:** Render a Button that indicates loading state based on form submission status.

**Inputs:**
- props: ButtonProps — properties to pass to the Button component
**Outputs:**
- JSX.Element — a Button component with loading state

## External dependencies
- react-dom
- @heroui/react

## Flagged idioms
- Destructuring assignment to extract 'pending' from useFormStatus hook.

## Behavioral notes
- The Button component's loading state is controlled by the 'pending' status from useFormStatus.
