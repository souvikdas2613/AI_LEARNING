# PROJECT_2 — multi-server MCP + OpenAI agent loop

**PROJECT_1** = registry + manual tool call ([`../PROJECT_1/registry_demo.md`](../PROJECT_1/registry_demo.md)).  
**PROJECT_2** = same registry + **OpenAI planner loop** → tool calls → natural-language answer.

**stdio vs remote HTTP:** [`../mcp_remote_http_transport.md`](../mcp_remote_http_transport.md)

| Script | API key | Role |
|--------|---------|------|
| [`registry_demo.py`](./registry_demo.py) | No | MCP smoke test (same idea as PROJECT_1) |
| [`runner.py`](./runner.py) | **`OPENAI_API_KEY`** | Interactive agent — you type a request |

---

## Why it is needed (utility)

| Piece | Benefit |
|-------|---------|
| **Registry + loop** | Real agents: discover tools once, then **repeat** plan → act → observe. |
| **OpenAI planner** | Model picks `{"tool", "arguments"}` JSON — no hand-coded `run_tool(...)` per question. |
| **`format_answer`** | Second LLM call turns tool observations into a user-facing reply. |
| **`state` + max_steps** | Caps runaway loops; stores actions/observations for the planner. |
| **Two MCP servers** | Planner must choose among time + weather tools via one `tool_registry`. |

---

## OpenAI `.env` (not Ollama)

Loads `AI_LEARNING/AI_LEARNING/.env` then local `.env` (same as RAG / topic 20).

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4.1-mini
```

**Removed from this project:** `BASE_URL`, `API_KEY`, `MODEL` aimed at local/Ollama gateways.  
Client is **`OpenAI(api_key=os.getenv("OPENAI_API_KEY"))`** only — no `base_url='http://localhost:11434/v1'`.

Model: `OPENAI_MODEL` or `MODEL_NAME`, else **`gpt-4.1-mini`**.

---

## Layout

```text
runner.py          # entry: registry → input → loop → answer
loop.py            # plan → execute → observe → repeat
planner.py         # OpenAI → JSON action
executor.py        # action → run_tool → observation text
state.py           # dict: actions, observations, steps
mcp_client.py      # connect / list_tools / call_tool
mcp_manager.py     # tool_registry + print_registry_summary
registry_demo.py   # no LLM
time-mcp-server/
weather-mcp-server/
```

---

## Agent flow

```text
runner.main()
  → create_tool_registry(SERVERS)
  → user_request = input()
  → run_agent_loop(...)

run_agent_loop:
  while steps < max_steps and not finished:
      action = planner(state, tools)     # OpenAI JSON
      if action["tool"] == "FINISH":
          format_answer(state) → finish → break
      observation = execute_action → run_tool(registry, ...)
      add_action / record_observation / next_step
```

MCP details (`list_tools`, `call_tool`, `tool_registry` shape): see **Clarifications** in [`../PROJECT_1/registry_demo.md`](../PROJECT_1/registry_demo.md).

---

## How to run

```bash
pip install fastmcp openai python-dotenv
```

From **`PROJECT_2`**:

```bash
python registry_demo.py    # MCP only
python runner.py             # full agent (needs API key)
```

### Sample session shape (`runner.py`)

```text
Connected to: time-mcp-server/server.py
Connected to: weather-mcp-server/server.py
MCP sessions: 2
...

Available Tools
----------------
current_time
generate_password
get_weather
roll_dice

User : What is the weather in Paris?

Planner Selected: {'tool': 'get_weather', 'arguments': {'city': 'Paris'}}
Planner Selected: {'tool': 'FINISH', 'arguments': {}}

Final Answer:
It's cloudy and about 9°C in Paris.
```

Exact planner JSON and wording vary by model.

---

## Line-by-line — key files

### `planner.py`

| Piece | Role |
|-------|------|
| `build_tool_descriptions` | Feeds planner tool `name`, `description`, `input_schema`. |
| `planner(state, tools)` | Prompt with request, past actions/observations, tool list. |
| Return | `{"tool": "...", "arguments": {...}}` or `FINISH`. |
| `_parse_planner_json` | Strips ``` fences if model wraps JSON. |

### `executor.py`

Runs `run_tool(tool_registry, tool_name, arguments)`; returns **text** from `CallToolResult.content[0].text`.

### `loop.py`

Orchestrates planner → executor → state updates; calls `format_answer` on `FINISH`.

### `runner.py`

`format_answer` — second OpenAI call with actions + observations; must not leak “tools” in the prompt rules.

### `state.py`

| Field | Meaning |
|-------|---------|
| `actions` | List of planner JSON actions taken |
| `observations` | Tool results per step |
| `max_steps` | Default **5** |
| `final_answer` | Set on FINISH |

### MCP layer

Same as PROJECT_1: [`mcp_client.py`](./mcp_client.py), [`mcp_manager.py`](./mcp_manager.py), [`print_registry_summary`](./mcp_manager.py).

---

## Clarifications (study Q&A)

*Add notes here when you ask in chat — PROJECT_1 doc has deeper MCP wire-format Q&A.*

### Planner JSON vs `run_tool`

- **Planner** outputs abstract `tool` + `arguments` (strings/dicts).
- **`run_tool`** resolves `tool` in `tool_registry`, uses stored `client`, calls MCP **`tools/call`**.
- **`executor`** strips `CallToolResult` to plain text for `observations` so the next planner turn reads sentences, not Python objects.

### Why two OpenAI calls?

| Call | When | Job |
|------|------|-----|
| **Planner** | Each loop step (until FINISH) | Decide next tool |
| **format_answer** | Once on FINISH | Natural language for the user |

### `tools` list vs `tool_registry`

- **`tools`** — metadata only for planner prompts (`name`, `description`, schema).
- **`tool_registry`** — same tools plus **`client`** for execution.

---

## Compare PROJECT_1 vs PROJECT_2

| | PROJECT_1 | PROJECT_2 |
|---|-----------|-----------|
| LLM | None | OpenAI planner + answer |
| Entry | `registry_demo.py` | `runner.py` |
| Tool choice | Hard-coded | Model JSON |
| Loop | Single call | `loop.py` up to `max_steps` |

---

## Interview one-liner

**MCP agent loop:** merge multi-server tools into one registry; **OpenAI** returns the next `tool` + `arguments`; execute via MCP; store observations; **FINISH** → format a user answer.