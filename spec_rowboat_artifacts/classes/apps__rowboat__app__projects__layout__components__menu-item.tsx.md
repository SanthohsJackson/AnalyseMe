# apps/rowboat/app/projects/layout/components/menu-item.tsx

**File:** apps/rowboat/app/projects/layout/components/menu-item.tsx  
**Language:** typescript

## Purpose
Render a menu item component with an icon and optional children, supporting selected and collapsed states.

## Interfaces
### `MenuItem` (function)
```
MenuItem({ icon: LucideIcon, selected?: boolean, collapsed?: boolean, children?: React.ReactNode }): JSX.Element
```
**Intent:** Render a styled menu item with an icon and optional children, adjusting styles based on selection and collapse state.

**Inputs:**
- icon: LucideIcon — the icon component to display
- selected?: boolean — whether the menu item is selected
- collapsed?: boolean — whether the menu item is collapsed
- children?: React.ReactNode — the child elements to render inside the menu item
**Outputs:**
- JSX.Element — the rendered menu item component

## External dependencies
- lucide-react

## Flagged idioms
- Destructuring props in function parameters to directly access and set default values.

## Behavioral notes
- The component conditionally renders children based on the 'collapsed' prop.
