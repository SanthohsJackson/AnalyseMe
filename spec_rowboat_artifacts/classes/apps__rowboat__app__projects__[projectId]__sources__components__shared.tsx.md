# apps/rowboat/app/projects/[projectId]/sources/components/shared.tsx

**File:** apps/rowboat/app/projects/[projectId]/sources/components/shared.tsx  
**Language:** typescript

## Purpose
Provide React components for displaying table labels, table values, and a list of URLs.

## Interfaces
### `UrlList` (function)
```
UrlList({ urls }: { urls: string })
```
**Intent:** Render a preformatted block containing a list of URLs.

**Inputs:**
- urls: string — the URLs to display
**Outputs:**
- JSX.Element — a preformatted block displaying the URLs

### `TableLabel` (function)
```
TableLabel({ children, className }: { children: React.ReactNode, className?: string })
```
**Intent:** Render a styled table header cell.

**Inputs:**
- children: React.ReactNode — the content of the table header
- className?: string — additional CSS classes
**Outputs:**
- JSX.Element — a table header cell with styled content

### `TableValue` (function)
```
TableValue({ children, className }: { children: React.ReactNode, className?: string })
```
**Intent:** Render a styled table cell.

**Inputs:**
- children: React.ReactNode — the content of the table cell
- className?: string — additional CSS classes
**Outputs:**
- JSX.Element — a table cell with styled content

## Flagged idioms
- React component pattern: using functional components to encapsulate UI elements
