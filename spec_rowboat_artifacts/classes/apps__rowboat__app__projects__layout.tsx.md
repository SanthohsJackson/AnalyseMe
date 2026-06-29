# apps/rowboat/app/projects/layout.tsx

**File:** apps/rowboat/app/projects/layout.tsx  
**Language:** typescript

## Purpose
Render a layout component with authentication and billing features.

## Interfaces
### `Layout` (function)
```
Layout({ children }: Readonly<{ children: React.ReactNode }>)
```
**Intent:** Wrap the provided children in an AppLayout component with authentication and billing features enabled.

**Inputs:**
- children: React.ReactNode — the content to be rendered within the layout
**Outputs:**
- JSX.Element — the rendered layout component

## Internal dependencies
- ./layout/components/app-layout

## External dependencies
- ../lib/feature_flags

## Flagged idioms
- Destructuring assignment in function parameters: simplifies access to properties of objects passed as arguments
