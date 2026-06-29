# apps/cli/src/tui/index.tsx

**File:** apps/cli/src/tui/index.tsx  
**Language:** typescript

## Purpose
Render the RowboatTui component with a specified or default server URL.

## Interfaces
### `runTui` (function)
```
runTui({ serverUrl }: { serverUrl?: string })
```
**Intent:** Initialize and render the RowboatTui component with a server URL, defaulting to an environment variable or a local URL if not provided.

**Inputs:**
- serverUrl: string — optional server URL to use for the TUI
**Side effects:**
- Renders the RowboatTui component using the Ink library

## Internal dependencies
- ./ui.js

## External dependencies
- react
- ink

## Flagged idioms
- Destructuring assignment in function parameters: simplifies access to object properties

## Behavioral notes
- The server URL defaults to an environment variable or a local address if not provided.
