# apps/rowboat/src/interface-adapters/controllers/data-sources/create-data-source.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/data-sources/create-data-source.controller.ts  
**Language:** typescript

## Purpose
Handle the creation of a data source by validating input and invoking a use case.

## Interfaces
### `ICreateDataSourceController` (class)
```
interface ICreateDataSourceController
```
**Intent:** Define the contract for a controller that creates data sources.


### `CreateDataSourceController` (class)
```
class CreateDataSourceController implements ICreateDataSourceController
```
**Intent:** Implement the controller interface to manage data source creation.

**Inputs:**
- createDataSourceUseCase: ICreateDataSourceUseCase

### `constructor` (method)
```
constructor({ createDataSourceUseCase }: { createDataSourceUseCase: ICreateDataSourceUseCase })
```
**Intent:** Initialize the controller with a use case for creating data sources.

**Inputs:**
- createDataSourceUseCase: ICreateDataSourceUseCase

### `execute` (method)
```
async execute(request: z.infer<typeof inputSchema>): Promise<z.infer<typeof DataSource>>
```
**Intent:** Validate the input request and execute the use case to create a data source.

**Inputs:**
- request: z.infer<typeof inputSchema>
**Outputs:**
- Promise<z.infer<typeof DataSource>>
**Raises:**
- BadRequestError: when the request is invalid

## Internal dependencies
- @/src/application/use-cases/data-sources/create-data-source.use-case
- @/src/entities/errors/common
- @/src/entities/models/data-source
- @/src/application/repositories/data-sources.repository.interface

## External dependencies
- zod

## Flagged idioms
- Use of Zod for input validation: ensures request data conforms to expected schema before processing.

## Behavioral notes
- The execute method uses safeParse to validate input, which provides detailed error information if validation fails.
