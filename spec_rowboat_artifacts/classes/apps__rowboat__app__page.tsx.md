# apps/rowboat/app/page.tsx

**File:** apps/rowboat/app/page.tsx  
**Language:** typescript

## Purpose
Render the Home component and redirect based on authentication feature flag.

## Interfaces
### `Home` (function)
```
Home()
```
**Intent:** Render the App component or redirect to '/projects' based on the USE_AUTH flag.

**Outputs:**
- JSX.Element — the rendered App component
**Side effects:**
- redirects to '/projects' if USE_AUTH is false

## Internal dependencies
- ./app
- ./lib/feature_flags

## External dependencies
- next/navigation

## Flagged idioms
- Conditional rendering and redirection based on a feature flag.

## Behavioral notes
- The function redirects to '/projects' if the USE_AUTH flag is not enabled.
