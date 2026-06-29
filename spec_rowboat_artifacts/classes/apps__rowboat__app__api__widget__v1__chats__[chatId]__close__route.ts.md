# apps/rowboat/app/api/widget/v1/chats/[chatId]/close/route.ts

**File:** apps/rowboat/app/api/widget/v1/chats/[chatId]/close/route.ts  
**Language:** typescript

## Purpose
Close a chat by updating its status in the database if it meets certain conditions.

## Interfaces
### `POST` (function)
```
POST(request: NextRequest, props: { params: Promise<{ chatId: string }> }): Promise<Response>
```
**Intent:** Attempt to close a chat by setting its 'closed' status to true if it is not already closed and belongs to the authenticated user.

**Inputs:**
- request: NextRequest — the incoming HTTP request
- props: { params: Promise<{ chatId: string }> } — an object containing a promise that resolves to the chat ID
**Outputs:**
- Promise<Response> — a promise that resolves to an HTTP response
**Side effects:**
- Updates the chat document in the MongoDB collection
- Returns a JSON response with the updated chat document or an error message

## Internal dependencies
- ../../../utils

## External dependencies
- next/server
- mongodb
- ../../../../../../lib/mongodb

## Flagged idioms
- Use of async/await for handling asynchronous operations
- MongoDB's findOneAndUpdate method to atomically update a document and return the updated document

## Behavioral notes
- The function checks if the chat is already closed and belongs to the authenticated user before updating.
