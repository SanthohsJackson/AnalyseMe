# apps/rowboat/src/application/use-cases/composio-trigger-deployments/list-composio-trigger-types.use-case.ts

**File:** apps/rowboat/src/application/use-cases/composio-trigger-deployments/list-composio-trigger-types.use-case.ts  
**Language:** typescript

## Purpose
List available Composio trigger types with pagination support.

## Interfaces
### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<z.infer<ReturnType<typeof PaginatedList<typeof ComposioTriggerType>>>>
```
**Intent:** Fetch and return a paginated list of Composio trigger types based on the provided toolkitSlug and optional cursor.

**Inputs:**
- request: z.infer<typeof inputSchema> — an object containing toolkitSlug and an optional cursor
**Outputs:**
- Promise<z.infer<ReturnType<typeof PaginatedList<typeof ComposioTriggerType>>>> — a promise resolving to a paginated list of Composio trigger types
**Side effects:**
- Network request to fetch trigger types from the Composio API

### `ListComposioTriggerTypesUseCase` (class)
```
class ListComposioTriggerTypesUseCase implements IListComposioTriggerTypesUseCase
```
**Intent:** Provide an implementation for listing Composio trigger types.


### `IListComposioTriggerTypesUseCase` (class)
```
interface IListComposioTriggerTypesUseCase
```
**Intent:** Define the contract for listing Composio trigger types.


## Internal dependencies
- ../../lib/composio/composio

## External dependencies
- zod
- @/src/entities/common/paginated-list
- @/src/entities/models/composio-trigger-type

## Flagged idioms
- Use of zod for input validation ensures type-safe request handling.

## Behavioral notes
- The method execute makes a network call to list trigger types and returns a paginated result.
