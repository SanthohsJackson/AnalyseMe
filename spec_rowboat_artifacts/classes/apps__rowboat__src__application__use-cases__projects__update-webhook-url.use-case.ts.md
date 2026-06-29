# apps/rowboat/src/application/use-cases/projects/update-webhook-url.use-case.ts

**File:** apps/rowboat/src/application/use-cases/projects/update-webhook-url.use-case.ts  
**Language:** typescript

## Purpose
Update the webhook URL for a project after authorizing the action and checking usage quotas.

## Interfaces
### `UpdateWebhookUrlUseCase` (class)
```
class UpdateWebhookUrlUseCase
```
**Intent:** Encapsulates the logic for updating a project's webhook URL, including authorization and quota checks.


### `constructor` (method)
```
constructor({ projectsRepository, projectActionAuthorizationPolicy, usageQuotaPolicy }: { projectsRepository: IProjectsRepository, projectActionAuthorizationPolicy: IProjectActionAuthorizationPolicy, usageQuotaPolicy: IUsageQuotaPolicy })
```
**Intent:** Initializes the use case with necessary dependencies for repository access, authorization, and quota management.

**Inputs:**
- projectsRepository: IProjectsRepository — repository for project data
- projectActionAuthorizationPolicy: IProjectActionAuthorizationPolicy — policy for authorizing project actions
- usageQuotaPolicy: IUsageQuotaPolicy — policy for managing usage quotas

### `execute` (method)
```
execute(request: z.infer<typeof InputSchema>): Promise<void>
```
**Intent:** Executes the process of updating a project's webhook URL, ensuring the action is authorized and within usage limits.

**Inputs:**
- request: z.infer<typeof InputSchema> — validated input containing projectId, userId, caller, apiKey, and url
**Outputs:**
- Promise<void> — resolves when the webhook URL update is complete
**Side effects:**
- Authorizes the action using projectActionAuthorizationPolicy
- Consumes quota using usageQuotaPolicy
- Updates the webhook URL in projectsRepository

### `IUpdateWebhookUrlUseCase` (class)
```
interface IUpdateWebhookUrlUseCase
```
**Intent:** Defines the contract for the UpdateWebhookUrlUseCase, specifying the execute method.


## Internal dependencies
- ../../repositories/projects.repository.interface
- ../../policies/project-action-authorization.policy
- ../../policies/usage-quota.policy.interface

## External dependencies
- zod

## Flagged idioms
- Dependency Injection: Constructor injection is used to provide dependencies, allowing for easier testing and flexibility.

## Behavioral notes
- The execute method performs multiple asynchronous operations in sequence: authorization, quota consumption, and repository update.
