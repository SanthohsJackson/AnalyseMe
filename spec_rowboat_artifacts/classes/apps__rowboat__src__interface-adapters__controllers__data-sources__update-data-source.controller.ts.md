# apps/rowboat/src/interface-adapters/controllers/data-sources/update-data-source.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/data-sources/update-data-source.controller.ts  
**Language:** typescript

## Purpose
The UpdateDataSourceController class validates and processes requests to update data sources using a specified use case.

## Interfaces
### `IUpdateDataSourceController` (class)
```
interface IUpdateDataSourceController
```
**Intent:** Defines the contract for a controller that updates data sources.


### `UpdateDataSourceController` (class)
```
class UpdateDataSourceController implements IUpdateDataSourceController
```
**Intent:** Implements the IUpdateDataSourceController interface to handle data source update requests.

**Inputs:**
- updateDataSourceUseCase: IUpdateDataSourceUseCase

### `constructor` (method)
```
constructor({ updateDataSourceUseCase }: { updateDataSourceUseCase: IUpdateDataSourceUseCase })
```
**Intent:** Initializes the UpdateDataSourceController with a use case for updating data sources.

**Inputs:**
- updateDataSourceUseCase: IUpdateDataSourceUseCase

### `execute` (method)
```
async execute(request: z.infer<typeof inputSchema>): Promise<z.infer<typeof DataSource>>
```
**Intent:** Validates the request and executes the update data source use case.

**Inputs:**
- request: z.infer<typeof inputSchema> — the request object containing update details
**Outputs:**
- Promise<z.infer<typeof DataSource>> — the updated data source
**Raises:**
- BadRequestError: when the request validation fails

## Internal dependencies
- @/src/application/use-cases/data-sources/update-data-source.use-case

## External dependencies
- zod

## Flagged idioms
- Use of zod for schema validation ensures type-safe request validation.

## Behavioral notes
- The execute method uses safeParse to validate the request, which provides detailed error information if validation fails.
