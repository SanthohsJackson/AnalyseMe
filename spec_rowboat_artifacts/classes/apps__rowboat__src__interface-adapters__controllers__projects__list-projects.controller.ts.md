# apps/rowboat/src/interface-adapters/controllers/projects/list-projects.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/projects/list-projects.controller.ts  
**Language:** typescript

## Purpose
Handle the listing of projects by validating input and executing the use case.

## Interfaces
### `IListProjectsController` (class)
```
interface IListProjectsController
```
**Intent:** Define the contract for a controller that lists projects.


### `ListProjectsController` (class)
```
class ListProjectsController implements IListProjectsController
```
**Intent:** Implement the IListProjectsController interface to handle project listing requests.


### `constructor` (method)
```
constructor({ listProjectsUseCase }: { listProjectsUseCase: IListProjectsUseCase })
```
**Intent:** Initialize the ListProjectsController with a use case for listing projects.

**Inputs:**
- listProjectsUseCase: IListProjectsUseCase — the use case to list projects

### `execute` (method)
```
async execute(request: z.infer<typeof InputSchema>): Promise<z.infer<ReturnType<typeof PaginatedList<typeof Project>>>>
```
**Intent:** Validate the input request and execute the use case to list projects.

**Inputs:**
- request: z.infer<typeof InputSchema> — the input data for listing projects
**Outputs:**
- Promise<z.infer<ReturnType<typeof PaginatedList<typeof Project>>>> — a paginated list of projects
**Raises:**
- BadRequestError: when the request input is invalid

## Internal dependencies
- @/src/application/use-cases/projects/list-projects.use-case
- @/src/entities/errors/common
- @/src/entities/models/project
- @/src/entities/common/paginated-list

## External dependencies
- zod

## Flagged idioms
- TypeScript interface implementation: ListProjectsController implements IListProjectsController to ensure it adheres to the defined contract.

## Behavioral notes
- The execute method uses zod to validate the input schema before proceeding with the use case execution.
