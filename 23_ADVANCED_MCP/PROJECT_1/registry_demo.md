# Multi-server MCP registry lab

Folder **`PROJECT_1`** — connect **two** FastMCP servers, merge their tools into **one registry**, call a tool by name.

**stdio vs remote HTTP:** [`../mcp_remote_http_transport.md`](../mcp_remote_http_transport.md)

| File | Role |
|------|------|
| [`registry_demo.py`](./registry_demo.py) | **Run this** — build registry, list tools, demo `get_weather` |
| [`mcp_client.py`](./mcp_client.py) | Low-level: connect, list tools, call tool |
| [`mcp_manager.py`](./mcp_manager.py) | Registry: many servers → one `tool_name` map |
| [`time-mcp-server/server.py`](./time-mcp-server/server.py) | MCP server (time, dice, password) |
| [`weather-mcp-server/server.py`](./weather-mcp-server/server.py) | MCP server (`get_weather`) |

**LLM:** this lab has **no** OpenAI/Ollama code — only MCP wiring. For an agent loop with **OpenAI** + one server, see [`../../20_MCP_AGENT_LOOP/PROJECT_2/2_mcp_task_agent_loop.md`](../../20_MCP_AGENT_LOOP/PROJECT_2/2_mcp_task_agent_loop.md).

---

## Why it is needed (utility)

| Idea | Plain meaning |
|------|----------------|
| **More than one MCP server** | Prod agents often attach to calendar, weather, internal APIs — not a single `server.py`. |
| **Tool registry** | Caller uses `run_tool(registry, "get_weather", {...})` without remembering which server owns the tool. |
| **Client vs manager** | `mcp_client` = one connection; `mcp_manager` = fan-out + merge. |
| **Before LLM** | Proves stdio MCP works **offline** (no `OPENAI_API_KEY`) before you let a model pick tools. |

---

## What it does (one sentence)

Start two MCP child processes, **discover** all `@mcp.tool()` names, store them in a dict, **call** one tool, then **disconnect**.

---

## Flow (diagram)

```text
registry_demo.main()
    → create_tool_registry([time server, weather server])
        → connect (stdio) × 2
        → list_tools on each client
        → tool_registry[name] = { client, tool metadata }

    → run_tool(registry, "get_weather", {"city": "Delhi"})
        → lookup client for get_weather
        → call_tool(...)

    → close_servers(clients)
```

---

## Tools exposed

| Server file | Tool names |
|-------------|------------|
| `time-mcp-server/server.py` | `current_time`, `roll_dice`, `generate_password` |
| `weather-mcp-server/server.py` | `get_weather(city: str)` |

**Name collision:** if two servers register the same `tool.name`, the **later** server in the list overwrites the earlier entry in `tool_registry`.

---

## How to run

```bash
pip install fastmcp
```

From folder **`PROJECT_1`** (paths are relative to cwd):

```bash
python registry_demo.py
```

No `.env` required for this demo.

---

## Sample run output

FastMCP may print banners on stderr; the important lines:

```text
Connected to: time-mcp-server/server.py
Connected to: weather-mcp-server/server.py

Available Tools
----------------
current_time
roll_dice
generate_password
get_weather

Tool Result:
CallToolResult(content=[TextContent(type='text', text='Sunny, 32°C', ...)], ...)
```

The useful payload is **`Sunny, 32°C`** inside `CallToolResult.content[0].text`.

---

## Line-by-line — [`mcp_client.py`](./mcp_client.py)

| Function | What happens |
|----------|----------------|
| `connect(server)` | `Client(server)` — FastMCP spawns the server script over **stdio**; `__aenter__` opens the session. |
| `disconnect(client)` | `__aexit__` shuts down the child process / transport. |
| `discover_tools(client)` | Thin wrapper — see [Where is `list_tools`?](#where-is-list_tools) below. |
| `execute_tool(client, name, arguments)` | Thin wrapper around `client.call_tool(...)` — same idea as discover → `list_tools`. |

---

## Clarifications (study Q&A)

*Notes from chat questions — expand this section when something in the code is unclear.*

### Where is `list_tools`?

**Not in your repo.** You never define `list_tools` in `PROJECT_1/`.

```python
from fastmcp import Client   # Client comes from the fastmcp package

async def discover_tools(client):
    return await client.list_tools()
```

| Layer | What it is |
|-------|------------|
| **`discover_tools`** | Your name in [`mcp_client.py`](./mcp_client.py) — readability for the learning project. |
| **`client.list_tools()`** | Method on **FastMCP `Client`** (library code, e.g. `fastmcp/client/mixins/tools.py` in site-packages). |
| **MCP protocol** | Client sends **`tools/list`** over the open session (stdio to your child `server.py`). |
| **Server side** | Tools are whatever you registered with `@mcp.tool()` in `time-mcp-server/server.py` and `weather-mcp-server/server.py`. |

Call chain:

```text
create_tool_registry
  → discover_tools(client)
      → client.list_tools()          # FastMCP
          → session → MCP tools/list
              → server returns names: current_time, roll_dice, ...
```

**Return value:** a list of tool objects (at minimum **name**, often **description** and **input JSON schema**). `mcp_manager` uses `tool.name` as the registry key.

### Where is `call_tool`?

**Also not in your repo.** Your code only wraps it:

```python
async def execute_tool(client, tool_name, arguments=None):
    if arguments is None:
        arguments = {}
    return await client.call_tool(tool_name, arguments)
```

| Layer | What it is |
|-------|------------|
| **`execute_tool`** | Your function in [`mcp_client.py`](./mcp_client.py). |
| **`client.call_tool(...)`** | Method on **FastMCP `Client`** — same mixin file as `list_tools`: `fastmcp/client/mixins/tools.py`. |
| **MCP protocol** | Client sends **`tools/call`** with `name` + `arguments` JSON to the server. |
| **Server side** | FastMCP dispatches to the Python function behind that `@mcp.tool()` (e.g. `get_weather(city=...)`). |

Call chain for the demo:

```text
run_tool(registry, "get_weather", {"city": "Delhi"})
  → execute_tool(client, "get_weather", {"city": "Delhi"})
      → client.call_tool("get_weather", {"city": "Delhi"})
          → MCP tools/call
              → weather-mcp-server runs get_weather
              → CallToolResult back to client
```

**Return value:** `CallToolResult` (text in `.content[0].text` for simple string tools). `list_tools` discovers names; `call_tool` runs one of them.

### Why wrap `list_tools` as `discover_tools`?

Keeps [`mcp_manager.py`](./mcp_manager.py) readable (“discover then register”) and matches topic **20** naming. You could call `client.list_tools()` directly; the wrapper is style, not requirement.

### Why wrap `call_tool` as `execute_tool`?

Same reason: [`run_tool`](./mcp_manager.py) reads “execute this tool on the right client” without FastMCP jargon. Under the hood it is always **`client.call_tool`**.

### What is `CallToolResult` in the sample output?

FastMCP returns a **result object**, not a plain string. The weather string you care about is usually:

```text
result.content[0].text   →   "Sunny, 32°C"
```

The long `CallToolResult(...)` line in the console is the **whole envelope** (content list, server meta, error flag).

### Better than `print(clients)` / `print(tool_registry)`?

**Avoid** printing the list or dict directly:

```python
print(clients)        # [<fastmcp.client.client.Client object at 0x...>, ...]
print(tool_registry)  # huge dict + nested Client objects — hard to read
```

`clients` holds **live FastMCP `Client` sessions** (sockets/stdio), not file paths. `tool_registry` stores **`client` object references** — repr is for debugging internals, not learning.

Use **`print_registry_summary(clients, tool_registry)`** in [`mcp_manager.py`](./mcp_manager.py) instead:

```text
MCP sessions: 2
  [0] Client-... → current_time, generate_password, roll_dice
  [1] Client-... → get_weather

Tool registry keys (4):
  - current_time
  - generate_password
  - get_weather
  - roll_dice
```

It groups **tool names per session** (`entry["client"] is client`) so you see which server owns which tools. You already get server paths from `connect()`’s `Connected to: ...` lines.

### From `@mcp.tool()` to `Tool(name='current_time', ...)`

Your server code:

```python
@mcp.tool()
def current_time():
    """Return the current date and time."""
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")
```

When you **import** / start `server.py`, `@mcp.tool()` runs **once** and registers a **`FunctionTool`** inside FastMCP — it does **not** call `current_time()` yet.

When the client runs `list_tools()` → MCP **`tools/list`**, the server serializes each registered tool into a **`Tool`** object (MCP types). Each field comes from a specific source:

| Field you see | Where it comes from | For `current_time` |
|---------------|---------------------|--------------------|
| **`name`** | Python function name (unless you pass `@mcp.tool(name="...")`) | `'current_time'` |
| **`title`** | `title=` on decorator, else FastMCP `_default_title(name)` → spaces + Title Case | `'Current Time'` from `current_time` |
| **`description`** | Function **docstring** (first paragraph) | `'Return the current date and time.'` |
| **`input_schema`** | **Signature** → Pydantic JSON Schema (`ParsedFunction.from_function`) | No parameters → `type: object`, **`properties: {}`** |
| **`output_schema`** | Often `None` unless return type / schema inferred or set on decorator | `None` here (string return, no explicit schema) |
| **`execution`**, **`icons`**, **`annotations`** | Defaults / optional decorator args | `None` in your simple tools |
| **`meta`** | FastMCP internal (e.g. `fastmcp.tags`) | `{'fastmcp': {'tags': []}}` |

**`input_schema` for no-arg tools:** the model still expects a JSON **object**, just with **no required fields** — so calls look like `call_tool("current_time", {})`.

Compare **`generate_password(length: int = 12)`:** `input_schema` would gain a `length` property (integer, default 12).

End-to-end:

```text
server.py loaded
  → @mcp.tool registers FunctionTool in FastMCP server

client list_tools()
  → tools/list
  → server returns [Tool(...), Tool(...), ...]
  → your discover_tools() / print sees Tool(name='current_time', title='Current Time', ...)

client call_tool("current_time", {})
  → tools/call
  → server runs current_time() body
  → returns strftime string in CallToolResult
```

Library references (in site-packages, not your repo): decorator `FastMCP.tool` → `FunctionTool.from_function` → `ParsedFunction.from_function` (schema + docstring); `Tool.to_mcp_tool` for wire format; title helper `name.replace("_", " ").title()`.

### What is inside `tool_registry`?

`tool_registry` is a **plain Python dict** built in `create_tool_registry`:

```python
tool_registry[tool.name] = {"client": client, "tool": tool}
```

**Top level — keys:** MCP **tool name** strings (must be unique across the merged registry).

| Key (example) | Value (always a dict with 2 keys) |
|---------------|-----------------------------------|
| `"current_time"` | see below |
| `"get_weather"` | see below |
| … | one entry per tool from both servers |

**Each value** — `entry`:

| Key inside `entry` | Type | Why it is stored |
|--------------------|------|------------------|
| **`"client"`** | FastMCP **`Client`** | The MCP session that owns this tool — `call_tool` must use **this** client (time server vs weather server). |
| **`"tool"`** | MCP **`Tool`** metadata object | From `list_tools()` — `name`, `title`, `description`, `input_schema`, etc. (not the Python function itself). |

**Conceptual shape** after running both servers:

```text
tool_registry = {
    "current_time": {
        "client": <Client connected to time-mcp-server/server.py>,
        "tool": Tool(name='current_time', title='Current Time', description='...', input_schema={...}, ...),
    },
    "roll_dice": { "client": <same Client as current_time>, "tool": Tool(...) },
    "generate_password": { "client": <same Client>, "tool": Tool(...) },
    "get_weather": {
        "client": <Client connected to weather-mcp-server/server.py>,
        "tool": Tool(name='get_weather', ...),
    },
}
```

**What is *not* in the registry:**

| Not stored | Where it lives instead |
|------------|------------------------|
| Server file path (`time-mcp-server/...`) | Only implied by which `client` you held at register time |
| Python source of `def current_time()` | On the **server process**, not in the client dict |
| Tool return values | Only appear after `run_tool` / `call_tool` |

**How `run_tool` uses it:**

```python
entry = tool_registry["get_weather"]
entry["client"]   # which MCP connection
entry["tool"]     # optional: read description/schema for an LLM picker later
execute_tool(entry["client"], "get_weather", {"city": "Delhi"})
```

**Collision rule:** same `tool.name` from two servers → **last server in `servers` list wins**; earlier entry is overwritten.

### What `run_tool` does (line by line)

```python
async def run_tool(tool_registry, tool_name, arguments):
    entry = tool_registry.get(tool_name)
    if entry is None:
        raise ValueError(f"Unknown tool: {tool_name}")
    return await execute_tool(entry["client"], tool_name, arguments)
```

| Line | What happens |
|------|----------------|
| **`tool_registry`** | The merged dict from `create_tool_registry` — you do not pass `clients` separately; the registry already remembers which `client` owns each tool. |
| **`tool_name`** | String MCP name, e.g. `"get_weather"` — must match a **top-level key** in `tool_registry`. |
| **`arguments`** | Dict matching the tool’s `input_schema`, e.g. `{"city": "Delhi"}`. For no-arg tools use `{}`. |
| **`entry = tool_registry.get(tool_name)`** | Lookup. `.get` returns `None` if the name was never registered (typo or wrong server). |
| **`if entry is None: raise ValueError`** | Fail fast — don’t call MCP with a bogus name. |
| **`entry["client"]`** | The FastMCP session that registered this tool — **required** because `get_weather` lives on the weather client, not the time client. |
| **`execute_tool(...)`** | Your wrapper → `client.call_tool(tool_name, arguments)` → MCP **`tools/call`** on that server. |
| **`return await ...`** | Returns **`CallToolResult`** (async all the way up to `registry_demo`). |

**Why not use `entry["tool"]` here?** Metadata is for listing / LLM planning; execution only needs the **correct client** + **name** + **args**. The server already knows how to run the Python function behind that name.

**Example** (`registry_demo.py`):

```text
run_tool(registry, "get_weather", {"city": "Delhi"})
  → entry = {"client": <weather Client>, "tool": Tool(...)}
  → execute_tool(<weather Client>, "get_weather", {"city": "Delhi"})
  → "Sunny, 32°C" inside CallToolResult
```

Wrong name: `run_tool(registry, "get_wether", {...})` → `ValueError: Unknown tool: get_wether` before any MCP call.

### Why pass `tool_name` again if the registry key is already the name?

Looks redundant:

```python
entry = tool_registry.get(tool_name)          # key IS tool_name
return await execute_tool(entry["client"], tool_name, arguments)
#                                      ^^^^^^^^^ again
```

| Reason | Explanation |
|--------|-------------|
| **MCP API shape** | `client.call_tool(name, arguments)` always needs the **name on the wire** — the protocol message is `tools/call` with a `name` field. The client object does not “remember” which single tool you intend; one client handles **many** tools. |
| **Registry vs transport** | `tool_registry` is **your** map (lookup). `execute_tool` / `call_tool` is **generic** transport: “on this session, call **this** name with **these** args.” It only takes `client`, not a full `entry`. |
| **Could we use `entry["tool"].name`?** | **Yes** — that should equal `tool_name` if the registry is consistent. Passing `tool_name` again is explicit and matches what you just looked up; you could write `execute_tool(entry["client"], entry["tool"].name, arguments)` with the same effect. |
| **Alternative design** | `run_tool` could be `execute_tool(entry, arguments)` and pull name from `entry["tool"].name` inside — fewer repeated args, but `execute_tool` would need to know about registry entries instead of staying a thin MCP wrapper. |

**Short answer:** the registry key tells you **which row** and **which client**; `call_tool` still needs the **tool name string** because one client serves multiple tools and MCP asks for the name every time.

### `print_registry_summary` — lines 10–12 (filter tools per client)

```python
tool_names = sorted(
    name for name, entry in tool_registry.items() if entry["client"] is client
)
```

**Goal:** For each MCP session in `clients`, list **only the tools that belong to that session** (not all four merged names on every line).

| Piece | Meaning |
|-------|---------|
| **`tool_registry.items()`** | Every `(tool_name, entry)` pair, e.g. `("get_weather", {client, tool})`. |
| **`entry["client"]`** | The FastMCP `Client` stored when that tool was registered. |
| **`client`** (loop variable) | The current session from `for i, client in enumerate(clients)`. |
| **`entry["client"] is client`** | **Identity check** — same object in memory as the one appended in `create_tool_registry` for that server. Not string compare; “this tool’s row points at **this** connection.” |
| **`name for ... if ...`** | Generator: collect tool **names** that pass the filter. |
| **`sorted(...)`** | Alphabetical order for stable printing (`current_time` before `roll_dice`). |

**Example** with two servers:

```text
clients[0] (time server)  → current_time, generate_password, roll_dice
clients[1] (weather)      → get_weather
```

Tools from the time server share **one** `Client` instance; `get_weather`’s `entry["client"]` is the **other** instance, so it fails the `is client` test when `client` is the time session.

**Why `is`, not `==`?** Each `connect()` returns one `Client` object. Registry stores that same object reference. `is` matches “owned by this session”; `==` might not be defined meaningfully between clients.

**If this filter were wrong:** every session line would print all tool names, and you could not see which server contributed which tools.

**Read it as English:** “Walk every tool in the registry; if this tool’s saved client is **the same connection** I’m printing right now, keep its **name**; then sort those names.”

**Micro walkthrough** — loop is on **time** `client` (`clients[0]`):

| `name` | `entry["client"] is client`? | Kept? |
|--------|------------------------------|-------|
| `current_time` | yes (time client) | ✓ |
| `roll_dice` | yes | ✓ |
| `generate_password` | yes | ✓ |
| `get_weather` | no (weather client) | ✗ |

→ `tool_names = ['current_time', 'generate_password', 'roll_dice']` after `sorted(...)`.

---

## Line-by-line — [`mcp_manager.py`](./mcp_manager.py)

### `print_registry_summary(clients, tool_registry)`

Human-readable debug after the registry is built — see [Better than `print(clients)`?](#better-than-printclients--printtool_registry).

### `create_tool_registry(servers)`

| Step | Code idea |
|------|-----------|
| For each path in `servers` | `client = await connect(server)` |
| Remember clients | append to `clients` list (for cleanup) |
| Discover | `tools = await discover_tools(client)` |
| Register | `tool_registry[tool.name] = {"client": client, "tool": tool}` |
| Summary | `print_registry_summary(...)` — optional debug |

Returns **`(clients, tool_registry)`** — you need **both**: registry to call tools, clients list to disconnect.

### `close_servers(clients)`

Loop `disconnect` — always use `try/finally` in demos so servers do not leak.

### `run_tool(tool_registry, tool_name, arguments)`

High-level: **resolve tool name → right MCP session → call it.** See also [What `run_tool` does (line by line)](#what-run_tool-does-line-by-line).

| Step | Meaning |
|------|---------|
| `entry = tool_registry.get(tool_name)` | Missing name → `ValueError` |
| `execute_tool(entry["client"], ...)` | Must use the **same client** that registered that tool |

---

## Line-by-line — [`registry_demo.py`](./registry_demo.py)

| Block | Meaning |
|-------|---------|
| `servers = [...]` | Two **relative** paths; run from `PROJECT_1/`. |
| `create_tool_registry` | Builds map; prints connection lines from `connect()`. |
| Print tool names | Unsorted iteration — order may vary; use `sorted()` if you want stable listings. |
| `run_tool(..., "get_weather", {"city": "Delhi"})` | Hard-coded demo call (no LLM). |
| `finally: close_servers` | Always tear down MCP children. |

---

## Line-by-line — MCP servers

### Time server

| Piece | Meaning |
|-------|---------|
| `FastMCP("Time Server")` | Server display name for MCP handshake. |
| `@mcp.tool()` | Exposes function to MCP clients. |
| `mcp.run()` | stdio transport when run as `__main__`. |

### Weather server

| Piece | Meaning |
|-------|---------|
| `get_weather(city)` | Looks up city in `WEATHER_DATA` dict; else *"Weather data not available."* |

---

## OpenAI later (not in this folder)

This project stops at **manual** `run_tool`. To add **OpenAI**:

- Use `OpenAI(api_key=os.getenv("OPENAI_API_KEY"))` and `OPENAI_MODEL` / `MODEL_NAME` from your existing `.env` — **not** Ollama `base_url`.
- Pattern: build a text catalog from `tool_registry` → model returns `tool_name` + JSON args → `run_tool(...)`.

Reference planner + loop: [`../../20_MCP_AGENT_LOOP/PROJECT_2/planner.py`](../../20_MCP_AGENT_LOOP/PROJECT_2/planner.py).

---

## Interview one-liner

**Multi-server MCP registry** = one map from **tool name → client**, so the app calls tools without knowing which server file backs them; discover once, execute many, disconnect in `finally`.