# apps/rowboat/app/projects/[projectId]/workflow/config_list.tsx

**File:** apps/rowboat/app/projects/[projectId]/workflow/config_list.tsx  
**Language:** typescript

## Purpose
Render a list of items with removable functionality in a React component.

## Interfaces
### `List` (function)
```
List({ items, onRemove }: { items: { id: string; node: React.ReactNode; }[]; onRemove: (id: string) => void; })
```
**Intent:** Render a list of items, each with a button to trigger a removal callback.

**Inputs:**
- items: { id: string; node: React.ReactNode; }[] — the list of items to display
- onRemove: (id: string) => void — callback to handle item removal
**Outputs:**
- JSX.Element — a rendered list of items

### `ListItem` (function)
```
ListItem({ children, onRemove }: { children: React.ReactNode; onRemove: () => void; })
```
**Intent:** Render a single list item with a button to trigger a removal callback.

**Inputs:**
- children: React.ReactNode — the content to display within the list item
- onRemove: () => void — callback to handle the removal of this item
**Outputs:**
- JSX.Element — a rendered list item with a remove button

## External dependencies
- lucide-react

## Flagged idioms
- React component pattern: using props to pass data and callbacks for rendering and interaction.

## Behavioral notes
- The remove button is only visible on hover due to the 'group-hover:block' class.
