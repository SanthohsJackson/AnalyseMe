# apps/rowboat/src/interface-adapters/controllers/projects/delete-project.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/projects/delete-project.controller.ts  
**Language:** typescript

## Purpose
Handle the deletion of a project by validating input and executing the corresponding use case.

## Interfaces
### `IDeleteProjectController` (class)
```
interface IDeleteProjectController
```
**Intent:** Define the contract for a controller that deletes a project.


### `DeleteProjectController` (class)
```
class DeleteProjectController implements IDeleteProjectController
```
**Intent:** Implement the IDeleteProjectController interface to handle project deletion.

**Inputs:**
- deleteProjectUseCase: IDeleteProjectUseCase

### `constructor` (method)
```
constructor({ deleteProjectUseCase }: { deleteProjectUseCase: IDeleteProjectUseCase })
```
**Intent:** Initialize the DeleteProjectController with a use case for deleting projects.

**Inputs:**
- deleteProjectUseCase: IDeleteProjectUseCase

### `execute` (method)
```
execute(request: z.infer<typeof InputSchema>): Promise<void>
```
**Intent:** Validate the input request and execute the delete project use case.

**Inputs:**
- request: z.infer<typeof InputSchema>
**Outputs:**
- Promise<void>
**Raises:**
- BadRequestError: when the request is invalid

## Internal dependencies
- @/src/application/use-cases/projects/delete-project.use-case

## External dependencies
- zod
- @/src/entities/errors/common

## Flagged idioms
- Dependency Injection: The use case is injected into the controller via the constructor, promoting loose coupling and testability.
- Zod for Validation: Zod is used to validate the input schema, ensuring the request meets expected structure before processing.

## Behavioral notes
- The execute method uses Zod's safeParse to validate input, which provides a success flag and error details if validation fails.
