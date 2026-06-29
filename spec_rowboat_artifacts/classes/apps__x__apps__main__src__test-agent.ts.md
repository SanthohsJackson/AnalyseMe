# apps/x/apps/main/src/test-agent.ts

**File:** apps/x/apps/main/src/test-agent.ts  
**Language:** typescript

## Purpose
Execute a main function that creates a run and a message, and subscribes to events using an external bus.

## Interfaces
### `main` (function)
```
async function main()
```
**Intent:** Initialize a run, subscribe to its events, and send a message, logging each step.

**Side effects:**
- Logs to console
- Creates a run using runsCore.createRun
- Subscribes to events using bus.subscribe
- Creates a message using runsCore.createMessage

## External dependencies
- @x/core/dist/runs/runs.js
- @x/core/dist/runs/bus.js

## Flagged idioms
- Async/await: Used for handling asynchronous operations in a readable manner.

## Behavioral notes
- The function assumes the existence of an agent file at WorkDir/agents/test-agent.md.
