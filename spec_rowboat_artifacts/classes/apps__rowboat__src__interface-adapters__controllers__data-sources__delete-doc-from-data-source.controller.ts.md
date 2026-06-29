# apps/rowboat/src/interface-adapters/controllers/data-sources/delete-doc-from-data-source.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/data-sources/delete-doc-from-data-source.controller.ts  
**Language:** typescript

## Purpose
Controller for deleting a document from a data source, validating input and invoking the use case.

## Interfaces
### `IDeleteDocFromDataSourceController` (interface)
```
interface IDeleteDocFromDataSourceController
```
**Intent:** Defines the contract for a controller that deletes a document from a data source.


### `DeleteDocFromDataSourceController` (class)
```
class DeleteDocFromDataSourceController implements IDeleteDocFromDataSourceController
```
**Intent:** Implements the controller interface to handle the deletion of a document from a data source.

**Inputs:**
- deleteDocFromDataSourceUseCase: IDeleteDocFromDataSourceUseCase

### `constructor` (method)
```
constructor({ deleteDocFromDataSourceUseCase }: { deleteDocFromDataSourceUseCase: IDeleteDocFromDataSourceUseCase })
```
**Intent:** Initializes the controller with the use case for deleting a document.

**Inputs:**
- deleteDocFromDataSourceUseCase: IDeleteDocFromDataSourceUseCase

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<void>
```
**Intent:** Validates the input request and executes the use case to delete a document.

**Inputs:**
- request: z.infer<typeof inputSchema> — the input data for the operation
**Outputs:**
- Promise<void> — resolves when the operation completes
**Raises:**
- BadRequestError: when the request validation fails

## Internal dependencies
- @/src/application/use-cases/data-sources/delete-doc-from-data-source.use-case

## External dependencies
- zod
- @/src/entities/errors/common

## Flagged idioms
- Use of Zod for input validation ensures type-safe request handling.

## Behavioral notes
- The execute method throws a BadRequestError if input validation fails.
