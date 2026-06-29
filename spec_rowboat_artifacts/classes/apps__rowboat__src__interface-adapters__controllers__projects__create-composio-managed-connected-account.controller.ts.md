# apps/rowboat/src/interface-adapters/controllers/projects/create-composio-managed-connected-account.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/projects/create-composio-managed-connected-account.controller.ts  
**Language:** typescript

## Purpose
Handle the creation of a Composio managed connected account by validating input and invoking a use case.

## Interfaces
### `ICreateComposioManagedConnectedAccountController` (class)
```
interface ICreateComposioManagedConnectedAccountController
```
**Intent:** Define the contract for a controller that creates a Composio managed connected account.


### `CreateComposioManagedConnectedAccountController` (class)
```
class CreateComposioManagedConnectedAccountController implements ICreateComposioManagedConnectedAccountController
```
**Intent:** Implement the controller interface to manage the creation of a Composio managed connected account.

**Inputs:**
- createComposioManagedConnectedAccountUseCase: ICreateComposioManagedConnectedAccountUseCase

### `constructor` (method)
```
constructor({ createComposioManagedConnectedAccountUseCase }: { createComposioManagedConnectedAccountUseCase: ICreateComposioManagedConnectedAccountUseCase })
```
**Intent:** Initialize the controller with a use case for creating a Composio managed connected account.

**Inputs:**
- createComposioManagedConnectedAccountUseCase: ICreateComposioManagedConnectedAccountUseCase

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<z.infer<typeof ZCreateConnectedAccountResponse>>
```
**Intent:** Validate the input request and execute the use case to create a connected account.

**Inputs:**
- request: z.infer<typeof inputSchema> — the input data for creating a connected account
**Outputs:**
- Promise<z.infer<typeof ZCreateConnectedAccountResponse>> — the response from the use case execution
**Raises:**
- BadRequestError: when the request validation fails

## Internal dependencies
- @/src/application/use-cases/projects/create-composio-managed-connected-account.use-case
- @/src/entities/errors/common
- @/src/application/lib/composio/types

## External dependencies
- zod

## Flagged idioms
- Use of Zod for input validation: ensures that the request data conforms to the expected schema before processing.

## Behavioral notes
- The execute method uses safeParse to validate input, which provides detailed error information if validation fails.
