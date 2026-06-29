# apps/rowboat/app/projects/[projectId]/manage-triggers/scheduled/new/page.tsx

**File:** apps/rowboat/app/projects/[projectId]/manage-triggers/scheduled/new/page.tsx  
**Language:** typescript

## Purpose
Render a page for creating a scheduled job rule, ensuring the user has an active billing subscription.

## Interfaces
### `Page` (function)
```
Page(props: { params: Promise<{ projectId: string }> })
```
**Intent:** Render a form for creating a scheduled job rule after verifying the user has an active billing subscription.

**Inputs:**
- props: { params: Promise<{ projectId: string }> } — an object containing a promise that resolves to an object with a projectId
**Outputs:**
- JSX.Element — a React component for creating a scheduled job rule
**Side effects:**
- awaits requireActiveBillingSubscription which may perform network or state validation

## Internal dependencies
- ../components/create-scheduled-job-rule-form
- @/app/lib/billing

## External dependencies
- next

## Flagged idioms
- Using async/await in a React component to handle asynchronous operations before rendering.

## Behavioral notes
- The function ensures billing subscription is active before rendering the form.
