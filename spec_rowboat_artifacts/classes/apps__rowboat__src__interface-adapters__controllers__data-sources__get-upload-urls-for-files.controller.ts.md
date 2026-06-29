# apps/rowboat/src/interface-adapters/controllers/data-sources/get-upload-urls-for-files.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/data-sources/get-upload-urls-for-files.controller.ts  
**Language:** typescript

## Purpose
Provide upload URLs for files based on a validated request.

## Interfaces
### `IGetUploadUrlsForFilesController` (class)
```
interface IGetUploadUrlsForFilesController
```
**Intent:** Define the contract for a controller that provides upload URLs for files.


### `GetUploadUrlsForFilesController` (class)
```
class GetUploadUrlsForFilesController implements IGetUploadUrlsForFilesController
```
**Intent:** Implement the controller to handle requests for file upload URLs.

**Inputs:**
- getUploadUrlsForFilesUseCase: IGetUploadUrlsForFilesUseCase

### `constructor` (method)
```
constructor({ getUploadUrlsForFilesUseCase }: { getUploadUrlsForFilesUseCase: IGetUploadUrlsForFilesUseCase })
```
**Intent:** Initialize the controller with a use case for getting upload URLs.

**Inputs:**
- getUploadUrlsForFilesUseCase: IGetUploadUrlsForFilesUseCase

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<{ fileId: string, uploadUrl: string, path: string }[]>
```
**Intent:** Validate the request and delegate to the use case to get upload URLs for the files.

**Inputs:**
- request: z.infer<typeof inputSchema> — the request object containing file details
**Outputs:**
- Promise<{ fileId: string, uploadUrl: string, path: string }[]> — a promise resolving to an array of file upload details
**Raises:**
- BadRequestError: when the request validation fails

## Internal dependencies
- @/src/application/use-cases/data-sources/get-upload-urls-for-files.use-case

## External dependencies
- zod
- @/src/entities/errors/common

## Flagged idioms
- Use of Zod for schema validation: ensures request data conforms to expected structure before processing.

## Behavioral notes
- The execute method throws a BadRequestError if the request does not pass validation.
