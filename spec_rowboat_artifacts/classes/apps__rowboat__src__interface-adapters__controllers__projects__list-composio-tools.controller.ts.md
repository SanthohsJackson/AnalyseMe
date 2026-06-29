# apps/rowboat/src/interface-adapters/controllers/projects/list-composio-tools.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/projects/list-composio-tools.controller.ts  
**Language:** typescript

## Purpose
This unit defines a controller for listing Composio tools, validating input, and executing the use case.

## Interfaces
### `IListComposioToolsController` (class)
```
interface IListComposioToolsController
```
**Intent:** Defines the contract for a controller that lists Composio tools.


### `ListComposioToolsController` (class)
```
class ListComposioToolsController implements IListComposioToolsController
```
**Intent:** Implements the controller for listing Composio tools using a provided use case.

**Inputs:**
- listComposioToolsUseCase: IListComposioToolsUseCase

### `constructor` (method)
```
constructor({ listComposioToolsUseCase }: { listComposioToolsUseCase: IListComposioToolsUseCase })
```
**Intent:** Initializes the controller with a specific use case for listing Composio tools.

**Inputs:**
- listComposioToolsUseCase: IListComposioToolsUseCase

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<z.infer<ReturnType<typeof ZListResponse<typeof ZTool>>>>
```
**Intent:** Validates the input request and executes the use case to list Composio tools.

**Inputs:**
- request: z.infer<typeof inputSchema>
**Outputs:**
- Promise<z.infer<ReturnType<typeof ZListResponse<typeof ZTool>>>>
**Raises:**
- BadRequestError: when the request is invalid

## Internal dependencies
- @/src/application/use-cases/projects/list-composio-tools.use-case
- @/src/application/lib/composio/types
- @/src/entities/errors/common

## External dependencies
- zod

## Flagged idioms
- Use of Zod for schema validation: ensures input data conforms to expected structure before processing.

## Behavioral notes
- The execute method uses safeParse to validate input, which provides detailed error information if validation fails.
