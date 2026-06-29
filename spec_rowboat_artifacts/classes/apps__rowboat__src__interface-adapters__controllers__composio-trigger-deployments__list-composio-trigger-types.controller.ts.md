# apps/rowboat/src/interface-adapters/controllers/composio-trigger-deployments/list-composio-trigger-types.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/composio-trigger-deployments/list-composio-trigger-types.controller.ts  
**Language:** typescript

## Purpose
Handle requests to list Composio trigger types with pagination support.

## Interfaces
### `IListComposioTriggerTypesController` (interface)
```
interface IListComposioTriggerTypesController
```
**Intent:** Define the contract for controllers that list Composio trigger types.


### `ListComposioTriggerTypesController` (class)
```
class ListComposioTriggerTypesController implements IListComposioTriggerTypesController
```
**Intent:** Implement the controller to handle listing of Composio trigger types.


### `constructor` (method)
```
constructor({ listComposioTriggerTypesUseCase }: { listComposioTriggerTypesUseCase: IListComposioTriggerTypesUseCase })
```
**Intent:** Initialize the controller with the necessary use case for listing trigger types.

**Inputs:**
- listComposioTriggerTypesUseCase: IListComposioTriggerTypesUseCase — the use case to execute listing

### `execute` (method)
```
async execute(request: z.infer<typeof inputSchema>): Promise<z.infer<ReturnType<typeof PaginatedList<typeof ComposioTriggerType>>>>
```
**Intent:** Validate the request and execute the use case to list Composio trigger types.

**Inputs:**
- request: z.infer<typeof inputSchema> — the input request containing toolkitSlug and optional cursor
**Outputs:**
- Promise<z.infer<ReturnType<typeof PaginatedList<typeof ComposioTriggerType>>>> — a paginated list of Composio trigger types
**Raises:**
- BadRequestError: when the request is invalid

## Internal dependencies
- @/src/application/use-cases/composio-trigger-deployments/list-composio-trigger-types.use-case
- @/src/entities/errors/common
- @/src/entities/models/composio-trigger-type
- @/src/entities/common/paginated-list

## External dependencies
- zod

## Flagged idioms
- Use of Zod for input validation ensures type-safe request parsing.

## Behavioral notes
- The execute method throws a BadRequestError if the input validation fails.
