# apps/rowboat/app/projects/[projectId]/sources/components/delete.tsx

**File:** apps/rowboat/app/projects/[projectId]/sources/components/delete.tsx  
**Language:** typescript

## Purpose
Provide a form component to delete a data source after user confirmation.

## Interfaces
### `DeleteSource` (function)
```
DeleteSource({ sourceId }: { sourceId: string })
```
**Intent:** Render a form that allows users to delete a data source by confirming their action.

**Inputs:**
- sourceId: string — the identifier of the data source to delete
**Side effects:**
- Renders a form with a button to delete a data source

### `handleDelete` (function)
```
handleDelete()
```
**Intent:** Handle the deletion of a data source after user confirmation.

**Side effects:**
- Prompts user for confirmation and deletes the data source if confirmed

## Internal dependencies
- ../../../../actions/data-source.actions
- ../../../../lib/components/form-status-button

## Flagged idioms
- Using a form with a submit button to trigger a JavaScript function for side effects

## Behavioral notes
- The deletion is contingent on user confirmation via a window prompt.
