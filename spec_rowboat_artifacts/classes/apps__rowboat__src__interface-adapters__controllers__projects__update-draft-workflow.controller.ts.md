# apps/rowboat/src/interface-adapters/controllers/projects/update-draft-workflow.controller.ts

**File:** apps/rowboat/src/interface-adapters/controllers/projects/update-draft-workflow.controller.ts  
**Language:** typescript

## Purpose
Handle the update of a draft workflow by validating input and invoking the use case.

## Interfaces
### `IUpdateDraftWorkflowController` (class)
```
interface IUpdateDraftWorkflowController
```
**Intent:** Define the contract for controllers that handle updating draft workflows.


### `UpdateDraftWorkflowController` (class)
```
class UpdateDraftWorkflowController implements IUpdateDraftWorkflowController
```
**Intent:** Implement the controller logic for updating draft workflows using a provided use case.

**Inputs:**
- updateDraftWorkflowUseCase: IUpdateDraftWorkflowUseCase

### `constructor` (method)
```
constructor({ updateDraftWorkflowUseCase }: { updateDraftWorkflowUseCase: IUpdateDraftWorkflowUseCase })
```
**Intent:** Initialize the controller with a specific use case for updating draft workflows.

**Inputs:**
- updateDraftWorkflowUseCase: IUpdateDraftWorkflowUseCase

### `execute` (method)
```
execute(request: z.infer<typeof InputSchema>): Promise<void>
```
**Intent:** Validate the input request and execute the update draft workflow use case if valid.

**Inputs:**
- request: z.infer<typeof InputSchema>
**Outputs:**
- Promise<void>
**Raises:**
- BadRequestError: when the request is invalid

## Internal dependencies
- @/src/application/use-cases/projects/update-draft-workflow.use-case

## External dependencies
- zod
- @/src/entities/errors/common

## Flagged idioms
- Use of Zod for input validation: ensures request data conforms to expected schema before processing.

## Behavioral notes
- Throws a BadRequestError with a detailed message if input validation fails.
