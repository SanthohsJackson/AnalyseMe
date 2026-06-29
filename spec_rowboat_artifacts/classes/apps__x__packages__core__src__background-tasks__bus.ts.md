# apps/x/packages/core/src/background-tasks/bus.ts

**File:** apps/x/packages/core/src/background-tasks/bus.ts  
**Language:** typescript

## Purpose
Manage subscription and publication of background task events.

## Interfaces
### `publish` (method)
```
publish(event: BackgroundTaskAgentEventType): void
```
**Intent:** Notify all subscribed handlers of a new event.

**Inputs:**
- event: BackgroundTaskAgentEventType — the event to be published to subscribers
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

### `BackgroundTaskBus` (class)
```
class BackgroundTaskBus
```
**Intent:** Encapsulate the logic for managing event subscriptions and publications.


## External dependencies
- @x/shared/dist/background-task.js

## Flagged idioms
- Use of closures to maintain state for unsubscribing handlers.

## Behavioral notes
- Handlers are stored in an array and called in the order they were added.
