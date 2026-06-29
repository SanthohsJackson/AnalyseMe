# apps/cli/src/runs/lock.ts

**File:** apps/cli/src/runs/lock.ts  
**Language:** typescript

## Purpose
Manage locks for run identifiers in memory to prevent concurrent execution.

## Interfaces
### `IRunsLock` (class)
```
interface IRunsLock
```
**Intent:** Define the contract for locking and releasing run identifiers.


### `InMemoryRunsLock` (class)
```
class InMemoryRunsLock implements IRunsLock
```
**Intent:** Provide an in-memory implementation of the IRunsLock interface.


### `lock` (method)
```
lock(runId: string): Promise<boolean>
```
**Intent:** Attempt to acquire a lock for the specified run identifier.

**Inputs:**
- runId: string — the identifier of the run to lock
**Outputs:**
- Promise<boolean> — true if the lock was acquired, false if it was already locked
**Side effects:**
- Modifies the internal locks record to add a lock for the given runId

### `release` (method)
```
release(runId: string): Promise<void>
```
**Intent:** Release the lock for the specified run identifier.

**Inputs:**
- runId: string — the identifier of the run to release
**Outputs:**
- Promise<void> — no return value
**Side effects:**
- Modifies the internal locks record to remove the lock for the given runId

## Flagged idioms
- Use of a Record to manage locks in memory, which is a common pattern for simple in-memory state management.

## Behavioral notes
- The lock method returns false if the runId is already locked, indicating that the lock could not be acquired.
