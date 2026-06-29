# apps/rowboat/src/interface-adapters/controllers/projects/remove-custom-mcp-server.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/projects/remove-custom-mcp-server.controller.ts  
**Language:** typescript

## Purpose
This unit defines a controller for removing a custom MCP server from a project, validating input and executing the use case.

## Interfaces
### `IRemoveCustomMcpServerController` (interface)
```
interface IRemoveCustomMcpServerController
```
**Intent:** Defines the contract for a controller that can execute the removal of a custom MCP server.


### `RemoveCustomMcpServerController` (class)
```
class RemoveCustomMcpServerController
```
**Intent:** Implements the controller interface to handle the removal of a custom MCP server by executing the use case.

**Inputs:**
- removeCustomMcpServerUseCase: IRemoveCustomMcpServerUseCase

### `constructor` (method)
```
constructor({ removeCustomMcpServerUseCase }: { removeCustomMcpServerUseCase: IRemoveCustomMcpServerUseCase })
```
**Intent:** Initializes the controller with the use case for removing a custom MCP server.

**Inputs:**
- removeCustomMcpServerUseCase: IRemoveCustomMcpServerUseCase

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<void>
```
**Intent:** Validates the input request and executes the use case to remove a custom MCP server.

**Inputs:**
- request: z.infer<typeof inputSchema> — the input data for the operation
**Outputs:**
- Promise<void> — resolves when the operation completes
**Raises:**
- BadRequestError: when the request validation fails

## Internal dependencies
- @/src/application/use-cases/projects/remove-custom-mcp-server.use-case

## External dependencies
- zod
- @/src/entities/errors/common

## Flagged idioms
- Use of Zod for input validation ensures type-safe request handling.

## Behavioral notes
- The execute method throws a BadRequestError if the input validation fails, ensuring only valid requests are processed.
