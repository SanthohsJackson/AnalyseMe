# apps/rowboat/app/projects/[projectId]/jobs/[jobId]/page.tsx

**File:** apps/rowboat/app/projects/[projectId]/jobs/[jobId]/page.tsx  
**Language:** typescript

## Purpose
Render a job view page after ensuring an active billing subscription.

## Interfaces
### `Page` (function)
```
Page(props: { params: Promise<{ projectId: string, jobId: string }> })
```
**Intent:** Render the JobView component for a specific project and job, ensuring the user has an active billing subscription.

**Inputs:**
- props: { params: Promise<{ projectId: string, jobId: string }> } — an object containing a promise that resolves to project and job identifiers
**Outputs:**
- JSX.Element — a rendered JobView component
**Side effects:**
- awaits requireActiveBillingSubscription which may perform network or subscription validation

## Internal dependencies
- ../components/job-view
- @/app/lib/billing

## External dependencies
- next

## Flagged idioms
- Using async/await to handle promises for asynchronous operations.

## Behavioral notes
- The function ensures an active billing subscription before rendering the component.
