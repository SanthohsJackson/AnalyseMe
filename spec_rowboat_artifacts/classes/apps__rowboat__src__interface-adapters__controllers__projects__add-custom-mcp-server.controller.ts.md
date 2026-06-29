# apps/rowboat/src/interface-adapters/controllers/projects/add-custom-mcp-server.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/projects/add-custom-mcp-server.controller.ts  
**Language:** typescript

## Purpose
Handle the addition of a custom MCP server to a project by validating input and invoking a use case.

## Interfaces
### `AddCustomMcpServerController` (class)
```
class AddCustomMcpServerController
```
**Intent:** Encapsulate the logic for adding a custom MCP server to a project.


### `IAddCustomMcpServerController` (class)
```
interface IAddCustomMcpServerController
```
**Intent:** Define the contract for controllers that handle adding custom MCP servers.


### `constructor` (method)
```
constructor({ addCustomMcpServerUseCase }: { addCustomMcpServerUseCase: IAddCustomMcpServerUseCase })
```
**Intent:** Initialize the controller with the necessary use case for adding a custom MCP server.

**Inputs:**
- addCustomMcpServerUseCase: IAddCustomMcpServerUseCase — the use case to execute the addition

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<void>
```
**Intent:** Validate the input request and execute the use case to add a custom MCP server.

**Inputs:**
- request: z.infer<typeof inputSchema> — the input data for adding a custom MCP server
**Outputs:**
- Promise<void> — resolves when the operation is complete
**Raises:**
- BadRequestError: when the request validation fails

## Internal dependencies
- @/src/application/use-cases/projects/add-custom-mcp-server.use-case
- @/src/entities/errors/common
- @/src/entities/models/project

## External dependencies
- zod

## Flagged idioms
- Use of Zod for input validation: ensures that the request data conforms to the expected schema before processing.

## Behavioral notes
- The execute method uses safeParse from Zod to validate input, which provides detailed error information if validation fails.
