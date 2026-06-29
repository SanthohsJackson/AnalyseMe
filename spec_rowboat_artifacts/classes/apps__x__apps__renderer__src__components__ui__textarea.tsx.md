# apps/x/apps/renderer/src/components/ui/textarea.tsx

**File:** apps/x/apps/renderer/src/components/ui/textarea.tsx  
**Language:** typescript

## Purpose
Provide a styled textarea component with forwarding ref support.

## Interfaces
### `TextareaProps` (class)
```
interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement>
```
**Intent:** Define the props for the Textarea component, extending standard textarea attributes.


## Internal dependencies
- ../../lib/utils

## External dependencies
- react

## Flagged idioms
- React.forwardRef: used to pass refs to DOM elements in functional components

## Behavioral notes
- The component applies a set of predefined styles and merges them with any additional class names provided.
