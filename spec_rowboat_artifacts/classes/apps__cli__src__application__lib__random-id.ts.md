# apps/cli/src/application/lib/random-id.ts

**File:** apps/cli/src/application/lib/random-id.ts  
**Language:** typescript

## Purpose
Generate a random string ID using a custom alphabet.

## Interfaces
### `randomId` (function)
```
randomId() -> Promise<string>
```
**Intent:** Generate a random ID string of length 7 using a predefined alphabet.

**Outputs:**
- Promise<string> — a randomly generated string ID

## External dependencies
- nanoid

## Flagged idioms
- Use of 'customAlphabet' from 'nanoid' to create a custom ID generator.
