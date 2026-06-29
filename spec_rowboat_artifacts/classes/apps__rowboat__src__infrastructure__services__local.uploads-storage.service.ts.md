# apps/rowboat/src/infrastructure/services/local.uploads-storage.service.ts

**File:** apps/rowboat/src/infrastructure/services/local.uploads-storage.service.ts  
**Language:** typescript

## Purpose
Provide local storage service for uploading and downloading files.

## Interfaces
### `LocalUploadsStorageService` (class)
```
class LocalUploadsStorageService implements IUploadsStorageService
```
**Intent:** Defines a service for handling file uploads and downloads using local storage.


### `constructor` (method)
```
constructor({ dataSourceDocsRepository }: { dataSourceDocsRepository: IDataSourceDocsRepository })
```
**Intent:** Initializes the service with a data source documents repository.

**Inputs:**
- dataSourceDocsRepository: IDataSourceDocsRepository — repository for accessing data source documents

### `getUploadUrl` (method)
```
async getUploadUrl(key: string, contentType: string) -> Promise<string>
```
**Intent:** Generates a URL for uploading a file.

**Inputs:**
- key: string — the key for the file
- contentType: string — the MIME type of the file
**Outputs:**
- Promise<string> — URL for uploading the file

### `getDownloadUrl` (method)
```
async getDownloadUrl(fileId: string) -> Promise<string>
```
**Intent:** Generates a URL for downloading a file.

**Inputs:**
- fileId: string — the identifier of the file
**Outputs:**
- Promise<string> — URL for downloading the file

### `getFileContents` (method)
```
async getFileContents(fileId: string) -> Promise<Buffer>
```
**Intent:** Retrieves the contents of a file from local storage.

**Inputs:**
- fileId: string — the identifier of the file
**Outputs:**
- Promise<Buffer> — contents of the file as a buffer
**Raises:**
- NotFoundError: when the file is not found or is not a local file
**Side effects:**
- Reads file contents from the local filesystem

## External dependencies
- fs
- path

## Flagged idioms
- Use of environment variable for configuration: allows dynamic configuration of the uploads directory.

## Behavioral notes
- The service assumes files are stored locally and uses synchronous file reading.
