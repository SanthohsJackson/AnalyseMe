# apps/rowboat/src/application/services/cache.service.interface.ts

**File:** apps/rowboat/src/application/services/cache.service.interface.ts  
**Language:** typescript

## Purpose
Define the contract for cache service implementations with methods for storing, retrieving, and deleting cached data.

## Interfaces
### `ICacheService` (class)
```
interface ICacheService
```
**Intent:** Provide a standard interface for cache operations including get, set, and delete methods.


### `get` (method)
```
get(key: string): Promise<string | null>
```
**Intent:** Retrieve a value from the cache using its key.

**Inputs:**
- key: string — The unique identifier for the cached item
**Outputs:**
- Promise<string | null> — Resolves to the cached value as a string, or null if the key doesn't exist or has expired

### `set` (method)
```
set(key: string, value: string, ttl?: number): Promise<void>
```
**Intent:** Store a value in the cache with an optional time-to-live.

**Inputs:**
- key: string — The unique identifier for the cached item
- value: string — The value to cache
- ttl?: number — Time-to-live in seconds
**Outputs:**
- Promise<void> — Resolves when the value has been successfully stored

### `delete` (method)
```
delete(key: string): Promise<boolean>
```
**Intent:** Remove a cached item by its key.

**Inputs:**
- key: string — The unique identifier of the cached item to remove
**Outputs:**
- Promise<boolean> — Resolves to true if the item was successfully deleted, false if the key didn't exist
