# MCP transports — local stdio vs remote HTTP

Your labs [**PROJECT_1**](./PROJECT_1/registry_demo.md) and [**PROJECT_2**](./PROJECT_2/project_2.md) use **stdio**: the client **starts** `server.py` as a child process and talks over stdin/stdout.

**Remote / HTTP** means the MCP server is already **running somewhere else** (another machine, container, or long-lived local process) and the client connects over **the network**.

---

## Why transports matter

| Layer | What it is |
|-------|------------|
| **MCP protocol** | Messages like `tools/list`, `tools/call` (JSON-RPC style) |
| **Transport** | **How** those messages move: pipes (stdio) or HTTP/SSE |

Same tools and same `@mcp.tool()` code on the server — different **wiring** on the client.

---

## stdio (what you use now)

```text
registry_demo / runner
    → Client("time-mcp-server/server.py")
    → OS spawns: python time-mcp-server/server.py
    → Parent writes/reads JSON on child's stdin/stdout
```

| Pros | Cons |
|------|------|
| Simple for learning; no ports/firewall | Server only lives while client holds the process |
| No HTTP server to configure | Hard to share one server across many apps |
| Works offline on one laptop | Not how most **hosted** MCP services expose tools |

FastMCP default: `mcp.run()` → **stdio** when you run the file directly.

---

## Remote MCP (concept)

```text
                    ┌─────────────────────┐
  Your agent/IDE    │  MCP Server         │
  (client)  ───────►│  (always on)        │
   HTTP/SSE         │  @mcp.tool() ...    │
                    └─────────────────────┘
                         another host
                         or :8000 on localhost
```

The client does **not** spawn `server.py`. It connects to a **URL** (and often sends auth headers).

---

## HTTP-family transports (names you will see)

FastMCP (and MCP SDK) distinguish several modes; names vary by version:

| Transport | Idea | Typical use |
|-----------|------|-------------|
| **`stdio`** | Local child process pipes | Cursor/CLI learning labs, IDE spawns server |
| **`streamable-http`** (often default HTTP today) | MCP over HTTP with streaming body | New deployments, “MCP URL” in configs |
| **`sse`** | Server-Sent Events over HTTP (older pattern) | Legacy servers; still in docs and proxies |
| **`http`** | Generic HTTP label in configs | Check FastMCP version — may map to streamable HTTP |

**Remote** in practice = client configured with something like:

```text
https://api.example.com/mcp
http://127.0.0.1:8000/mcp
```

not a path to `server.py`.

---

## Server side (FastMCP — concept)

Local lab:

```python
if __name__ == "__main__":
    mcp.run()  # stdio
```

Expose over the network (concept — flags depend on FastMCP version):

```bash
# Examples from docs / CLI patterns (verify with: fastmcp --help)
fastmcp run time-mcp-server/server.py --transport http --host 0.0.0.0 --port 8000
```

Or in code: `run_http_async()`, `http_app()` — serves MCP on a **path** (often `/mcp`).

The **same** `@mcp.tool()` functions run; only the listener changes from pipes to HTTP.

---

## Client side (FastMCP — concept)

Lab (stdio):

```python
from fastmcp import Client
client = Client("time-mcp-server/server.py")
```

Remote (URL transport — illustrative):

```python
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

client = Client(StreamableHttpTransport("http://127.0.0.1:8000/mcp"))
```

Legacy SSE-style URL might use `SSETransport("http://127.0.0.1:8000/sse")`.

Your **PROJECT_1** `connect()` / `discover_tools()` / `call_tool()` stay the same **after** the client is connected — only how `Client(...)` is constructed changes.

---

## Comparison table

| | stdio (PROJECT_1/2) | Remote HTTP |
|---|----------------------|-------------|
| **Client connects with** | Path to `server.py` | Base URL + transport |
| **Who starts the server?** | Client (spawn) | You / ops / platform |
| **Network** | No | Yes |
| **Multiple clients** | One process per client typically | One server, many clients |
| **Cursor / cloud agents** | Common for dev | Common for **shared** tools (APIs, DB, SaaS) |
| **Auth** | OS user / file access | API keys, OAuth, mTLS on HTTP |

---

## JSON-RPC flow (same on every transport)

Whether stdio or HTTP, the logical flow is unchanged:

```text
tools/list   →  [ Tool(name, description, input_schema, ...), ... ]
tools/call   →  { name, arguments }  →  CallToolResult
```

See [**PROJECT_1 clarifications**](./PROJECT_1/registry_demo.md#clarifications-study-qa) for `list_tools` / `call_tool` mapping.

---

## When to choose what

| Situation | Prefer |
|-----------|--------|
| Learning, unit-style demos, no open ports | **stdio** |
| Same tool server for IDE + agent + CI | **HTTP** remote |
| Tool runs in K8s / VPC | **HTTP** + auth, not stdio from random laptops |
| Cursor config `command` + `args` | Usually **stdio** spawn |
| Cursor / host gives **URL** only | **HTTP** (streamable HTTP or SSE) |

---

## Security notes (remote)

| Topic | Why it matters |
|-------|----------------|
| **TLS** (`https://`) | Protect tokens and tool args on the wire |
| **Auth headers** | Remote servers must not be open MCP on the public internet |
| **Tool power** | `tools/call` can run real side effects — treat URL like an API endpoint |

---

## Mental model — one sentence

**stdio** = MCP as a **subprocess pipe**; **remote HTTP** = MCP as a **web service** — same tool list and tool calls, different connection string.

---

## Interview one-liner

**MCP transport** carries `tools/list` and `tools/call`; **stdio** spawns a local server script; **remote HTTP/SSE** connects to a URL so one shared MCP server can serve multiple clients across the network.