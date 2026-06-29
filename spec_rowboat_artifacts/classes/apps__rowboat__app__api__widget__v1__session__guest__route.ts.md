# apps/rowboat/app/api/widget/v1/session/guest/route.ts

**File:** apps/rowboat/app/api/widget/v1/session/guest/route.ts  
**Language:** typescript

## Purpose
Handle POST requests to create a guest session and return a signed JWT.

## Interfaces
### `POST` (function)
```
POST(req: NextRequest) -> Promise<Response>
```
**Intent:** Create a guest session with a unique user ID and return a signed JWT as the session ID.

**Inputs:**
- req: NextRequest — the incoming HTTP request
**Outputs:**
- Promise<Response> — a JSON response containing the sessionId
**Side effects:**
- Generates a JWT token
- Reads environment variable CHAT_WIDGET_SESSION_JWT_SECRET

## Internal dependencies
- apps/rowboat/app/api/widget/v1/utils

## External dependencies
- next/server
- jose
- zod
- rowboat-shared

## Flagged idioms
- Use of async/await for handling asynchronous operations

## Behavioral notes
- The function relies on an environment variable for signing the JWT.
