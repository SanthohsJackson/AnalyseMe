# apps/x/packages/core/src/code-mode/types.ts

**File:** apps/x/packages/core/src/code-mode/types.ts  
**Language:** typescript

## Purpose
Define and validate configuration and status objects for code mode agents using Zod schemas.

## External dependencies
- zod
- @x/shared/dist/code-mode.js

## Flagged idioms
- Use of Zod for schema validation: provides runtime type checking and validation for objects.

## Behavioral notes
- The 'approvalPolicy' field in 'CodeModeConfig' is optional and defaults to 'ask' if not set.
