# apps/rowboat/components/ui/page-header.tsx

**File:** apps/rowboat/components/ui/page-header.tsx  
**Language:** typescript

## Purpose
Render a page header with a title, optional description, and optional children components.

## Interfaces
### `PageHeader` (function)
```
PageHeader({ title, description, children }: PageHeaderProps)
```
**Intent:** Display a styled header section with a title, optional description, and optional additional content.

**Inputs:**
- title: string — the main title to display
- description?: string — an optional description to display under the title
- children?: React.ReactNode — optional React nodes to display alongside the title and description
**Side effects:**
- Renders a React component to the DOM

## External dependencies
- React

## Flagged idioms
- Conditional rendering using logical AND (&&) to display optional elements based on their presence.
