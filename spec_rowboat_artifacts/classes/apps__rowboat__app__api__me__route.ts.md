# apps/rowboat/app/api/me/route.ts

**File:** apps/rowboat/app/api/me/route.ts  
**Language:** typescript

## Purpose
Handle GET requests to return user information based on authentication status.

## Interfaces
### `GET` (function)
```
GET(_req: NextRequest)
```
**Intent:** Determine user identity based on authentication status and respond with user id or an unauthorized error.

**Inputs:**
- _req: NextRequest — the incoming request object
**Outputs:**
- NextResponse — JSON response containing user id or error message
**Side effects:**
- Returns a JSON response with user data or an error message

## Internal dependencies
- @/app/actions/auth.actions
- @/app/lib/feature_flags

## External dependencies
- next/server

## Flagged idioms
- Use of feature flags to conditionally execute authentication logic.

## Behavioral notes
- If USE_AUTH is false, a default guest user id is returned.
