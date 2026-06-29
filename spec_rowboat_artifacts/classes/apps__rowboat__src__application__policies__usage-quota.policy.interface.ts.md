# apps/rowboat/src/application/policies/usage-quota.policy.interface.ts

**File:** apps/rowboat/src/application/policies/usage-quota.policy.interface.ts  
**Language:** typescript

## Purpose
Defines an interface for enforcing and consuming usage quotas for project actions.

## Interfaces
### `IUsageQuotaPolicy` (class)
```
interface IUsageQuotaPolicy
```
**Intent:** Provides a contract for implementing usage quota checks and consumption for project actions.


### `assertAndConsumeProjectAction` (method)
```
assertAndConsumeProjectAction(projectId: string): Promise<void>
```
**Intent:** Ensures a project action does not exceed its usage quota and records the action.

**Inputs:**
- projectId: string - The ID of the project to assert and consume.
**Outputs:**
- Promise<void>
**Raises:**
- QuotaExceededError: if the quota is exceeded.

### `assertAndConsumeRunJobAction` (method)
```
assertAndConsumeRunJobAction(projectId: string): Promise<void>
```
**Intent:** Ensures a project job run does not exceed its usage quota and records the action.

**Inputs:**
- projectId: string - The ID of the project to assert and consume.
**Outputs:**
- Promise<void>
**Raises:**
- QuotaExceededError: if the quota is exceeded.

## External dependencies
- @/src/entities/errors/common
