# apps/rowboat/app/scripts/mongodb-drop-indexes.ts

**File:** apps/rowboat/app/scripts/mongodb-drop-indexes.ts  
**Language:** typescript

## Purpose
Drop all non-_id indexes from a MongoDB database.

## Interfaces
### `main` (function)
```
main()
```
**Intent:** Execute the process of dropping all non-_id indexes from the database and handle any errors that occur.

**Raises:**
- Error: when an error occurs during index dropping
**Side effects:**
- Logs to console
- Exits process with status 1 on error

## Internal dependencies
- ../../src/infrastructure/mongodb/drop-indexes

## External dependencies
- ../lib/loadenv
- ../lib/mongodb

## Flagged idioms
- async/await: used for handling asynchronous operations
- try/catch with .catch(): used for error handling in asynchronous functions

## Behavioral notes
- The function logs a message to the console upon successful completion and logs an error message and exits the process if an error occurs.
