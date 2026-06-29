# apps/rowboat/app/projects/[projectId]/tools/oauth/callback/page.tsx

**File:** apps/rowboat/app/projects/[projectId]/tools/oauth/callback/page.tsx  
**Language:** typescript

## Purpose
Handle the OAuth callback by closing the window after authentication.

## Interfaces
### `OAuthCallback` (function)
```
OAuthCallback()
```
**Intent:** Close the current window if it was opened by another window to signal the completion of the OAuth authentication process.

**Side effects:**
- Closes the window if it was opened by another window.

## External dependencies
- react

## Flagged idioms
- useEffect: used to perform side effects in functional components.

## Behavioral notes
- The window is only closed if it was opened by another window, as checked by window.opener.
