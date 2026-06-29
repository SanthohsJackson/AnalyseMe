# apps/rowboat/app/billing/layout.tsx

**File:** apps/rowboat/app/billing/layout.tsx  
**Language:** typescript

## Purpose
Render a layout component with authentication and billing features.

## Interfaces
### `Layout` (function)
```
Layout({ children }: Readonly<{ children: React.ReactNode }>)
```
**Intent:** Wrap the provided children in an AppLayout component with authentication and billing enabled.

**Inputs:**
- children: React.ReactNode — the content to be rendered within the layout
**Outputs:**
- JSX.Element — the rendered layout component

## Internal dependencies
- ../projects/layout/components/app-layout

## External dependencies
- react

## Flagged idioms
- Destructuring assignment in function parameters: simplifies access to props.
