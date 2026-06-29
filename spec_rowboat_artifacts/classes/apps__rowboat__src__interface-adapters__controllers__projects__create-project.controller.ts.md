# apps/rowboat/src/interface-adapters/controllers/projects/create-project.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/projects/create-project.controller.ts  
**Language:** typescript

## Purpose
Handle the creation of a project by validating input and executing the use case.

## Interfaces
### `ICreateProjectController` (class)
```
interface ICreateProjectController
```
**Intent:** Define the contract for a controller that handles project creation.


### `CreateProjectController` (class)
```
class CreateProjectController implements ICreateProjectController
```
**Intent:** Implement the project creation controller using a use case.


### `constructor` (method)
```
constructor({ createProjectUseCase }: { createProjectUseCase: ICreateProjectUseCase })
```
**Intent:** Initialize the controller with the necessary use case.

**Inputs:**
- createProjectUseCase: ICreateProjectUseCase — the use case for creating a project

### `execute` (method)
```
async execute(request: z.infer<typeof InputSchema>): Promise<z.infer<typeof Project>>
```
**Intent:** Validate the input and execute the project creation use case.

**Inputs:**
- request: z.infer<typeof InputSchema> — the input data for creating a project
**Outputs:**
- Promise<z.infer<typeof Project>> — the created project
**Raises:**
- BadRequestError: when the input request is invalid

## Internal dependencies
- @/src/application/use-cases/projects/create-project.use-case
- @/src/entities/errors/common
- @/src/entities/models/project

## External dependencies
- zod

## Flagged idioms
- Use of Zod for input validation ensures type-safe parsing and error handling.

## Behavioral notes
- The input is validated using Zod's safeParse method, which provides structured error handling.
