# apps/rowboat/app/api/twilio/utils.ts

**File:** apps/rowboat/app/api/twilio/utils.ts  
**Language:** typescript

## Purpose
Provide utility functions for generating TwiML responses for Twilio interactions.

## Interfaces
### `XmlResponse` (function)
```
XmlResponse(content: TwiML)
```
**Intent:** Convert TwiML content into an HTTP response with XML content type.

**Inputs:**
- content: TwiML — the TwiML content to be converted to an XML response
**Outputs:**
- Response — an HTTP response with XML content

### `reject` (function)
```
reject(reason: VoiceResponse.RejectAttributes['reason'])
```
**Intent:** Generate a TwiML response to reject a call with a specified reason.

**Inputs:**
- reason: VoiceResponse.RejectAttributes['reason'] — the reason for rejecting the call
**Outputs:**
- Response — an HTTP response with XML content indicating call rejection

### `hangup` (function)
```
hangup()
```
**Intent:** Generate a TwiML response to hang up a call.

**Outputs:**
- Response — an HTTP response with XML content indicating call hangup

## External dependencies
- twilio
- zod

## Flagged idioms
- Use of TwiML and VoiceResponse from Twilio to construct XML responses for telephony applications.
