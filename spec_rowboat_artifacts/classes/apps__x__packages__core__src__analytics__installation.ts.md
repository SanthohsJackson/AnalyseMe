# apps/x/packages/core/src/analytics/installation.ts

**File:** apps/x/packages/core/src/analytics/installation.ts  
**Language:** typescript

## Purpose
Generate or retrieve a unique installation ID for analytics purposes.

## Interfaces
### `getInstallationId` (function)
```
getInstallationId() -> str
```
**Intent:** Ensure a consistent and unique installation ID is available for analytics, creating and storing it if necessary.

**Outputs:**
- str — a unique installation ID
**Side effects:**
- Reads from 'installation.json' file
- Writes to 'installation.json' file if it does not exist or lacks a valid ID
- Logs errors to the console

## Internal dependencies
- ../config/config.js

## External dependencies
- node:fs
- node:path
- node:crypto

## Flagged idioms
- Use of 'randomUUID()' to generate a unique identifier.

## Behavioral notes
- Caches the installation ID in memory after the first retrieval to avoid repeated file access.
- Creates the directory structure for the installation file if it does not exist.
