# apps/cli/src/application/assistant/agent.ts

**File:** apps/cli/src/application/assistant/agent.ts  
**Language:** typescript

## Purpose
Defines a CopilotAgent with a set of built-in tools and instructions.

## Internal dependencies
- ../../agents/agents.js
- ./instructions.js
- ../lib/builtin-tools.js

## External dependencies
- zod

## Flagged idioms
- Use of zod for type inference: Ensures type safety and validation by inferring types from zod schemas.

## Behavioral notes
- The tools object is populated by iterating over entries in BuiltinTools and assigning each tool a type of 'builtin'.
