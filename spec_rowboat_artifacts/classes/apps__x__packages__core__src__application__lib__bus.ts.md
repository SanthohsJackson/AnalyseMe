# apps/x/packages/core/src/application/lib/bus.ts

**File:** apps/x/packages/core/src/application/lib/bus.ts  
**Language:** typescript

## Purpose
Provide an in-memory event bus for publishing and subscribing to events.

## Interfaces
### `publish` (method)
```
publish(event: z.infer<typeof RunEvent>): Promise<void>
```
**Intent:** Broadcast an event to all subscribers for the event's runId and wildcard subscribers.

**Inputs:**
- event: z.infer<typeof RunEvent> — the event to publish
**Outputs:**
- Promise<void> — resolves when all subscribers have been notified
**Side effects:**
- Notifies all subscribers of the event

### `subscribe` (method)
```
subscribe(runId: string, handler: (event: z.infer<typeof RunEvent>) => Promise<void>): Promise<() => void>
```
**Intent:** Register a handler to be called when events with the specified runId are published.

**Inputs:**
- runId: string — the identifier for the event type
- handler: (event: z.infer<typeof RunEvent>) => Promise<void> — the function to handle the event
**Outputs:**
- Promise<() => void> — a function to unsubscribe the handler
**Side effects:**
- Adds a handler to the list of subscribers for the specified runId

### `IBus` (class)
```
interface IBus
```
**Intent:** Define the contract for an event bus with publish and subscribe capabilities.


### `InMemoryBus` (class)
```
class InMemoryBus implements IBus
```
**Intent:** Implement an in-memory version of the IBus interface.


## External dependencies
- @x/shared/dist/runs.js
- zod

## Flagged idioms
- Use of Map to manage subscribers allows efficient addition and removal of handlers.

## Behavioral notes
- Wildcard '*' subscribers receive all events regardless of runId.
