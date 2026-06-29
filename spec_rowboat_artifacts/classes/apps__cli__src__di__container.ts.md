# apps/cli/src/di/container.ts

**File:** apps/cli/src/di/container.ts  
**Language:** typescript

## Purpose
Configure and register dependencies in a DI container for use in the application.

## Internal dependencies
- ../models/repo.js
- ../mcp/repo.js
- ../agents/repo.js
- ../runs/repo.js
- ../application/lib/id-gen.js
- ../application/lib/message-queue.js
- ../application/lib/bus.js
- ../runs/lock.js
- ../agents/runtime.js

## External dependencies
- awilix

## Flagged idioms
- Dependency Injection: The code uses a DI container to manage and inject dependencies, promoting loose coupling and easier testing.

## Behavioral notes
- The container is configured with strict mode, which enforces stricter checks on dependency resolution.
- All registered dependencies are configured as singletons, ensuring a single instance is used throughout the application.
