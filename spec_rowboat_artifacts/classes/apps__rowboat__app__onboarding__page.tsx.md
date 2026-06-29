# apps/rowboat/app/onboarding/page.tsx

**File:** apps/rowboat/app/onboarding/page.tsx  
**Language:** typescript

## Purpose
Render the onboarding page, enforcing authentication if required.

## Interfaces
### `Page` (function)
```
Page()
```
**Intent:** Render the App component for the onboarding page, redirecting or requiring authentication based on feature flags.

**Outputs:**
- JSX.Element — the rendered App component
**Side effects:**
- redirects to '/projects' if USE_AUTH is false
- calls requireAuth() to enforce authentication

## Internal dependencies
- ./app
- ../lib/auth
- ../lib/feature_flags

## External dependencies
- next/navigation

## Flagged idioms
- Conditional redirect based on feature flag: controls access flow based on configuration

## Behavioral notes
- The function will redirect to '/projects' if the USE_AUTH flag is false, bypassing authentication.
