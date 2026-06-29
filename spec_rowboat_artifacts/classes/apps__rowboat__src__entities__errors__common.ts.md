# apps/rowboat/src/entities/errors/common.ts

**File:** apps/rowboat/src/entities/errors/common.ts  
**Language:** typescript

## Purpose
Define custom error classes for handling specific error scenarios in the application.

## Interfaces
### `BillingError` (method)
```
constructor(message?: string, options?: ErrorOptions)
```
**Intent:** Initialize a BillingError instance with an optional message and options.

**Inputs:**
- message?: string — optional error message
- options?: ErrorOptions — optional error options

### `QuotaExceededError` (method)
```
constructor(message?: string, options?: ErrorOptions)
```
**Intent:** Initialize a QuotaExceededError instance with an optional message and options.

**Inputs:**
- message?: string — optional error message
- options?: ErrorOptions — optional error options

### `BadRequestError` (method)
```
constructor(message?: string, options?: ErrorOptions)
```
**Intent:** Initialize a BadRequestError instance with an optional message and options.

**Inputs:**
- message?: string — optional error message
- options?: ErrorOptions — optional error options

### `NotFoundError` (method)
```
constructor(message?: string, options?: ErrorOptions)
```
**Intent:** Initialize a NotFoundError instance with an optional message and options.

**Inputs:**
- message?: string — optional error message
- options?: ErrorOptions — optional error options

### `NotAuthorizedError` (method)
```
constructor(message?: string, options?: ErrorOptions)
```
**Intent:** Initialize a NotAuthorizedError instance with an optional message and options.

**Inputs:**
- message?: string — optional error message
- options?: ErrorOptions — optional error options

## Flagged idioms
- Extending the built-in Error class to create custom error types.
