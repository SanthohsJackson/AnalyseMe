# apps/rowboat/src/interface-adapters/controllers/projects/create-custom-connected-account.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/projects/create-custom-connected-account.controller.ts  
**Language:** typescript

## Purpose
Handle the creation of a custom connected account by validating input and invoking a use case.

## Interfaces
### `ICreateCustomConnectedAccountController` (class)
```
interface ICreateCustomConnectedAccountController
```
**Intent:** Define the contract for a controller that executes the creation of a custom connected account.


### `CreateCustomConnectedAccountController` (class)
```
class CreateCustomConnectedAccountController implements ICreateCustomConnectedAccountController
```
**Intent:** Implement the controller interface to manage the creation of a custom connected account.

**Inputs:**
- createCustomConnectedAccountUseCase: ICreateCustomConnectedAccountUseCase

### `constructor` (method)
```
constructor({ createCustomConnectedAccountUseCase }: { createCustomConnectedAccountUseCase: ICreateCustomConnectedAccountUseCase })
```
**Intent:** Initialize the controller with a use case for creating custom connected accounts.

**Inputs:**
- createCustomConnectedAccountUseCase: ICreateCustomConnectedAccountUseCase

### `execute` (method)
```
async execute(request: z.infer<typeof inputSchema>): Promise<z.infer<typeof ZCreateConnectedAccountResponse>>
```
**Intent:** Validate the input request and execute the use case to create a custom connected account.

**Inputs:**
- request: z.infer<typeof inputSchema> — the input data for creating a connected account
**Outputs:**
- Promise<z.infer<typeof ZCreateConnectedAccountResponse>> — the response from the use case execution
**Raises:**
- BadRequestError: when the request validation fails

## Internal dependencies
- @/src/application/use-cases/projects/create-custom-connected-account.use-case
- @/src/entities/errors/common
- @/src/application/lib/composio/types

## External dependencies
- zod

## Flagged idioms
- Use of Zod for schema validation: ensures input data conforms to expected structure before processing.

## Behavioral notes
- The execute method uses safeParse to validate input, which provides a success flag and error details.
