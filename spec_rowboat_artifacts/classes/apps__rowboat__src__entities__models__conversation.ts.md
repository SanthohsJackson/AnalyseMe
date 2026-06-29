# apps/rowboat/src/entities/models/conversation.ts

**File:** apps/rowboat/src/entities/models/conversation.ts  
**Language:** typescript

## Purpose
Define a schema for a conversation object using zod.

## Internal dependencies
- ./turn

## External dependencies
- zod
- @/app/lib/types/workflow_types

## Flagged idioms
- Use of zod for schema validation: provides a declarative way to define and validate data structures.

## Behavioral notes
- The 'turns' field is optional, and 'updatedAt' is also optional, indicating flexibility in the data structure.
