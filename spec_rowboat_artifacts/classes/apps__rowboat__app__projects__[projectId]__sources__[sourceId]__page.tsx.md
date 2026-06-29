# apps/rowboat/app/projects/[projectId]/sources/[sourceId]/page.tsx

**File:** apps/rowboat/app/projects/[projectId]/sources/[sourceId]/page.tsx  
**Language:** typescript

## Purpose
Render a page component after ensuring an active billing subscription.

## Interfaces
### `Page` (function)
```
Page(props: { params: Promise<{ projectId: string, sourceId: string }> })
```
**Intent:** Render the SourcePage component with project and source identifiers after verifying billing status.

**Inputs:**
- props: { params: Promise<{ projectId: string, sourceId: string }> } — an object containing a promise that resolves to project and source identifiers
**Outputs:**
- JSX.Element — a React component for the source page
**Side effects:**
- awaits requireActiveBillingSubscription which may perform network or state operations

## Internal dependencies
- ./source-page

## External dependencies
- @/app/lib/billing

## Flagged idioms
- async/await: used for handling asynchronous operations, ensuring billing is checked before rendering

## Behavioral notes
- The function awaits a promise for parameters and a billing subscription check before rendering.
