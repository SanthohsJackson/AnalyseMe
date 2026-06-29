# apps/rowboat/app/lib/components/form-status-button.tsx

**File:** apps/rowboat/app/lib/components/form-status-button.tsx  
**Language:** typescript

## Purpose
Render a button component with status-dependent loading behavior.

## Interfaces
### `FormStatusButton` (function)
```
FormStatusButton({ props }: { props: ButtonHTMLAttributes<HTMLButtonElement> & { startContent?: React.ReactNode; endContent?: React.ReactNode; variant?: 'primary' | 'secondary' | 'tertiary'; size?: 'sm' | 'md' | 'lg'; isLoading?: boolean; } })
```
**Intent:** Render a button that reflects the form's pending status by showing a loading indicator.

**Inputs:**
- props: ButtonHTMLAttributes<HTMLButtonElement> & { startContent?: React.ReactNode; endContent?: React.ReactNode; variant?: 'primary' | 'secondary' | 'tertiary'; size?: 'sm' | 'md' | 'lg'; isLoading?: boolean; } — properties for the button component
**Outputs:**
- JSX.Element — a button component with loading state

## External dependencies
- react-dom
- @/components/ui/button
- react

## Flagged idioms
- Destructuring assignment is used to extract 'pending' from the useFormStatus hook, which is a common pattern in React to access specific values from hooks.

## Behavioral notes
- The button's loading state is controlled by the 'pending' status from the useFormStatus hook.
