# apps/cli/src/examples/index.ts

**File:** apps/cli/src/examples/index.ts  
**Language:** typescript

## Purpose
Define and export a record of examples parsed from JSON using a Zod schema.

## Internal dependencies
- ../entities/example.js

## External dependencies
- zod

## Flagged idioms
- TypeScript's 'import with' syntax is used to import JSON with a specific type.

## Behavioral notes
- The 'examples' object is typed using Zod's inference capabilities to ensure it matches the 'Example' schema.
