# apps/rowboat/app/lib/components/page-section.tsx

**File:** apps/rowboat/app/lib/components/page-section.tsx  
**Language:** typescript

## Purpose
Render a section of a page with a title and content, optionally styled as dangerous.

## Interfaces
### `PageSection` (function)
```
PageSection({ title, children, danger = false }: { title: string; children: React.ReactNode; danger?: boolean })
```
**Intent:** Render a section with a title and content, applying a 'danger' style if specified.

**Inputs:**
- title: string — the title of the section
- children: React.ReactNode — the content to display within the section
- danger?: boolean — optional flag to style the section as dangerous

## Flagged idioms
- Conditional class names in JSX: used to apply different styles based on the 'danger' flag.

## Behavioral notes
- The 'danger' flag changes the text and border color to red if true.
