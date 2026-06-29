# apps/rowboat/src/application/use-cases/projects/list-composio-toolkits.use-case.ts

**File:** apps/rowboat/src/application/use-cases/projects/list-composio-toolkits.use-case.ts  
**Language:** typescript

## Purpose
List Composio toolkits for a given project, ensuring authorization and quota compliance.

## Interfaces
### `IListComposioToolkitsUseCase` (class)
```
interface IListComposioToolkitsUseCase
```
**Intent:** Define the contract for listing Composio toolkits with necessary authorization and quota checks.


### `ListComposioToolkitsUseCase` (class)
```
class ListComposioToolkitsUseCase implements IListComposioToolkitsUseCase
```
**Intent:** Implement the use case for listing Composio toolkits, ensuring authorization and quota policies are enforced.

**Inputs:**
- projectActionAuthorizationPolicy: IProjectActionAuthorizationPolicy
- usageQuotaPolicy: IUsageQuotaPolicy

### `constructor` (method)
```
constructor({ projectActionAuthorizationPolicy, usageQuotaPolicy }: { projectActionAuthorizationPolicy: IProjectActionAuthorizationPolicy, usageQuotaPolicy: IUsageQuotaPolicy })
```
**Intent:** Initialize the use case with the necessary authorization and quota policies.

**Inputs:**
- projectActionAuthorizationPolicy: IProjectActionAuthorizationPolicy
- usageQuotaPolicy: IUsageQuotaPolicy

### `execute` (method)
```
execute(request: z.infer<typeof InputSchema>): Promise<z.infer<ReturnType<typeof ZListResponse<typeof ZToolkit>>>>
```
**Intent:** Execute the listing of Composio toolkits after ensuring the request is authorized and within quota limits.

**Inputs:**
- request: z.infer<typeof InputSchema>
**Outputs:**
- Promise<z.infer<ReturnType<typeof ZListResponse<typeof ZToolkit>>>>
**Side effects:**
- Authorization check via projectActionAuthorizationPolicy
- Quota consumption via usageQuotaPolicy

## Internal dependencies
- ../../policies/project-action-authorization.policy
- ../../policies/usage-quota.policy.interface
- @/src/application/lib/composio/composio
- ../../lib/composio/types

## External dependencies
- zod

## Flagged idioms
- Use of zod for schema validation: ensures input conforms to expected structure before processing.

## Behavioral notes
- The execute method performs authorization and quota checks before listing toolkits, ensuring compliance with policies.
