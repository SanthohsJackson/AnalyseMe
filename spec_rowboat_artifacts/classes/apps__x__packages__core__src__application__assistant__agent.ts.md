# apps/x/packages/core/src/application/assistant/agent.ts

**File:** apps/x/packages/core/src/application/assistant/agent.ts  
**Language:** typescript

## Purpose
Build a CopilotAgent dynamically using built-in tools and live instructions.

## Interfaces
### `buildCopilotAgent` (function)
```
buildCopilotAgent() -> Promise<z.infer<typeof Agent>>
```
**Intent:** Constructs a CopilotAgent with tools derived from BuiltinTools and instructions from buildCopilotInstructions.

**Outputs:**
- Promise<z.infer<typeof Agent>> — an object representing the CopilotAgent

## Internal dependencies
- ./instructions.js
- ../lib/builtin-tools.js

## External dependencies
- @x/shared/dist/agent.js
- zod

## Flagged idioms
- Use of async/await for handling asynchronous operations.

## Behavioral notes
- The tools object is dynamically populated based on the keys of BuiltinTools.
