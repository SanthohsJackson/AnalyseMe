# apps/rowboat/src/interface-adapters/controllers/projects/update-project-name.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/projects/update-project-name.controller.ts  
**Language:** typescript

## Purpose
Handle the updating of a project's name by validating input and executing the corresponding use case.

## Interfaces
### `IUpdateProjectNameController` (class)
```
interface IUpdateProjectNameController
```
**Intent:** Define the contract for a controller that updates a project's name.


### `UpdateProjectNameController` (class)
```
class UpdateProjectNameController implements IUpdateProjectNameController
```
**Intent:** Implement the controller interface to update a project's name using a use case.


### `constructor` (method)
```
constructor({ updateProjectNameUseCase }: { updateProjectNameUseCase: IUpdateProjectNameUseCase })
```
**Intent:** Initialize the controller with the necessary use case for updating project names.

**Inputs:**
- updateProjectNameUseCase: IUpdateProjectNameUseCase — the use case to execute for updating project names

### `execute` (method)
```
async execute(request: z.infer<typeof InputSchema>): Promise<void>
```
**Intent:** Validate the input request and execute the use case to update the project name.

**Inputs:**
- request: z.infer<typeof InputSchema> — the input data for updating a project name
**Outputs:**
- Promise<void> — resolves when the operation completes
**Raises:**
- BadRequestError: when the input request is invalid

## Internal dependencies
- @/src/application/use-cases/projects/update-project-name.use-case

## External dependencies
- zod
- @/src/entities/errors/common

## Flagged idioms
- Use of Zod for input validation: ensures input data conforms to expected schema before processing.

## Behavioral notes
- The execute method throws a BadRequestError if the input validation fails, preventing further processing.
