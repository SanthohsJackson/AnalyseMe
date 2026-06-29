# apps/rowboat/app/projects/[projectId]/manage-triggers/triggers/[deploymentId]/page.tsx

**File:** apps/rowboat/app/projects/[projectId]/manage-triggers/triggers/[deploymentId]/page.tsx  
**Language:** typescript

## Purpose
Render a page for managing a specific trigger deployment, ensuring the user has an active billing subscription.

## Interfaces
### `Page` (function)
```
Page(props: { params: Promise<{ projectId: string; deploymentId: string }> })
```
**Intent:** Render the ComposioTriggerDeploymentView component for a specific project and deployment, after verifying billing status.

**Inputs:**
- props: { params: Promise<{ projectId: string; deploymentId: string }> } — promise resolving to project and deployment identifiers
**Outputs:**
- JSX.Element — component rendering the trigger deployment view
**Side effects:**
- requireActiveBillingSubscription: checks for an active billing subscription

## Internal dependencies
- ../../components/composio-trigger-deployment-view
- @/app/lib/billing

## External dependencies
- next

## Flagged idioms
- async/await: used to handle asynchronous operations for params and billing check
