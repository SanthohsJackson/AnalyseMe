# apps/rowboat/app/lib/components/menu-item.tsx

**File:** apps/rowboat/app/lib/components/menu-item.tsx  
**Language:** typescript

## Purpose
Render a button component with customizable icon, text, and selection state.

## Interfaces
### `MenuItemProps` (class)
```
interface MenuItemProps
```
**Intent:** Define the properties required by the MenuItem component.

**Inputs:**
- icon: React.ReactNode — the icon to display in the menu item
- children: React.ReactNode — the content to display in the menu item
- selected: boolean — whether the menu item is selected
- onClick: () => void — the function to call when the menu item is clicked

## External dependencies
- react
- clsx

## Flagged idioms
- React functional component: used to define a UI component with props.

## Behavioral notes
- The button's appearance changes based on the 'selected' prop using conditional class names.
