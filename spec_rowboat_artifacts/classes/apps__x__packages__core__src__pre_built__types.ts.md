# apps/x/packages/core/src/pre_built/types.ts

**File:** apps/x/packages/core/src/pre_built/types.ts  
**Language:** typescript

## Purpose
Define and validate configuration types for pre-built agents using zod.

## External dependencies
- zod

## Flagged idioms
- Use of zod for schema validation and type inference: ensures runtime validation and TypeScript type safety.

## Behavioral notes
- The default values for 'enabled' and 'intervalMs' in PreBuiltAgentConfig ensure that these fields have sensible defaults if not provided.
- The PREBUILT_AGENTS array is used to define a union type for agent names, ensuring type safety for agent name references.
