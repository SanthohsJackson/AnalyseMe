# apps/rowboat/app/projects/[projectId]/workflow/error.tsx

**File:** apps/rowboat/app/projects/[projectId]/workflow/error.tsx  
**Language:** typescript

## Purpose
Display an error message using an Alert component when there is an error loading a workflow.

## Interfaces
### `Error` (function)
```
Error(props: { error: Error })
```
**Intent:** Render an Alert component to inform the user about an error that occurred while loading a workflow.

**Inputs:**
- props: { error: Error } — an object containing the error to display

## External dependencies
- @heroui/react

## Flagged idioms
- JSX syntax: used to define the structure of the Alert component within the function.

## Behavioral notes
- The error message displayed is derived from the 'message' property of the error object passed in props.
