# apps/x/packages/core/src/agent-schedule/repo.ts

**File:** apps/x/packages/core/src/agent-schedule/repo.ts  
**Language:** typescript

## Purpose
Manage agent schedule configurations stored in a file system.

## Interfaces
### `ensureConfig` (method)
```
ensureConfig(): Promise<void>
```
**Intent:** Ensure that the agent schedule configuration file exists, creating it with default values if necessary.

**Outputs:**
- Promise<void>
**Side effects:**
- Creates a default agent schedule configuration file if it does not exist.

### `getConfig` (method)
```
getConfig(): Promise<z.infer<typeof AgentScheduleConfig>>
```
**Intent:** Retrieve and parse the current agent schedule configuration from the file system.

**Outputs:**
- Promise<z.infer<typeof AgentScheduleConfig>>

### `upsert` (method)
```
upsert(agentName: string, entry: z.infer<typeof AgentScheduleEntry>): Promise<void>
```
**Intent:** Add or update an agent's schedule entry in the configuration file.

**Inputs:**
- agentName: string
- entry: z.infer<typeof AgentScheduleEntry>
**Outputs:**
- Promise<void>
**Side effects:**
- Updates or adds an agent schedule entry in the configuration file.

### `delete` (method)
```
delete(agentName: string): Promise<void>
```
**Intent:** Delete an agent's schedule entry from the configuration file.

**Inputs:**
- agentName: string
**Outputs:**
- Promise<void>
**Side effects:**
- Removes an agent schedule entry from the configuration file.

### `FSAgentScheduleRepo` (class)
```
class FSAgentScheduleRepo implements IAgentScheduleRepo
```
**Intent:** Provide a file system-based implementation of the IAgentScheduleRepo interface.


### `IAgentScheduleRepo` (class)
```
interface IAgentScheduleRepo
```
**Intent:** Define the contract for agent schedule repository operations.


## Internal dependencies
- ../config/config.js

## External dependencies
- @x/shared/dist/agent-schedule.js
- fs/promises
- path
- zod

## Flagged idioms
- Use of async/await for handling asynchronous file operations.

## Behavioral notes
- The configuration file is assumed to be JSON formatted and is parsed/serialized accordingly.
