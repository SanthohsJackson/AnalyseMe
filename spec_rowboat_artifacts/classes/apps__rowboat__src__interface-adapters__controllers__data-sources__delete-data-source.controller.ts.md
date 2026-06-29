# apps/rowboat/src/interface-adapters/controllers/data-sources/delete-data-source.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/data-sources/delete-data-source.controller.ts  
**Language:** typescript

## Purpose
Handle the deletion of a data source by validating input and invoking the appropriate use case.

## Interfaces
### `IDeleteDataSourceController` (interface)
```
interface IDeleteDataSourceController
```
**Intent:** Define the contract for a controller that deletes a data source.


### `DeleteDataSourceController` (class)
```
class DeleteDataSourceController implements IDeleteDataSourceController
```
**Intent:** Implement the controller for deleting a data source, ensuring input validation and use case execution.


### `constructor` (method)
```
constructor({ deleteDataSourceUseCase }: { deleteDataSourceUseCase: IDeleteDataSourceUseCase })
```
**Intent:** Initialize the controller with the necessary use case for data source deletion.

**Inputs:**
- deleteDataSourceUseCase: IDeleteDataSourceUseCase — the use case to execute the deletion

### `execute` (method)
```
async execute(request: z.infer<typeof inputSchema>): Promise<void>
```
**Intent:** Validate the input request and execute the data source deletion use case.

**Inputs:**
- request: z.infer<typeof inputSchema> — the input data for deletion
**Outputs:**
- Promise<void> — resolves when the operation completes
**Raises:**
- BadRequestError: when the request validation fails

## Internal dependencies
- @/src/application/use-cases/data-sources/delete-data-source.use-case

## External dependencies
- zod
- @/src/entities/errors/common

## Flagged idioms
- Use of Zod for input validation ensures type-safe request handling.

## Behavioral notes
- The execute method throws a BadRequestError if input validation fails.
