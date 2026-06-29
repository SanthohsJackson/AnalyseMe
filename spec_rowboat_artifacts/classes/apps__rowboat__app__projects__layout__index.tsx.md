# apps/rowboat/app/projects/layout/index.tsx

**File:** apps/rowboat/app/projects/layout/index.tsx  
**Language:** typescript

## Purpose
Render a layout component for a project with children components.

## Interfaces
### `Layout` (function)
```
Layout({ params, children }: { params: { projectId: string }, children: React.ReactNode })
```
**Intent:** Render the AppLayout component with the provided children.

**Inputs:**
- params: { projectId: string } — parameters including the project ID
- children: React.ReactNode — the child components to render within the layout
**Outputs:**
- JSX.Element — the rendered layout component

## Internal dependencies
- ./components/app-layout

## External dependencies
- @/app/lib/feature_flags

## Flagged idioms
- Destructuring assignment in function parameters: simplifies access to nested properties.
