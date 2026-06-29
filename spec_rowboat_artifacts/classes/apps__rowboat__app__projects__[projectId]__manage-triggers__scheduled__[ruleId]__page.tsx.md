# apps/rowboat/app/projects/[projectId]/manage-triggers/scheduled/[ruleId]/page.tsx

**File:** apps/rowboat/app/projects/[projectId]/manage-triggers/scheduled/[ruleId]/page.tsx  
**Language:** typescript

## Purpose
Render a scheduled job rule view after ensuring an active billing subscription.

## Interfaces
### `Page` (function)
```
Page(props: { params: Promise<{ projectId: string; ruleId: string }> })
```
**Intent:** Render the ScheduledJobRuleView component with the provided project and rule identifiers after verifying the billing subscription.

**Inputs:**
- props: { params: Promise<{ projectId: string; ruleId: string }> } — an object containing a promise that resolves to project and rule identifiers
**Outputs:**
- JSX.Element — a component rendering the scheduled job rule view
**Side effects:**
- await requireActiveBillingSubscription(): ensures the user has an active billing subscription

## Internal dependencies
- ../components/scheduled-job-rule-view

## External dependencies
- next
- @/app/lib/billing

## Flagged idioms
- async/await: used for handling asynchronous operations, ensuring the billing subscription check is completed before rendering
