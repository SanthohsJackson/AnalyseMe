# apps/rowboatx/components/markdown-viewer.tsx

**File:** apps/rowboatx/components/markdown-viewer.tsx  
**Language:** typescript

## Purpose
Render markdown content as HTML using React components.

## Interfaces
### `MarkdownViewer` (function)
```
MarkdownViewer({ content }: MarkdownViewerProps)
```
**Intent:** Display markdown content as HTML within a styled container.

**Inputs:**
- content: string — the markdown content to render
**Side effects:**
- Renders HTML content to the DOM

## External dependencies
- react-markdown
- remark-gfm

## Flagged idioms
- Use of ReactMarkdown component to render markdown: leverages React for dynamic content rendering

## Behavioral notes
- The component applies GitHub Flavored Markdown (GFM) extensions via remark-gfm.
