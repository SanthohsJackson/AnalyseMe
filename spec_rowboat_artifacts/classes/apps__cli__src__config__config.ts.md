# apps/cli/src/config/config.ts

**File:** apps/cli/src/config/config.ts  
**Language:** typescript

## Purpose
Ensure necessary directories exist for the application to function properly.

## Interfaces
### `ensureDirs` (function)
```
ensureDirs()
```
**Intent:** Create the required directories for the application if they do not already exist.

**Side effects:**
- Creates directories if they do not exist: I/O operation on the filesystem

## External dependencies
- path
- fs
- os

## Flagged idioms
- Use of fs.existsSync and fs.mkdirSync with recursive option to ensure directory existence.

## Behavioral notes
- The function ensures the existence of the main working directory and two subdirectories ('agents' and 'config').
