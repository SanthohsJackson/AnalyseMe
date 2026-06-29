# apps/cli/src/application/lib/id-gen.ts

**File:** apps/cli/src/application/lib/id-gen.ts  
**Language:** typescript

## Purpose
Generate a lexicographically sortable, ISO8601-based unique identifier string.

## Interfaces
### `IMonotonicallyIncreasingIdGenerator` (class)
```
interface IMonotonicallyIncreasingIdGenerator
```
**Intent:** Define a contract for generating monotonically increasing ID strings.


### `IdGen` (class)
```
class IdGen implements IMonotonicallyIncreasingIdGenerator
```
**Intent:** Implement the IMonotonicallyIncreasingIdGenerator interface to generate unique ID strings.


### `constructor` (method)
```
constructor()
```
**Intent:** Initialize the IdGen instance with process ID and an empty host tag.


### `next` (method)
```
async next() -> Promise<string>
```
**Intent:** Generate a unique ID string based on the current timestamp, process ID, and sequence number.

**Outputs:**
- Promise<string> — a unique, lexicographically sortable ID string

## External dependencies
- process

## Flagged idioms
- Use of ISO8601 format for generating sortable timestamps.

## Behavioral notes
- The sequence number increments if the current timestamp matches the last used timestamp, ensuring uniqueness.
