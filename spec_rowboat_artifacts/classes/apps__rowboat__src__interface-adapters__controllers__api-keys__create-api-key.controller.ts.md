# apps/rowboat/src/interface-adapters/controllers/api-keys/create-api-key.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/api-keys/create-api-key.controller.ts  
**Language:** typescript

## Purpose
Handle the creation of API keys by validating input and invoking the use case.

## Interfaces
### `ICreateApiKeyController` (class)
```
interface ICreateApiKeyController
```
**Intent:** Define the contract for a controller that creates API keys.


### `CreateApiKeyController` (class)
```
class CreateApiKeyController implements ICreateApiKeyController
```
**Intent:** Implement the API key creation controller using a specified use case.

**Inputs:**
- createApiKeyUseCase: ICreateApiKeyUseCase

### `constructor` (method)
```
constructor({ createApiKeyUseCase }: { createApiKeyUseCase: ICreateApiKeyUseCase })
```
**Intent:** Initialize the controller with a specific API key creation use case.

**Inputs:**
- createApiKeyUseCase: ICreateApiKeyUseCase

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<z.infer<typeof ApiKey>>
```
**Intent:** Validate the input request and execute the API key creation use case.

**Inputs:**
- request: z.infer<typeof inputSchema>
**Outputs:**
- Promise<z.infer<typeof ApiKey>>
**Raises:**
- BadRequestError: when the request is invalid

## Internal dependencies
- @/src/application/use-cases/api-keys/create-api-key.use-case

## External dependencies
- zod

## Flagged idioms
- Use of Zod for input validation ensures type-safe request handling.

## Behavioral notes
- The input is validated using Zod before proceeding with the use case execution.
