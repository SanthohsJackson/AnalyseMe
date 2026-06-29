# apps/cli/src/application/lib/exec-tool.ts

**File:** apps/cli/src/application/lib/exec-tool.ts  
**Language:** typescript

## Purpose
Execute tools based on their type, either 'mcp' or 'builtin'.

## Interfaces
### `execMcpTool` (function)
```
execMcpTool(agentTool: z.infer<typeof ToolAttachment> & { type: 'mcp' }, input: any) -> Promise<any>
```
**Intent:** Execute an MCP tool using the provided server name and tool name.

**Inputs:**
- agentTool: z.infer<typeof ToolAttachment> & { type: 'mcp' } — the tool to execute
- input: any — the input for the tool execution
**Outputs:**
- Promise<any> — the result of the tool execution

### `execTool` (function)
```
execTool(agentTool: z.infer<typeof ToolAttachment>, input: any) -> Promise<any>
```
**Intent:** Determine the type of tool and execute it accordingly, handling both 'mcp' and 'builtin' types.

**Inputs:**
- agentTool: z.infer<typeof ToolAttachment> — the tool to execute
- input: any — the input for the tool execution
**Outputs:**
- Promise<any> — the result of the tool execution
**Raises:**
- Error: when the builtin tool is unsupported or lacks an execute method

## Internal dependencies
- ../../mcp/mcp.js
- ./builtin-tools.js

## External dependencies
- zod

## Flagged idioms
- TypeScript type inference with zod: used to ensure the agentTool parameter conforms to expected types.

## Behavioral notes
- The function execTool throws an error if a builtin tool is unsupported or lacks an execute method.
