# apps/rowboat/src/infrastructure/services/redis.cache.service.ts

**File:** apps/rowboat/src/infrastructure/services/redis.cache.service.ts  
**Language:** typescript

## Purpose
Provide caching services using Redis as the backend.

## Interfaces
### `RedisCacheService` (class)
```
class RedisCacheService implements ICacheService
```
**Intent:** Defines a service for interacting with a Redis cache.


### `get` (method)
```
get(key: string): Promise<string | null>
```
**Intent:** Retrieve a value from the Redis cache by its key.

**Inputs:**
- key: string — the key to retrieve from the cache
**Outputs:**
- Promise<string | null> — the value associated with the key, or null if not found

### `set` (method)
```
set(key: string, value: string, ttl?: number): Promise<void>
```
**Intent:** Store a value in the Redis cache with an optional expiration time.

**Inputs:**
- key: string — the key to set in the cache
- value: string — the value to associate with the key
- ttl?: number — optional time-to-live for the cache entry
**Outputs:**
- Promise<void> — resolves when the operation is complete

### `delete` (method)
```
delete(key: string): Promise<boolean>
```
**Intent:** Remove a key and its associated value from the Redis cache.

**Inputs:**
- key: string — the key to delete from the cache
**Outputs:**
- Promise<boolean> — true if the key was deleted, false otherwise

## Internal dependencies
- @/src/application/services/cache.service.interface
- @/app/lib/redis

## Flagged idioms
- Use of async/await for handling asynchronous operations with Redis.
