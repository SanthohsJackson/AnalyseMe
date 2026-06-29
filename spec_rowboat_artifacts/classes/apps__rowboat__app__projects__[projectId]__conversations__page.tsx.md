# apps/rowboat/app/projects/[projectId]/conversations/page.tsx

**File:** apps/rowboat/app/projects/[projectId]/conversations/page.tsx  
**Language:** typescript

## Purpose
Render a page that displays a list of conversations for a given project, ensuring the user has an active billing subscription.

## Interfaces
### `Page` (function)
```
Page(props: { params: Promise<{ projectId: string }> })
```
**Intent:** Render the ConversationsList component for a specific project after verifying the user's billing status.

**Inputs:**
- props: { params: Promise<{ projectId: string }> } — an object containing a promise that resolves to an object with a projectId
**Outputs:**
- JSX.Element — a React component rendering the ConversationsList
**Side effects:**
- await requireActiveBillingSubscription(): ensures the user has an active billing subscription

## Internal dependencies
- ./components/conversations-list
- @/app/lib/billing

## External dependencies
- next

## Flagged idioms
- async/await: used for handling promises and asynchronous operations

## Behavioral notes
- The function ensures that the user has an active billing subscription before rendering the component.
