# apps/rowboat/src/application/use-cases/projects/list-projects.use-case.ts

**File:** apps/rowboat/src/application/use-cases/projects/list-projects.use-case.ts  
**Language:** typescript

## Purpose
List projects for a user with optional pagination.

## Interfaces
### `ListProjectsUseCase` (class)
```
class ListProjectsUseCase
```
**Intent:** Encapsulates the use case for listing projects associated with a user.


### `IListProjectsUseCase` (class)
```
interface IListProjectsUseCase
```
**Intent:** Defines the contract for the ListProjectsUseCase, specifying the execute method.


### `constructor` (method)
```
constructor({ projectsRepository }: { projectsRepository: IProjectsRepository })
```
**Intent:** Initializes the ListProjectsUseCase with a projects repository.

**Inputs:**
- projectsRepository: IProjectsRepository — the repository to access project data

### `execute` (method)
```
async execute(request: z.infer<typeof InputSchema>): Promise<z.infer<ReturnType<typeof PaginatedList<typeof Project>>>>
```
**Intent:** Fetches a list of projects for a user, optionally paginated by cursor and limit.

**Inputs:**
- request: z.infer<typeof InputSchema> — the input schema containing userId, cursor, and limit
**Outputs:**
- Promise<z.infer<ReturnType<typeof PaginatedList<typeof Project>>>> — a paginated list of projects

## Internal dependencies
- ../../repositories/projects.repository.interface

## External dependencies
- zod
- @/src/entities/models/project
- @/src/entities/common/paginated-list

## Flagged idioms
- Use of zod for input validation ensures type-safe request handling.

## Behavioral notes
- The execute method relies on the projectsRepository to fetch data, indicating a dependency on external data sources.
