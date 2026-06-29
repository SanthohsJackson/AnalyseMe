# apps/rowboat/app/lib/components/datasource-icon.tsx

**File:** apps/rowboat/app/lib/components/datasource-icon.tsx  
**Language:** typescript

## Purpose
Render an icon based on the type of data source and size specified.

## Interfaces
### `DataSourceIcon` (function)
```
DataSourceIcon({ type, size }: { type?: 'crawl' | 'urls' | 'files' | 'text' | undefined; size?: 'sm' | 'md'; })
```
**Intent:** Render a specific icon component based on the provided data source type and size.

**Inputs:**
- type?: 'crawl' | 'urls' | 'files' | 'text' | undefined — the type of data source to determine which icon to render
- size?: 'sm' | 'md' — the size of the icon to render
**Outputs:**
- JSX.Element — the rendered icon component

## External dependencies
- lucide-react

## Flagged idioms
- Conditional rendering using JSX to select components based on props.

## Behavioral notes
- If type is undefined, a default FileIcon is rendered.
