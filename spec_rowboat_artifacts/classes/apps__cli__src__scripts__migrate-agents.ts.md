# apps/cli/src/scripts/migrate-agents.ts

**File:** apps/cli/src/scripts/migrate-agents.ts  
**Language:** typescript

## Purpose
Migrate agent data from JSON files to a repository.

## Internal dependencies
- ../agents/agents.js
- ../agents/repo.js
- ../config/config.js
- ../di/container.js

## External dependencies
- node:fs/promises
- path

## Flagged idioms
- Use of async/await for handling asynchronous operations: ensures non-blocking execution while reading files and interacting with the repository.

## Behavioral notes
- The script logs errors to the console if parsing a JSON file fails, but continues processing other files.
