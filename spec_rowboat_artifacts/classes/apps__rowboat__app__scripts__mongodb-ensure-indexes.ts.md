# apps/rowboat/app/scripts/mongodb-ensure-indexes.ts

**File:** apps/rowboat/app/scripts/mongodb-ensure-indexes.ts  
**Language:** typescript

## Purpose
Ensure all necessary MongoDB indexes are created.

## Interfaces
### `main` (function)
```
main()
```
**Intent:** Invoke the ensureAllIndexes function to set up database indexes and handle any errors by logging and exiting.

**Raises:**
- Error: when ensureAllIndexes fails
**Side effects:**
- Logs to console
- Exits process with status 1 on error

## Internal dependencies
- ../../src/infrastructure/mongodb/ensure-indexes

## External dependencies
- ../lib/loadenv
- ../lib/mongodb

## Flagged idioms
- async/await: used for handling asynchronous operations
- try/catch pattern: implemented using .catch() for error handling

## Behavioral notes
- The process exits with status 1 if an error occurs during index creation.
