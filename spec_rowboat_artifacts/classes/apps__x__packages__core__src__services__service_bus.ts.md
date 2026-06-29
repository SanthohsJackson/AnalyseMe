# apps/x/packages/core/src/services/service_bus.ts

**File:** apps/x/packages/core/src/services/service_bus.ts  
**Language:** typescript

## Purpose
Provide a simple publish-subscribe mechanism for handling service events.

## Interfaces
### `publish` (method)
```
publish(event: ServiceEventType) -> Promise<void>
```
**Intent:** Notify all subscribed handlers of a new event.

**Inputs:**
- event: ServiceEventType — the event to be published to all subscribers
**Outputs:**
- Promise<void> — resolves when all handlers have been invoked

### `subscribe` (method)
```
subscribe(handler: ServiceEventHandler) -> Promise<() => void>
```
**Intent:** Register a handler to be called when events are published, and provide a way to unsubscribe.

**Inputs:**
- handler: ServiceEventHandler — the function to be called when an event is published
**Outputs:**
- Promise<() => void> — resolves to an unsubscribe function
**Side effects:**
- Adds the handler to the list of subscribers

### `ServiceBus` (class)
```
class ServiceBus
```
**Intent:** Encapsulate the publish-subscribe logic for service events.


## External dependencies
- @x/shared/dist/service-events.js

## Flagged idioms
- Promise.all: used to handle asynchronous execution of multiple handlers

## Behavioral notes
- The unsubscribe function removes the handler from the subscribers list if it exists.
