# apps/rowboat/src/interface-adapters/controllers/api-keys/list-api-keys.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/api-keys/list-api-keys.controller.ts  
**Language:** typescript

## Purpose
The ListApiKeysController handles requests to list API keys by validating input and delegating to a use case.

## Interfaces
### `IListApiKeysController` (interface)
```
interface IListApiKeysController
```
**Intent:** Defines the contract for a controller that lists API keys.


### `ListApiKeysController` (class)
```
class ListApiKeysController implements IListApiKeysController
```
**Intent:** Implements the IListApiKeysController interface to handle API key listing requests.


### `constructor` (method)
```
constructor({ listApiKeysUseCase }: { listApiKeysUseCase: IListApiKeysUseCase })
```
**Intent:** Initializes the ListApiKeysController with a use case for listing API keys.

**Inputs:**
- listApiKeysUseCase: IListApiKeysUseCase — the use case to execute API key listing

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<z.infer<typeof ApiKey>[]>
```
**Intent:** Validates the input request and executes the use case to list API keys.

**Inputs:**
- request: z.infer<typeof inputSchema> — the validated input for listing API keys
**Outputs:**
- Promise<z.infer<typeof ApiKey>[]> — a promise resolving to a list of API keys
**Raises:**
- BadRequestError: when the request validation fails

## Internal dependencies
- @/src/application/use-cases/api-keys/list-api-keys.use-case

## External dependencies
- zod

## Flagged idioms
- Use of Zod for input validation ensures type-safe request handling.

## Behavioral notes
- The execute method throws a BadRequestError if input validation fails.
