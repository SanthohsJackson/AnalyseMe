# apps/rowboat/app/projects/[projectId]/sources/components/web-recrawl.tsx

**File:** apps/rowboat/app/projects/[projectId]/sources/components/web-recrawl.tsx  
**Language:** typescript

## Purpose
Render a form with a button to trigger a refresh action.

## Interfaces
### `Recrawl` (function)
```
Recrawl({ handleRefresh }: { handleRefresh: () => void })
```
**Intent:** Provide a user interface element to initiate a refresh operation.

**Inputs:**
- handleRefresh: () => void — a function to be called on form submission
**Side effects:**
- Submits a form which triggers the handleRefresh function

## External dependencies
- lucide-react
- ../../../../lib/components/form-status-button

## Flagged idioms
- JSX syntax for defining React components
