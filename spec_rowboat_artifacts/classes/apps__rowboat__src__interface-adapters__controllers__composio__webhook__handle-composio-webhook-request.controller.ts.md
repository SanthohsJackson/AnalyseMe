# apps/rowboat/src/interface-adapters/controllers/composio/webhook/handle-composio-webhook-request.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/composio/webhook/handle-composio-webhook-request.controller.ts  
**Language:** typescript

## Purpose
Handle and validate incoming webhook requests for the Composio service.

## Interfaces
### `IHandleComposioWebhookRequestController` (class)
```
interface IHandleComposioWebhookRequestController
```
**Intent:** Define the contract for handling Composio webhook requests.


### `HandleComposioWebhookRequestController` (class)
```
class HandleComposioWebhookRequestController implements IHandleComposioWebhookRequestController
```
**Intent:** Implement the logic to handle Composio webhook requests using a specified use case.

**Inputs:**
- handleCompsioWebhookRequestUseCase: IHandleCompsioWebhookRequestUseCase

### `constructor` (method)
```
constructor({ handleCompsioWebhookRequestUseCase }: { handleCompsioWebhookRequestUseCase: IHandleCompsioWebhookRequestUseCase })
```
**Intent:** Initialize the controller with a use case for handling webhook requests.

**Inputs:**
- handleCompsioWebhookRequestUseCase: IHandleCompsioWebhookRequestUseCase

### `execute` (method)
```
execute(request: z.infer<typeof inputSchema>): Promise<void>
```
**Intent:** Validate the incoming request and execute the associated use case if valid.

**Inputs:**
- request: z.infer<typeof inputSchema> — the incoming webhook request
**Outputs:**
- Promise<void>
**Raises:**
- BadRequestError: when the request is invalid

## Internal dependencies
- @/src/application/use-cases/composio/webhook/handle-composio-webhook-request.use-case

## External dependencies
- zod
- @/src/entities/errors/common

## Flagged idioms
- Use of Zod for schema validation: ensures request data conforms to expected structure before processing.

## Behavioral notes
- The execute method throws a BadRequestError if the request validation fails.
