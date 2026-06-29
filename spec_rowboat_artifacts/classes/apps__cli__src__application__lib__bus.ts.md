# apps/cli/src/application/lib/bus.ts

**File:** apps/cli/src/application/lib/bus.ts  
**Language:** typescript

## Purpose
Provide an in-memory event bus for publishing and subscribing to events.

## Interfaces
### `publish` (method)
```
publish(event: z.infer<typeof RunEvent>): Promise<void>
```
**Intent:** Broadcast an event to all subscribers associated with the event's runId and to any global subscribers.

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
- runId: string — the identifier for the event run
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
**Intent:** Implement an in-memory version of the IBus interface for managing event subscriptions and notifications.


## Internal dependencies
- ../../entities/run-events.js

## External dependencies
- zod

## Flagged idioms
- Use of Map to manage collections of subscribers for efficient lookup and modification.

## Behavioral notes
- Subscribers for a specific runId and global subscribers (using '*') are both notified when an event is published.
