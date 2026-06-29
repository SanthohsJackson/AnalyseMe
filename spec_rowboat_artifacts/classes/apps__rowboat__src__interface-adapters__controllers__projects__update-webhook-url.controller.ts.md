# apps/rowboat/src/interface-adapters/controllers/projects/update-webhook-url.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/projects/update-webhook-url.controller.ts  
**Language:** typescript

## Purpose
Handle the updating of a webhook URL by validating input and executing the corresponding use case.

## Interfaces
### `IUpdateWebhookUrlController` (class)
```
interface IUpdateWebhookUrlController
```
**Intent:** Define the contract for a controller that updates a webhook URL.


### `UpdateWebhookUrlController` (class)
```
class UpdateWebhookUrlController implements IUpdateWebhookUrlController
```
**Intent:** Implement the controller for updating a webhook URL using a provided use case.

**Inputs:**
- updateWebhookUrlUseCase: IUpdateWebhookUrlUseCase

### `constructor` (method)
```
constructor({ updateWebhookUrlUseCase }: { updateWebhookUrlUseCase: IUpdateWebhookUrlUseCase })
```
**Intent:** Initialize the controller with a specific use case for updating webhook URLs.

**Inputs:**
- updateWebhookUrlUseCase: IUpdateWebhookUrlUseCase

### `execute` (method)
```
execute(request: z.infer<typeof InputSchema>): Promise<void>
```
**Intent:** Validate the input request and execute the update webhook URL use case if valid.

**Inputs:**
- request: z.infer<typeof InputSchema> — the input data to validate and process
**Outputs:**
- Promise<void> — resolves when the operation completes
**Raises:**
- BadRequestError: when the input validation fails

## Internal dependencies
- @/src/application/use-cases/projects/update-webhook-url.use-case
- @/src/entities/errors/common

## External dependencies
- zod

## Flagged idioms
- Use of Zod for input validation: ensures that the input data conforms to a predefined schema before processing.

## Behavioral notes
- The execute method uses Zod's safeParse to validate input, which provides a structured error object if validation fails.
