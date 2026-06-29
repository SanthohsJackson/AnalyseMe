# apps/x/packages/core/src/account/account.ts

**File:** apps/x/packages/core/src/account/account.ts  
**Language:** typescript

## Purpose
Determine if a user is signed in by checking for the presence of tokens.

## Interfaces
### `isSignedIn` (function)
```
isSignedIn() -> Promise<boolean>
```
**Intent:** Check the OAuth repository for tokens to determine if a user is signed in.

**Outputs:**
- Promise<boolean> — resolves to true if tokens are present, false otherwise
**Side effects:**
- Resolves a dependency from a container and reads data from an OAuth repository

## Internal dependencies
- ../di/container.js
- ../auth/repo.js

## Flagged idioms
- Dependency injection via a container to resolve the OAuth repository

## Behavioral notes
- The function checks for tokens associated with 'rowboat' to determine sign-in status.
