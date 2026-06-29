# apps/rowboat/app/scripts/setup_qdrant.ts

**File:** apps/rowboat/app/scripts/setup_qdrant.ts  
**Language:** typescript

## Purpose
Set up a Qdrant collection for storing embedding vectors.

## Internal dependencies
- ../lib/loadenv
- ../lib/qdrant

## Flagged idioms
- Immediately Invoked Function Expression (IIFE): used to execute asynchronous setup code immediately.

## Behavioral notes
- The EMBEDDING_VECTOR_SIZE is determined by an environment variable or defaults to 1536 if not set.
- The collection creation logs success or failure to the console.
