# apps/rowboat/app/lib/components/pagination.tsx

**File:** apps/rowboat/app/lib/components/pagination.tsx  
**Language:** typescript

## Purpose
Render a pagination component that updates the URL based on the selected page.

## Interfaces
### `Pagination` (function)
```
Pagination({ total, page }: { total: number; page: number; })
```
**Intent:** Render a pagination UI component and update the URL when the page changes.

**Inputs:**
- total: number — the total number of pages
- page: number — the initial page to display
**Side effects:**
- Updates the browser's URL to reflect the current page

## External dependencies
- @heroui/react
- next/navigation

## Flagged idioms
- Using hooks from 'next/navigation' to manipulate the browser's URL based on component state.

## Behavioral notes
- The URL is updated with a query parameter 'page' to reflect the current page.
