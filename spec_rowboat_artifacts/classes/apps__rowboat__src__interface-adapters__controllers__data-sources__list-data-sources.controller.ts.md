# apps/rowboat/src/interface-adapters/controllers/data-sources/list-data-sources.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/data-sources/list-data-sources.controller.ts  
**Language:** typescript

## Purpose
Handle requests to list data sources by validating input and invoking a use case.

## Interfaces
### `ListDataSourcesController` (class)
```
class ListDataSourcesController
```
**Intent:** Encapsulate the logic for listing data sources, including input validation and use case execution.


### `IListDataSourcesController` (class)
```
interface IListDataSourcesController
```
**Intent:** Define the contract for a controller that lists data sources.


### `constructor` (method)
```
constructor({ listDataSourcesUseCase }: { listDataSourcesUseCase: IListDataSourcesUseCase })
```
**Intent:** Initialize the ListDataSourcesController with a specific use case.

**Inputs:**
- listDataSourcesUseCase: IListDataSourcesUseCase — the use case to execute for listing data sources

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<z.infer<typeof DataSource>[]>
```
**Intent:** Validate the input request and execute the use case to list data sources.

**Inputs:**
- request: z.infer<typeof inputSchema> — the input data for listing data sources
**Outputs:**
- Promise<z.infer<typeof DataSource>[]> — a promise resolving to an array of data sources
**Raises:**
- BadRequestError: when the request input is invalid

## Internal dependencies
- @/src/application/use-cases/data-sources/list-data-sources.use-case

## External dependencies
- zod

## Flagged idioms
- Use of zod for input validation ensures type-safe request handling.

## Behavioral notes
- The execute method throws a BadRequestError if input validation fails.
