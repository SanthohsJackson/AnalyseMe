# apps/rowboat/src/application/use-cases/projects/list-composio-tools.use-case.ts

**File:** apps/rowboat/src/application/use-cases/projects/list-composio-tools.use-case.ts  
**Language:** typescript

## Purpose
Provide a use case for listing Composio tools with authorization and quota checks.

## Interfaces
### `IListComposioToolsUseCase` (class)
```
interface IListComposioToolsUseCase
```
**Intent:** Define the contract for executing the use case to list Composio tools.


### `ListComposioToolsUseCase` (class)
```
class ListComposioToolsUseCase implements IListComposioToolsUseCase
```
**Intent:** Implement the use case for listing Composio tools with necessary policies.

**Inputs:**
- projectActionAuthorizationPolicy: IProjectActionAuthorizationPolicy
- usageQuotaPolicy: IUsageQuotaPolicy

### `constructor` (method)
```
constructor({ projectActionAuthorizationPolicy, usageQuotaPolicy }: { projectActionAuthorizationPolicy: IProjectActionAuthorizationPolicy, usageQuotaPolicy: IUsageQuotaPolicy })
```
**Intent:** Initialize the use case with authorization and quota policies.

**Inputs:**
- projectActionAuthorizationPolicy: IProjectActionAuthorizationPolicy
- usageQuotaPolicy: IUsageQuotaPolicy

### `execute` (method)
```
execute(request: z.infer<typeof InputSchema>): Promise<z.infer<ReturnType<typeof ZListResponse<typeof ZTool>>>>
```
**Intent:** Execute the listing of Composio tools after performing authorization and quota checks.

**Inputs:**
- request: z.infer<typeof InputSchema>
**Outputs:**
- Promise<z.infer<ReturnType<typeof ZListResponse<typeof ZTool>>>>
**Side effects:**
- Authorization check and quota consumption

## Internal dependencies
- ../../policies/project-action-authorization.policy
- ../../policies/usage-quota.policy.interface
- @/src/application/lib/composio/composio
- ../../lib/composio/types

## External dependencies
- zod

## Flagged idioms
- Use of zod for schema validation: ensures input conforms to expected structure.

## Behavioral notes
- The execute method performs authorization and quota checks before listing tools.
