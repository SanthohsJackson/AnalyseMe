# apps/rowboat/app/projects/[projectId]/sources/new/page.tsx

**File:** apps/rowboat/app/projects/[projectId]/sources/new/page.tsx  
**Language:** typescript

## Purpose
Render a form for adding a data source, redirecting if a feature flag is not enabled.

## Interfaces
### `Page` (function)
```
Page(props: { params: Promise<{ projectId: string }> })
```
**Intent:** Render a form component for adding a data source if the USE_RAG feature flag is true; otherwise, redirect to the project page.

**Inputs:**
- props: { params: Promise<{ projectId: string }> } — an object containing a promise that resolves to an object with a projectId
**Side effects:**
- redirects to another page if USE_RAG is false
- awaits requireActiveBillingSubscription

## Internal dependencies
- ./form
- ../../../../lib/feature_flags
- @/app/lib/billing

## External dependencies
- next
- next/navigation

## Flagged idioms
- Using feature flags to conditionally redirect or render components.

## Behavioral notes
- The function awaits a promise for params and requires an active billing subscription before proceeding.
