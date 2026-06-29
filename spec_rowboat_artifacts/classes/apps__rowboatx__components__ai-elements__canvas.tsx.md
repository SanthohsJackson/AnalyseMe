# apps/rowboatx/components/ai-elements/canvas.tsx

**File:** apps/rowboatx/components/ai-elements/canvas.tsx  
**Language:** typescript

## Purpose
Render a ReactFlow canvas with optional children and specific interaction settings.

## Interfaces
### `Canvas` (function)
```
Canvas({ children, ...props }: CanvasProps)
```
**Intent:** Render a ReactFlow component with a background and optional children, configured with specific interaction properties.

**Inputs:**
- children: ReactNode — optional elements to render within the canvas
- props: CanvasProps — additional properties for ReactFlow

## External dependencies
- @xyflow/react
- react

## Flagged idioms
- Spread operator (...) is used to pass additional props to the ReactFlow component, allowing for flexible configuration.

## Behavioral notes
- The canvas disables panning on drag and zoom on double-click, and enables selection on drag.
