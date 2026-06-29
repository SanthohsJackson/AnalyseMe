# apps/x/packages/core/src/analytics/usage.ts

**File:** apps/x/packages/core/src/analytics/usage.ts  
**Language:** typescript

## Purpose
Capture and report usage statistics for language model operations.

## Interfaces
### `captureLlmUsage` (function)
```
captureLlmUsage(args: CaptureLlmUsageArgs): void
```
**Intent:** Collect and send language model usage data to an analytics service for tracking purposes.

**Inputs:**
- args: CaptureLlmUsageArgs — the arguments containing usage details and metadata
**Side effects:**
- Sends usage data to an analytics service via the capture function

### `CaptureLlmUsageArgs` (class)
```
CaptureLlmUsageArgs
```
**Intent:** Define the structure of arguments required for capturing language model usage.


### `LlmUsageInput` (class)
```
LlmUsageInput
```
**Intent:** Define the structure for optional language model usage metrics.


## Internal dependencies
- ./posthog.js
- ./use_case.js

## Flagged idioms
- Use of optional chaining and nullish coalescing to handle undefined values gracefully.

## Behavioral notes
- The function defaults token counts to zero if not provided and calculates total tokens if not explicitly given.
