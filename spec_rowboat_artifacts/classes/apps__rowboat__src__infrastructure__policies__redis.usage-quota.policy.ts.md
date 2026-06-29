# apps/rowboat/src/infrastructure/policies/redis.usage-quota.policy.ts

**File:** apps/rowboat/src/infrastructure/policies/redis.usage-quota.policy.ts  
**Language:** typescript

## Purpose
Enforce and track usage quotas for projects using Redis as a backend.

## Interfaces
### `RedisUsageQuotaPolicy` (class)
```
class RedisUsageQuotaPolicy implements IUsageQuotaPolicy
```
**Intent:** Defines a policy for managing usage quotas using Redis.


### `assertAndConsumeProjectAction` (method)
```
async assertAndConsumeProjectAction(projectId: string) -> Promise<void>
```
**Intent:** Check and enforce the per-minute query quota for a project.

**Inputs:**
- projectId: string — the identifier for the project
**Outputs:**
- Promise<void> — resolves when the action is processed
**Raises:**
- QuotaExceededError: when the project exceeds its query quota per minute
**Side effects:**
- Increments a Redis key and sets its expiration

### `assertAndConsumeRunJobAction` (method)
```
async assertAndConsumeRunJobAction(projectId: string) -> Promise<void>
```
**Intent:** Check and enforce the per-hour job quota for a project.

**Inputs:**
- projectId: string — the identifier for the project
**Outputs:**
- Promise<void> — resolves when the action is processed
**Raises:**
- QuotaExceededError: when the project exceeds its job quota per hour
**Side effects:**
- Increments a Redis key and sets its expiration

## Internal dependencies
- @/src/application/policies/usage-quota.policy.interface
- @/app/lib/redis
- @/src/entities/errors/common
- @/src/application/lib/utils/time-to-next-minute

## Flagged idioms
- Use of environment variables to configure quotas, allowing dynamic configuration without code changes.

## Behavioral notes
- If the environment variables for quotas are not set, the quotas default to zero, effectively disabling the quota checks.
