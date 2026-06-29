# apps/rowboat/app/projects/[projectId]/sources/page.tsx

**File:** apps/rowboat/app/projects/[projectId]/sources/page.tsx  
**Language:** typescript

## Purpose
Render a page displaying a list of data sources for a specific project, ensuring an active billing subscription.

## Interfaces
### `Page` (function)
```
Page(props: { params: Promise<{ projectId: string }> })
```
**Intent:** Render the SourcesList component for a given project, ensuring the user has an active billing subscription.

**Inputs:**
- props: { params: Promise<{ projectId: string }> } — an object containing a promise that resolves to an object with a projectId
**Outputs:**
- JSX.Element — a React component rendering the SourcesList
**Side effects:**
- await requireActiveBillingSubscription() — checks for an active billing subscription

## Internal dependencies
- ./components/sources-list
- @/app/lib/billing

## External dependencies
- next

## Flagged idioms
- Using async/await to handle promises in a React component function.
