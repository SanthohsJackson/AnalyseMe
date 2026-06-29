# apps/rowboat/app/scripts/delete_qdrant.ts

**File:** apps/rowboat/app/scripts/delete_qdrant.ts  
**Language:** typescript

## Purpose
Delete a Qdrant collection named 'embeddings'.

## Internal dependencies
- ../lib/loadenv
- ../lib/qdrant

## Flagged idioms
- Immediately Invoked Function Expression (IIFE): used to execute asynchronous code in a contained scope.

## Behavioral notes
- Logs the result of the delete operation or an error if it fails.
