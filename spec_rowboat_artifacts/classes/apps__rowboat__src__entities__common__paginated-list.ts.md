# apps/rowboat/src/entities/common/paginated-list.ts

**File:** apps/rowboat/src/entities/common/paginated-list.ts  
**Language:** typescript

## Purpose
Define a schema for a paginated list using Zod.

## Interfaces
### `PaginatedList` (function)
```
PaginatedList<T extends z.ZodTypeAny>(schema: T)
```
**Intent:** Create a Zod schema for a paginated list structure with items and an optional next cursor.

**Inputs:**
- schema: T — a Zod schema for the items in the list
**Outputs:**
- z.ZodObject — a Zod object schema with items and nextCursor

## External dependencies
- zod

## Flagged idioms
- Generic function with type constraint to ensure schema compatibility.
