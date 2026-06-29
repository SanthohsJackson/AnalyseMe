# apps/x/packages/core/src/config/initConfigs.ts

**File:** apps/x/packages/core/src/config/initConfigs.ts  
**Language:** typescript

## Purpose
Initialize configuration files at application startup to ensure they exist before being accessed by the UI.

## Interfaces
### `initConfigs` (function)
```
initConfigs() -> Promise<void>
```
**Intent:** Ensure that all necessary configuration files and states are initialized at application startup.

**Outputs:**
- Promise<void> — resolves when all configuration files are ensured
**Side effects:**
- Ensures configuration files and state are initialized by calling ensureConfig and ensureState methods on various repositories

## Internal dependencies
- ../di/container.js
- ../models/repo.js
- ../mcp/repo.js
- ../agent-schedule/repo.js
- ../agent-schedule/state-repo.js
- ./security.js

## Flagged idioms
- Dependency injection via container.resolve to obtain repository instances

## Behavioral notes
- The function uses Promise.all to ensure all configuration and state initialization tasks are executed concurrently.
