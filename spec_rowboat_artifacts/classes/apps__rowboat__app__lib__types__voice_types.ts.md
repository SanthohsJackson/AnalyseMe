# apps/rowboat/app/lib/types/voice_types.ts

**File:** apps/rowboat/app/lib/types/voice_types.ts  
**Language:** typescript

## Purpose
Define TypeScript interfaces and schemas for Twilio configuration and inbound call handling.

## Interfaces
### `TwilioConfigResponse` (class)
```
interface TwilioConfigResponse
```
**Intent:** Represents the response structure for Twilio configuration operations, indicating success or error.


### `InboundConfigResponse` (class)
```
interface InboundConfigResponse
```
**Intent:** Represents the response structure for inbound configuration operations, including status and potential errors.


## Internal dependencies
- ./types

## External dependencies
- zod

## Flagged idioms
- Use of 'zod' for schema validation, which provides a declarative way to define and validate data structures.
