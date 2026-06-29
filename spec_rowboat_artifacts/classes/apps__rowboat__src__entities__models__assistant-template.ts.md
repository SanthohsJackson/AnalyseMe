# apps/rowboat/src/entities/models/assistant-template.ts

**File:** apps/rowboat/src/entities/models/assistant-template.ts  
**Language:** typescript

## Purpose
Define and validate data structures for assistant templates and their likes using zod.

## Internal dependencies
- ../../../app/lib/types/workflow_types

## External dependencies
- zod

## Flagged idioms
- Use of zod for schema validation: provides a declarative way to define and validate data structures.

## Behavioral notes
- The 'source' field in AssistantTemplate is restricted to specific values ('library', 'community') using zod's enum.
