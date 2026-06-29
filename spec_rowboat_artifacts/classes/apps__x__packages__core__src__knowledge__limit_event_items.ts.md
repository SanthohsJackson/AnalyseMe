# apps/x/packages/core/src/knowledge/limit_event_items.ts

**File:** apps/x/packages/core/src/knowledge/limit_event_items.ts  
**Language:** typescript

## Purpose
Limit the number of event items to a specified maximum, indicating if truncation occurred.

## Interfaces
### `limitEventItems` (function)
```
limitEventItems(items: string[], max: number = MAX_EVENT_ITEMS): { items: string[]; truncated: boolean }
```
**Intent:** Restrict the number of items in a list to a maximum, returning the truncated list and a flag indicating if truncation was necessary.

**Inputs:**
- items: string[] — the list of event items to limit
- max: number — the maximum number of items allowed (default is MAX_EVENT_ITEMS)
**Outputs:**
- { items: string[]; truncated: boolean } — the possibly truncated list of items and a flag indicating if truncation occurred

## Flagged idioms
- Default parameter value — provides a default maximum limit using a constant.

## Behavioral notes
- The function returns a flag indicating whether the list was truncated.
