# apps/rowboat/app/projects/[projectId]/layout.tsx

**File:** apps/rowboat/app/projects/[projectId]/layout.tsx  
**Language:** typescript

## Purpose
Render the children components within a layout context for a specific project.

## Interfaces
### `Layout` (function)
```
Layout({ params, children }: { params: Promise<{ projectId: string }>, children: React.ReactNode })
```
**Intent:** Render the provided children components, presumably within a layout for a specific project identified by projectId.

**Inputs:**
- params: Promise<{ projectId: string }> — a promise resolving to an object containing the project ID
- children: React.ReactNode — the components to be rendered within the layout
**Outputs:**
- React.ReactNode — the children components
