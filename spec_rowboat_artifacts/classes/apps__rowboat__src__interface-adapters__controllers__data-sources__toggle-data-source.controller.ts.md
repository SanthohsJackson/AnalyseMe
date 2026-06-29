# apps/rowboat/src/interface-adapters/controllers/data-sources/toggle-data-source.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/data-sources/toggle-data-source.controller.ts  
**Language:** typescript

## Purpose
Toggle the active state of a data source based on a validated request.

## Interfaces
### `ToggleDataSourceController` (class)
```
class ToggleDataSourceController
```
**Intent:** Encapsulates the logic to toggle a data source's active state using a use case.


### `constructor` (method)
```
constructor({ toggleDataSourceUseCase }: { toggleDataSourceUseCase: IToggleDataSourceUseCase })
```
**Intent:** Initializes the controller with a specific use case for toggling data sources.

**Inputs:**
- toggleDataSourceUseCase: IToggleDataSourceUseCase — the use case to execute the toggle operation

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<z.infer<typeof DataSource>>
```
**Intent:** Validates the request and executes the toggle operation on the data source.

**Inputs:**
- request: z.infer<typeof inputSchema> — the request object containing toggle parameters
**Outputs:**
- Promise<z.infer<typeof DataSource>> — the toggled data source
**Raises:**
- BadRequestError: when the request validation fails

### `IToggleDataSourceController` (class)
```
interface IToggleDataSourceController
```
**Intent:** Defines the contract for a controller that can toggle a data source.


## Internal dependencies
- @/src/application/use-cases/data-sources/toggle-data-source.use-case
- @/src/entities/errors/common
- @/src/entities/models/data-source

## External dependencies
- zod

## Flagged idioms
- Use of Zod for schema validation: Ensures request data conforms to expected structure before processing.

## Behavioral notes
- The execute method uses safeParse to validate input, which provides detailed error information if validation fails.
