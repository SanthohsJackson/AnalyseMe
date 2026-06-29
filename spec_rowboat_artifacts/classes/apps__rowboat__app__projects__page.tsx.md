# apps/rowboat/app/projects/page.tsx

**File:** apps/rowboat/app/projects/page.tsx  
**Language:** typescript

## Purpose
Render the App component after ensuring an active billing subscription.

## Interfaces
### `Page` (function)
```
Page()
```
**Intent:** Ensure the user has an active billing subscription before rendering the App component.

**Side effects:**
- awaits requireActiveBillingSubscription

## Internal dependencies
- ./app

## External dependencies
- @/app/lib/billing

## Flagged idioms
- Using async/await to handle asynchronous operations in a function.
