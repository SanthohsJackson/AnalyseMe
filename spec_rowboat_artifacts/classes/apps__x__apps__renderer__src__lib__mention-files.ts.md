# apps/x/apps/renderer/src/lib/mention-files.ts

**File:** apps/x/apps/renderer/src/lib/mention-files.ts  
**Language:** typescript

## Purpose
Build an ordered list of file paths with certain prefixes stripped, prioritizing active and recent files.

## Interfaces
### `buildMentionFileList` (function)
```
buildMentionFileList({ files, activePath, recentFiles }: BuildMentionFileListOptions) => string[]
```
**Intent:** Generate a list of file paths with duplicates removed and certain prefixes stripped, prioritizing active and recent files.

**Inputs:**
- files: string[] — list of file paths to process
- activePath: string | null — the currently active file path, if any
- recentFiles: string[] — list of recently accessed file paths, if any
**Outputs:**
- string[] — ordered list of normalized file paths

## Internal dependencies
- @/lib/wiki-links

## Flagged idioms
- Use of Set to track seen items and ensure uniqueness in the output list.

## Behavioral notes
- The function normalizes file paths by stripping a specific prefix before processing.
