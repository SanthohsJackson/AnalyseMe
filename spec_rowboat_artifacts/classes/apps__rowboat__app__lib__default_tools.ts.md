# apps/rowboat/app/lib/default_tools.ts

**File:** apps/rowboat/app/lib/default_tools.ts  
**Language:** typescript

## Purpose
Provide a list of default built-in tools for a workflow editor, conditionally based on environment variables.

## Interfaces
### `getDefaultTools` (function)
```
getDefaultTools() -> Array<any>
```
**Intent:** Return a list of default tools for use in a workflow editor if a specific environment flag is set.

**Outputs:**
- Array<any> — list of default tools if the condition is met, otherwise an empty array

## External dependencies
- zod

## Behavioral notes
- The function checks an environment variable to determine if it should return the list of tools or an empty array.
