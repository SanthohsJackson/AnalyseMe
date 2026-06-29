# apps/rowboatx/components/ai-elements/connection.tsx

**File:** apps/rowboatx/components/ai-elements/connection.tsx  
**Language:** typescript

## Purpose
Render a connection line and endpoint circle in an SVG graphic.

## Interfaces
### `Connection` (function)
```
Connection({ fromX, fromY, toX, toY })
```
**Intent:** Render an SVG path and circle to visually represent a connection between two points.

**Inputs:**
- fromX: number — the x-coordinate of the starting point
- fromY: number — the y-coordinate of the starting point
- toX: number — the x-coordinate of the ending point
- toY: number — the y-coordinate of the ending point

## External dependencies
- @xyflow/react

## Flagged idioms
- Use of JSX to define SVG elements for rendering in a React component.

## Behavioral notes
- The path uses a cubic Bezier curve to create a smooth connection between the points.
