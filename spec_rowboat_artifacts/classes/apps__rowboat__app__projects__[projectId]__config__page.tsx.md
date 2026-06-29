# apps/rowboat/app/projects/[projectId]/config/page.tsx

**File:** apps/rowboat/app/projects/[projectId]/config/page.tsx  
**Language:** typescript

## Purpose
Render a project settings page after ensuring an active billing subscription.

## Interfaces
### `Page` (function)
```
Page(props: { params: Promise<{ projectId: string; }> })
```
**Intent:** Render the SimpleConfigApp component for a specific project after verifying billing status.

**Inputs:**
- props: { params: Promise<{ projectId: string; }> } — an object containing a promise that resolves to an object with a projectId
**Outputs:**
- JSX.Element — a React component rendering the SimpleConfigApp
**Side effects:**
- awaits requireActiveBillingSubscription which may have side effects related to billing

## Internal dependencies
- ./app
- @/app/lib/billing

## External dependencies
- next

## Flagged idioms
- async/await: used for handling asynchronous operations, ensuring billing is checked before rendering

## Behavioral notes
- The function awaits a promise for params, indicating asynchronous data fetching.
