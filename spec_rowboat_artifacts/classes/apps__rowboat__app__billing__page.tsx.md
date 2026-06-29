# apps/rowboat/app/billing/page.tsx

**File:** apps/rowboat/app/billing/page.tsx  
**Language:** typescript

## Purpose
Render a billing page or redirect based on billing feature flag.

## Interfaces
### `Page` (function)
```
Page()
```
**Intent:** Render the billing page for a customer if billing is enabled; otherwise, redirect to the projects page.

**Outputs:**
- JSX.Element — rendered billing page component
**Side effects:**
- redirect to '/projects' if billing is not used

## Internal dependencies
- ../lib/billing
- ./app
- ../lib/feature_flags

## External dependencies
- next/navigation

## Flagged idioms
- Conditional redirect based on feature flag: controls access to billing features.

## Behavioral notes
- The function performs an asynchronous operation to fetch customer and usage data before rendering the page.
