# apps/rowboat/src/interface-adapters/controllers/data-sources/recrawl-web-data-source.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/data-sources/recrawl-web-data-source.controller.ts  
**Language:** typescript

## Purpose
Handle the recrawling of web data sources by validating input and invoking a use case.

## Interfaces
### `RecrawlWebDataSourceController` (class)
```
class RecrawlWebDataSourceController
```
**Intent:** Encapsulate the logic for controlling the recrawl of web data sources.


### `IRecrawlWebDataSourceController` (class)
```
interface IRecrawlWebDataSourceController
```
**Intent:** Define the contract for a controller that handles recrawling of web data sources.


### `constructor` (method)
```
constructor({ recrawlWebDataSourceUseCase }: { recrawlWebDataSourceUseCase: IRecrawlWebDataSourceUseCase })
```
**Intent:** Initialize the controller with a specific use case for recrawling web data sources.

**Inputs:**
- recrawlWebDataSourceUseCase: IRecrawlWebDataSourceUseCase — the use case to execute recrawling

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<void>
```
**Intent:** Validate the input request and execute the recrawl operation using the provided use case.

**Inputs:**
- request: z.infer<typeof inputSchema> — the input data for the recrawl operation
**Outputs:**
- Promise<void> — resolves when the operation completes
**Raises:**
- BadRequestError: when the request validation fails
**Side effects:**
- Invokes the recrawlWebDataSourceUseCase with validated input

## Internal dependencies
- @/src/application/use-cases/data-sources/recrawl-web-data-source.use-case

## External dependencies
- zod
- @/src/entities/errors/common

## Flagged idioms
- Use of zod for input validation ensures type-safe request handling.

## Behavioral notes
- The execute method throws a BadRequestError if input validation fails.
