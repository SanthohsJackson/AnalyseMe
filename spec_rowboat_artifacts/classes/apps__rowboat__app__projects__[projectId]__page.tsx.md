# apps/rowboat/app/projects/[projectId]/page.tsx

**File:** apps/rowboat/app/projects/[projectId]/page.tsx  
**Language:** typescript

## Purpose
Redirects to a project's workflow page after ensuring an active billing subscription.

## Interfaces
### `Page` (function)
```
Page(props: { params: Promise<{ projectId: string }> })
```
**Intent:** Ensures the user has an active billing subscription and then redirects them to the project's workflow page.

**Inputs:**
- props: { params: Promise<{ projectId: string }> } — an object containing a promise that resolves to an object with a projectId
**Side effects:**
- redirects to a URL based on the projectId
- calls requireActiveBillingSubscription

## Internal dependencies
- @/app/lib/billing

## External dependencies
- next/navigation

## Flagged idioms
- async/await pattern for handling promises

## Behavioral notes
- The function assumes the promise in props.params resolves successfully.
