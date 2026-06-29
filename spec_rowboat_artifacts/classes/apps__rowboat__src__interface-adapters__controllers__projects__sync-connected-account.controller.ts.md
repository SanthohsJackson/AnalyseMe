# apps/rowboat/src/interface-adapters/controllers/projects/sync-connected-account.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/projects/sync-connected-account.controller.ts  
**Language:** typescript

## Purpose
This unit defines a controller for synchronizing a connected account with a project.

## Interfaces
### `ISyncConnectedAccountController` (class)
```
interface ISyncConnectedAccountController
```
**Intent:** Defines the contract for a controller that synchronizes a connected account.


### `SyncConnectedAccountController` (class)
```
class SyncConnectedAccountController implements ISyncConnectedAccountController
```
**Intent:** Implements the controller for synchronizing a connected account using a use case.


### `constructor` (method)
```
constructor({ syncConnectedAccountUseCase }: { syncConnectedAccountUseCase: ISyncConnectedAccountUseCase })
```
**Intent:** Initializes the controller with a use case for synchronizing connected accounts.

**Inputs:**
- syncConnectedAccountUseCase: ISyncConnectedAccountUseCase — the use case for synchronizing connected accounts

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<z.infer<typeof ComposioConnectedAccount>>
```
**Intent:** Validates the input and executes the synchronization of a connected account.

**Inputs:**
- request: z.infer<typeof inputSchema> — the input data for synchronizing a connected account
**Outputs:**
- Promise<z.infer<typeof ComposioConnectedAccount>> — the result of the synchronization
**Raises:**
- BadRequestError: when the request is invalid

## Internal dependencies
- @/src/application/use-cases/projects/sync-connected-account.use-case
- @/src/entities/errors/common
- @/src/entities/models/project

## External dependencies
- zod

## Flagged idioms
- Use of zod for input validation ensures type-safe request handling.

## Behavioral notes
- The execute method uses safeParse to validate input, which provides detailed error information if validation fails.
