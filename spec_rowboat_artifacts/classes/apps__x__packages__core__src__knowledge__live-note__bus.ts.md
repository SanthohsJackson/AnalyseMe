# apps/x/packages/core/src/knowledge/live-note/bus.ts

**File:** apps/x/packages/core/src/knowledge/live-note/bus.ts  
**Language:** typescript

## Purpose
Manage event subscription and publication for live notes.

## Interfaces
### `publish` (method)
```
publish(event: LiveNoteAgentEventType): void
```
**Intent:** Notify all subscribed handlers of a new event.

**Inputs:**
- event: LiveNoteAgentEventType — the event to be published to subscribers
**Side effects:**
- Calls each subscribed handler with the event

### `subscribe` (method)
```
subscribe(handler: Handler): () => void
```
**Intent:** Register a handler to be called on event publication and provide a way to unsubscribe.

**Inputs:**
- handler: Handler — the function to be called when an event is published
**Outputs:**
- () => void — a function to unsubscribe the handler
**Side effects:**
- Adds the handler to the list of subscribers

### `LiveNoteBus` (class)
```
class LiveNoteBus
```
**Intent:** Encapsulate the logic for managing event subscriptions and publications.


## External dependencies
- @x/shared/dist/live-note.js

## Flagged idioms
- Use of closures to maintain state for unsubscribing handlers.

## Behavioral notes
- The unsubscribe function removes the handler from the list of subscribers if it exists.
