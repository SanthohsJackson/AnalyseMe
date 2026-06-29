# apps/x/packages/core/src/events/producer.ts

**File:** apps/x/packages/core/src/events/producer.ts  
**Language:** typescript

## Purpose
Manage event creation and directory setup for event processing.

## Interfaces
### `createEvent` (function)
```
createEvent(event: Omit<RowboatEvent, 'id'>) -> Promise<void>
```
**Intent:** Generate a unique ID for the event and save it to the pending events directory.

**Inputs:**
- event: Omit<RowboatEvent, 'id'> — the event data without an ID
**Outputs:**
- Promise<void> — resolves when the event is written to a file
**Side effects:**
- Creates the pending directory if it doesn't exist
- Writes the event data to a JSON file in the pending directory

### `ensureEventDirs` (function)
```
ensureEventDirs() -> void
```
**Intent:** Ensure that the necessary directories for event processing exist.

**Outputs:**
- void
**Side effects:**
- Creates the pending and done directories if they don't exist

## Internal dependencies
- ../config/config.js
- ../application/lib/id-gen.js
- ../di/container.js

## External dependencies
- fs
- path
- @x/shared/dist/events.js

## Flagged idioms
- Use of dependency injection to resolve the ID generator from a container, allowing for flexible configuration and testing.

## Behavioral notes
- The createEvent function assumes that events are processed in chronological order within a batch.
