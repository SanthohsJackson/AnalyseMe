# apps/rowboat/app/api/tmp-images/[id]/route.ts

**File:** apps/rowboat/app/api/tmp-images/[id]/route.ts  
**Language:** typescript

## Purpose
Handle GET requests to serve temporary images from an in-memory cache.

## Interfaces
### `GET` (function)
```
GET(request: NextRequest, props: { params: Promise<{ id: string }> })
```
**Intent:** Retrieve and serve an image from a temporary in-memory cache using an ID, or return an error if the ID is missing or the image is not found.

**Inputs:**
- request: NextRequest — the incoming request object
- props: { params: Promise<{ id: string }> } — an object containing a promise that resolves to an object with an 'id' string
**Outputs:**
- NextResponse — a response object with the image data or an error message
**Side effects:**
- Returns a JSON response with an error message if the 'id' is missing or not found
- Serves image data from the in-memory cache if available

## Internal dependencies
- @/src/application/services/temp-binary-cache

## External dependencies
- next/server

## Flagged idioms
- Use of async/await to handle asynchronous operations with promises

## Behavioral notes
- The function checks for the presence of an 'id' and returns a 400 error if it is missing.
- If the image is not found in the cache, a 404 error is returned.
- The response includes headers to control caching and content disposition.
