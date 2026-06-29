# apps/rowboat/app/projects/[projectId]/jobs/page.tsx

**File:** apps/rowboat/app/projects/[projectId]/jobs/page.tsx  
**Language:** typescript

## Purpose
Render a page that displays a list of jobs for a specific project, ensuring the user has an active billing subscription.

## Interfaces
### `Page` (function)
```
Page(props: { params: Promise<{ projectId: string }> })
```
**Intent:** Fetch the projectId from the provided promise, verify active billing, and render the JobsList component for that project.

**Inputs:**
- props: { params: Promise<{ projectId: string }> } — an object containing a promise that resolves to an object with a projectId
**Outputs:**
- JSX.Element — a component rendering the jobs list for the specified project
**Side effects:**
- awaits requireActiveBillingSubscription: ensures the user has an active billing subscription

## Internal dependencies
- ./components/jobs-list

## External dependencies
- next
- @/app/lib/billing

## Flagged idioms
- async/await: used to handle asynchronous operations for fetching parameters and checking billing status

## Behavioral notes
- The function ensures that the user has an active billing subscription before rendering the jobs list.
