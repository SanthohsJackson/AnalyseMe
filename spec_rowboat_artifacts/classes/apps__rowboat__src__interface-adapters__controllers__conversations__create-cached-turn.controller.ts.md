# apps/rowboat/src/interface-adapters/controllers/conversations/create-cached-turn.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/conversations/create-cached-turn.controller.ts  
**Language:** typescript

## Purpose
Handle the creation of a cached turn in a conversation by validating input and invoking a use case.

## Interfaces
### `ICreateCachedTurnController` (class)
```
interface ICreateCachedTurnController
```
**Intent:** Define the contract for a controller that creates a cached turn.


### `CreateCachedTurnController` (class)
```
class CreateCachedTurnController implements ICreateCachedTurnController
```
**Intent:** Implement the controller for creating a cached turn, using a specified use case.

**Inputs:**
- createCachedTurnUseCase: ICreateCachedTurnUseCase

### `constructor` (method)
```
constructor({ createCachedTurnUseCase }: { createCachedTurnUseCase: ICreateCachedTurnUseCase })
```
**Intent:** Initialize the controller with a use case for creating cached turns.

**Inputs:**
- createCachedTurnUseCase: ICreateCachedTurnUseCase

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<{ key: string }>
```
**Intent:** Validate the input request and execute the use case to create a cached turn.

**Inputs:**
- request: z.infer<typeof inputSchema>
**Outputs:**
- Promise<{ key: string }>
**Raises:**
- BadRequestError: when the request is invalid

## Internal dependencies
- @/src/application/use-cases/conversations/create-cached-turn.use-case

## External dependencies
- zod

## Flagged idioms
- Use of Zod for input validation: ensures request data conforms to expected schema before processing.

## Behavioral notes
- The execute method throws a BadRequestError if the input validation fails.
