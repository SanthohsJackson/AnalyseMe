# apps/x/packages/core/src/events/consumer.ts

**File:** apps/x/packages/core/src/events/consumer.ts  
**Language:** typescript

## Purpose
Defines interfaces for event consumers and their targets in an event processing system.

## Interfaces
### `EventConsumerTarget` (class)
```
interface EventConsumerTarget
```
**Intent:** Represents a target that an event consumer might fire on, with consumer-defined identifiers and criteria.


### `EventConsumerFireResult` (class)
```
interface EventConsumerFireResult
```
**Intent:** Represents the result of firing an event consumer on a target, including a run identifier and optional error.


### `EventConsumer` (class)
```
interface EventConsumer
```
**Intent:** Defines the contract for an event consumer, including methods for listing eligible targets, finding candidates, and firing on a candidate.


## External dependencies
- @x/shared/dist/events.js
