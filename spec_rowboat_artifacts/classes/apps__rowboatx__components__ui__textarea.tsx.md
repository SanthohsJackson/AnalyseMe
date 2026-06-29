# apps/rowboatx/components/ui/textarea.tsx

**File:** apps/rowboatx/components/ui/textarea.tsx  
**Language:** typescript

## Purpose
Provide a styled textarea component for user input in a React application.

## Interfaces
### `Textarea` (function)
```
Textarea({ className, ...props }: React.ComponentProps<'textarea'>)
```
**Intent:** Render a textarea element with predefined styles and additional properties.

**Inputs:**
- className: string — additional CSS classes to apply
- ...props: React.ComponentProps<'textarea'> — other properties for the textarea element

## Internal dependencies
- @/lib/utils

## External dependencies
- react

## Flagged idioms
- Spread operator: used to pass additional props to the textarea element.

## Behavioral notes
- The textarea is styled with a combination of predefined and custom classes.
