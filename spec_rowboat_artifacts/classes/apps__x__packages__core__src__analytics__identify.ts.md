# apps/x/packages/core/src/analytics/identify.ts

**File:** apps/x/packages/core/src/analytics/identify.ts  
**Language:** typescript

## Purpose
Identify a user with PostHog analytics if they are signed in and have billing information.

## Interfaces
### `identifyIfSignedIn` (function)
```
identifyIfSignedIn() -> Promise<void>
```
**Intent:** To ensure that user identification is performed with PostHog analytics if the user is signed in and has valid billing information.

**Outputs:**
- Promise<void> — resolves when identification process completes
**Side effects:**
- Logs errors to console if identification fails
- Calls identify function from posthog.js with user data

## Internal dependencies
- ../account/account.js
- ../billing/billing.js
- ./posthog.js

## Flagged idioms
- Use of async/await for handling asynchronous operations

## Behavioral notes
- The function is idempotent and safe to call on every app start.
- Errors during the identification process are caught and logged, preventing them from blocking app launch.
