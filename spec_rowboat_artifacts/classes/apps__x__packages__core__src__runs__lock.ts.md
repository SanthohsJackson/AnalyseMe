# apps/x/packages/core/src/runs/lock.ts

**File:** apps/x/packages/core/src/runs/lock.ts  
**Language:** typescript

## Purpose
Manage locks for run identifiers in memory to prevent concurrent operations.

## Interfaces
### `IRunsLock` (class)
```
interface IRunsLock
```
**Intent:** Define the contract for locking and releasing run identifiers.


### `lock` (method)
```
lock(runId: string): Promise<boolean>
```
**Intent:** Attempt to acquire a lock for a given run identifier.

**Inputs:**
- runId: string — the identifier of the run to lock
**Outputs:**
- Promise<boolean> — true if the lock was acquired, false if it was already locked
**Side effects:**
- Mutates the internal locks record by setting the runId to true if not already locked

### `release` (method)
```
release(runId: string): Promise<void>
```
**Intent:** Release the lock for a given run identifier.

**Inputs:**
- runId: string — the identifier of the run to release
**Outputs:**
- Promise<void> — no return value
**Side effects:**
- Mutates the internal locks record by deleting the runId

### `InMemoryRunsLock` (class)
```
class InMemoryRunsLock implements IRunsLock
```
**Intent:** Provide an in-memory implementation of the IRunsLock interface.


## Flagged idioms
- Use of a Record to manage locks in memory, which is a common pattern for simple in-memory key-value storage.

## Behavioral notes
- The lock method returns false if the runId is already locked, ensuring no duplicate locks.
