# apps/rowboat/app/lib/mcp.ts

**File:** apps/rowboat/app/lib/mcp.ts  
**Language:** typescript

## Purpose
Provide a helper function to establish a connection to an MCP server using different transport protocols.

## Interfaces
### `getMcpClient` (function)
```
getMcpClient(serverUrl: string, serverName: string) -> Promise<Client>
```
**Intent:** Attempt to connect to an MCP server using Streamable HTTP transport first, and fall back to SSE transport if the first attempt fails.

**Inputs:**
- serverUrl: string — the URL of the MCP server
- serverName: string — the name of the MCP server
**Outputs:**
- Promise<Client> — a promise that resolves to a connected Client instance
**Side effects:**
- Logs connection attempts and successes to the console

## External dependencies
- @modelcontextprotocol/sdk/client/index.js
- @modelcontextprotocol/sdk/client/sse.js
- @modelcontextprotocol/sdk/client/streamableHttp.js

## Flagged idioms
- Try-catch block used to handle connection attempts and fallbacks between different transport protocols.

## Behavioral notes
- The function logs messages to the console indicating the success or failure of connection attempts.
