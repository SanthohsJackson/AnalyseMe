# apps/rowboat/src/interface-adapters/controllers/projects/get-composio-toolkit.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/projects/get-composio-toolkit.controller.ts  
**Language:** typescript

## Purpose
Handle requests to get a Composio toolkit by validating input and invoking the use case.

## Interfaces
### `IGetComposioToolkitController` (interface)
```
interface IGetComposioToolkitController
```
**Intent:** Define the contract for a controller that executes a request to get a Composio toolkit.


### `GetComposioToolkitController` (class)
```
class GetComposioToolkitController implements IGetComposioToolkitController
```
**Intent:** Implement the controller interface to handle requests for retrieving a Composio toolkit.


### `constructor` (method)
```
constructor({ getComposioToolkitUseCase }: { getComposioToolkitUseCase: IGetComposioToolkitUseCase })
```
**Intent:** Initialize the controller with the necessary use case for toolkit retrieval.

**Inputs:**
- getComposioToolkitUseCase: IGetComposioToolkitUseCase — the use case to execute toolkit retrieval

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<z.infer<typeof ZGetToolkitResponse>>
```
**Intent:** Validate the request and execute the use case to retrieve the toolkit.

**Inputs:**
- request: z.infer<typeof inputSchema> — the validated request object
**Outputs:**
- Promise<z.infer<typeof ZGetToolkitResponse>> — the response from the use case execution
**Raises:**
- BadRequestError: when the request validation fails

## Internal dependencies
- @/src/application/use-cases/projects/get-composio-toolkit.use-case
- @/src/application/lib/composio/types
- @/src/entities/errors/common

## External dependencies
- zod

## Flagged idioms
- Use of Zod for schema validation: ensures request data conforms to expected structure before processing.

## Behavioral notes
- The execute method uses safeParse to validate input, which provides detailed error information if validation fails.
