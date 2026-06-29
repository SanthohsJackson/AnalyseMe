# apps/rowboat/app/projects/[projectId]/manage-triggers/recurring/[ruleId]/page.tsx

**File:** apps/rowboat/app/projects/[projectId]/manage-triggers/recurring/[ruleId]/page.tsx  
**Language:** typescript

## Purpose
Render a view for a recurring job rule after ensuring an active billing subscription.

## Interfaces
### `Page` (function)
```
Page(props: { params: Promise<{ projectId: string; ruleId: string }> })
```
**Intent:** Fetch parameters, ensure billing is active, and render the recurring job rule view.

**Inputs:**
- props: { params: Promise<{ projectId: string; ruleId: string }> } — an object containing a promise that resolves to project and rule identifiers
**Outputs:**
- JSX.Element — a React component rendering the recurring job rule view
**Side effects:**
- await requireActiveBillingSubscription() — checks for an active billing subscription

## Internal dependencies
- ../../components/recurring-job-rule-view
- @/app/lib/billing

## External dependencies
- next

## Flagged idioms
- async/await — used for handling asynchronous operations like fetching parameters and checking billing status

## Behavioral notes
- The function ensures an active billing subscription before rendering the view.
