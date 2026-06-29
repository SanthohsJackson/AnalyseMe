# apps/x/packages/core/src/knowledge/file-lock.ts

**File:** apps/x/packages/core/src/knowledge/file-lock.ts  
**Language:** typescript

## Purpose
Ensure exclusive access to a file path by queuing asynchronous operations.

## Interfaces
### `withFileLock` (function)
```
withFileLock<T>(absPath: string, fn: () => Promise<T>): Promise<T>
```
**Intent:** Queue and execute an asynchronous function with exclusive access to a specified file path.

**Inputs:**
- absPath: string — the absolute path to lock
- fn: () => Promise<T> — the asynchronous function to execute with the lock
**Outputs:**
- Promise<T> — the result of the asynchronous function
**Side effects:**
- Modifies the global 'locks' Map to manage file locks

## Flagged idioms
- Use of Promises to create a queue for asynchronous operations, ensuring sequential execution.

## Behavioral notes
- The lock is released only if the current lock is the last one set for the path, preventing premature deletion.
