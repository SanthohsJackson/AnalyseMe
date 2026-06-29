# apps/rowboat/src/interface-adapters/controllers/api-keys/delete-api-key.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/api-keys/delete-api-key.controller.ts  
**Language:** typescript

## Purpose
Handles the deletion of API keys by validating input and invoking a use case.

## Interfaces
### `IDeleteApiKeyController` (class)
```
interface IDeleteApiKeyController
```
**Intent:** Defines the contract for a controller that deletes API keys.


### `DeleteApiKeyController` (class)
```
class DeleteApiKeyController implements IDeleteApiKeyController
```
**Intent:** Implements the IDeleteApiKeyController interface to handle API key deletion.

**Inputs:**
- deleteApiKeyUseCase: IDeleteApiKeyUseCase — the use case for deleting API keys

### `constructor` (method)
```
constructor({ deleteApiKeyUseCase }: { deleteApiKeyUseCase: IDeleteApiKeyUseCase })
```
**Intent:** Initializes the DeleteApiKeyController with a use case for deleting API keys.

**Inputs:**
- deleteApiKeyUseCase: IDeleteApiKeyUseCase — the use case for deleting API keys

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<boolean>
```
**Intent:** Validates the input and executes the API key deletion use case.

**Inputs:**
- request: z.infer<typeof inputSchema> — the input data for deleting an API key
**Outputs:**
- Promise<boolean> — the result of the API key deletion
**Raises:**
- BadRequestError: when the request validation fails

## Internal dependencies
- @/src/application/use-cases/api-keys/delete-api-key.use-case

## External dependencies
- zod
- @/src/entities/errors/common

## Flagged idioms
- Use of Zod for input validation ensures type-safe request handling.

## Behavioral notes
- The input is validated using Zod, and a BadRequestError is thrown if validation fails.
