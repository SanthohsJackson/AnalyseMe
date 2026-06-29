# apps/rowboat/app/projects/[projectId]/copilot/use-parsed-blocks.tsx

**File:** apps/rowboat/app/projects/[projectId]/copilot/use-parsed-blocks.tsx  
**Language:** typescript

## Purpose
Parse markdown text into blocks of text and code, and provide a memoized hook for parsed blocks.

## Interfaces
### `parseMarkdown` (function)
```
parseMarkdown(markdown: string) -> Block[]
```
**Intent:** Split markdown text into blocks of text and code based on specific markers.

**Inputs:**
- markdown: string — the markdown text to parse
**Outputs:**
- Block[] — an array of parsed blocks, each being either text or code

### `useParsedBlocks` (function)
```
useParsedBlocks(text: string) -> Block[]
```
**Intent:** Provide a memoized version of parsed markdown blocks for React components.

**Inputs:**
- text: string — the text to parse and memoize
**Outputs:**
- Block[] — a memoized array of parsed blocks

## External dependencies
- react

## Flagged idioms
- useMemo: used to memoize the result of parsing to optimize performance in React components

## Behavioral notes
- The function parseMarkdown distinguishes code blocks by a specific marker 'copilot_change\n'.
