# apps/rowboat/components/ui/page-heading.tsx

**File:** apps/rowboat/components/ui/page-heading.tsx  
**Language:** typescript

## Purpose
Render a page heading with a title and optional description using styled typography.

## Interfaces
### `PageHeading` (function)
```
PageHeading({ title, description }: PageHeadingProps)
```
**Intent:** Display a styled page heading with a title and optional description.

**Inputs:**
- title: string — the main heading text
- description?: string — optional subheading text
**Side effects:**
- Renders HTML elements with styled classes

## External dependencies
- clsx
- @/app/styles/design-tokens

## Flagged idioms
- Use of clsx for conditional className construction: simplifies dynamic class assignment

## Behavioral notes
- The description paragraph is only rendered if a description is provided.
