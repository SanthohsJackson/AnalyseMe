# apps/rowboat/app/projects/[projectId]/manage-triggers/page.tsx

**File:** apps/rowboat/app/projects/[projectId]/manage-triggers/page.tsx  
**Language:** typescript

## Purpose
Render a page component that requires an active billing subscription and displays job rules tabs for a specific project.

## Interfaces
### `Page` (function)
```
Page(props: { params: Promise<{ projectId: string }> })
```
**Intent:** Render the JobRulesTabs component for a given project, ensuring the user has an active billing subscription.

**Inputs:**
- props: { params: Promise<{ projectId: string }> } — an object containing a promise that resolves to an object with a projectId
**Outputs:**
- JSX.Element — a component rendering job rules tabs for the specified project
**Side effects:**
- await requireActiveBillingSubscription(): ensures an active billing subscription is present

## Internal dependencies
- ./components/job-rules-tabs
- @/app/lib/billing

## External dependencies
- next

## Flagged idioms
- async/await: used for handling promises and asynchronous operations
