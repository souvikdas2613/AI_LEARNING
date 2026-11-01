# MCP task agent + semantic memory

**PROJECT_2** = [`20_MCP_AGENT_LOOP/PROJECT_2`](../../20_MCP_AGENT_LOOP/PROJECT_2/) **plus** persistent **semantic memory** from [`PROJECT_1`](../PROJECT_1/1_semantic_memory_lab.md).

| Layer | What |
|--------|------|
| **MCP agent** | Decompose → plan (`TASK` / `TOOL`) → MCP tools → answer |
| **Semantic memory** | SQLite + `text-embedding-3-small` — **retrieve** before the loop, **save** after a successful finish |

**Read first:** [`PROJECT_1/1_semantic_memory_lab.md`](../PROJECT_1/1_semantic_memory_lab.md) (storage + `min_score` / `max_results`) · [`20_MCP_AGENT_LOOP/PROJECT_2/2_mcp_task_agent_loop.md`](../../20_MCP_AGENT_LOOP/PROJECT_2/2_mcp_task_agent_loop.md) (task loop without memory) · [`1_introduction_to_memory_engineering.md`](../1_introduction_to_memory_engineering.md).

| File | Role |
|------|------|
| [`runner.py`](./runner.py) | **Entry** — `python runner.py` |
| [`loop.py`](./loop.py) | Retrieve memories → decompose → agent loop → **`finish_and_remember`** |
| [`memory.py`](./memory.py) | Same API as PROJECT_1 (`max_results`, `min_score`, OpenAI embeddings) |
| [`state.py`](./state.py) | Session state + `state["memories"]` from search hits |
| [`task_planner.py`](./task_planner.py) | LLM #0 — skips tools for memory / chat questions |
| [`planner.py`](./planner.py) | LLM #1 — sees `state["memories"]` |
| [`answer.py`](./answer.py) | LLM #2 — sees `state["memories"]` |
| [`test_memory.py`](./test_memory.py) | Memory-only smoke (no MCP) — seeds **Souvik** demo rows |
| MCP stack | [`server.py`](./server.py) · [`mcp_client.py`](./mcp_client.py) · [`executor.py`](./executor.py) |

Run from **`PROJECT_2`** so `memory.db` and `server.py` resolve correctly.

---

## Index

| # | Topic |
|---|--------|
| 1 | [Memory + agent flow](#memory--agent-flow) |
| 2 | [Requirements](#requirements) |
| 3 | [How to run](#how-to-run) |
| 4 | [Two kinds of user requests](#two-kinds-of-user-requests) |
| 5 | [PROJECT_1 vs PROJECT_2 vs Ch20 PROJECT_2](#project_1-vs-project_2-vs-ch20-project_2) |
| 6 | [Who calls whom](#who-calls-whom) |
| 7 | [Line by line — memory hooks in loop.py](#line-by-line--memory-hooks-in-loopy) |

---

## Memory + agent flow

```text
runner.py
  create_database()
  MCP connect + list tools
  user_request = input()
        │
        ▼
loop.run_agent_loop
        │
        ├─ search_semantic_memories(user_request, max_results=3)
        │     └─ add_memory(state, hit) for each dict
        │
        ├─ decompose_task(user_request) → state["tasks"]
        │
        └─ while can_continue:
               ├─ all tasks done?  → finish_and_remember → save_memory
               ├─ planner FINISH?  → finish_and_remember → save_memory
               └─ else TASK+TOOL → MCP → update state
        │
        ▼
print state["final_answer"]
```

**Retrieve (start of run):** [`search_semantic_memories`](./memory.py) embeds the **current** user line and loads past turns that pass **`min_score`** (default **0.20**). Hits land in **`state["memories"]`** for planner and answer prompts.

**Save (end of run):** [`finish_and_remember`](./loop.py) calls [`format_answer`](./answer.py), then [`save_memory(user_request, answer)`](./memory.py). The pair *(question, final answer)* is embedded and inserted for **next** runs.

Both finish paths use the same helper (tasks all completed **or** planner returns **`FINISH`**).

---

## Requirements

```bash
pip install fastmcp openai python-dotenv numpy
```

`.env` (repo root; `load_dotenv()` finds it):

```env
OPENAI_API_KEY=your_key_here
MODEL_NAME=gpt-4o-mini
```

| Variable | Used in |
|----------|---------|
| `OPENAI_API_KEY` | Embeddings (`memory.py`) + chat (`task_planner`, `planner`, `answer`) |
| `MODEL_NAME` | Chat only |

---

## How to run

From **`PROJECT_2`**:

**1 — Seed memory (optional first time):**

```bash
python test_memory.py
```

Clears the table, saves three demo turns (name **Souvik**), runs one search.

**First run with an empty `memory.db`:** If you skip step 1 and go straight to `runner.py` with `What is my name?`, search returns **`Results: []`** — nothing to retrieve. The agent can only say it does not know until you **store** a name (step 1, or a prior run like `My name is Souvik` that finishes and calls `save_memory`).

**2 — Agent with memory:**

```bash
python runner.py
```

Examples:

| User line | Expected behavior |
|-----------|-------------------|
| `What is my name?` | No MCP tasks (decomposer returns empty); planner **FINISH**; answer uses retrieved memory; **save_memory** stores this Q&A |
| `roll dice` | One task → **Observation:** from `roll_dice` |
| `get time, roll dice and generate password` | Three tasks + MCP tools (like Ch20 PROJECT_2); finish when all complete; **save_memory** stores full exchange summary |
| `What is photosynthesis?` | Empty task plan (general knowledge); **FINISH**; LLM answer only — **no** MCP |
| `hello, how are you?` | Empty task plan (chat); **FINISH**; polite reply — **no** MCP |

### Multi-run checklist (after `python test_memory.py`)

Run **`python runner.py`** once per line below from **`PROJECT_2`**. Wait for **Task Plan** (memory search runs first).

| # | You type | Task Plan | MCP `Observation:`? | Final answer should |
|---|----------|-----------|------------------------|---------------------|
| 1 | `What is my name?` | *(empty)* | No | Mention **Souvik** (from DB row seeded in `test_memory.py`) |
| 2 | `roll dice` | Roll the dice | Yes — integer 1–6 | Real dice value from tool |
| 3 | `get time, roll dice and generate password` | 3 lines | Yes — time, dice, password string | All three facts |
| 4 | `What is photosynthesis?` | *(empty)* | No | Short science explanation (not from MCP) |
| 5 | `hello, how are you?` | *(empty)* | No | Greeting only |

Each successful finish also calls **`save_memory`** — later runs may retrieve those turns in **Relevant Previous Memories** (scores depend on similarity).

### Empty database — what happens on first `runner.py`

```text
create_database()          → empty table (new memory.db)
search_semantic_memories     → Results: []  (no rows yet)
decompose_task               → empty for "What is my name?"
planner → FINISH
format_answer                → no Souvik in state["memories"] → "I don't know your name"
save_memory                  → stores THAT Q&A for next time (still not your real name)
```

To get **Souvik** on the first name question: run **`python test_memory.py`** once, **or** first ask **`My name is Souvik.`** (FINISH + save), **then** in a **second** `runner.py` session ask **`What is my name?`**

**Sample (run 1, 2026-11-01):** Final answer snippet — *Your name is Souvik. Nice to meet you!* (only after DB was seeded)

---

## Two kinds of user requests

| Type | Task planner | MCP | Memory retrieve | Memory save |
|------|--------------|-----|-----------------|-------------|
| **Memory / chat** | Empty task list | Not used | Prior turns in prompt | After **FINISH** |
| **Tool workflow** | Multiple tasks | Used each step | Still runs (may be empty) | After **FINISH** or all tasks done |

[`task_planner.py`](./task_planner.py) **CRITICAL RULE** avoids inventing tool tasks for “what is my name?” so the loop can go straight to **FINISH** and [`answer.py`](./answer.py).

---

## PROJECT_1 vs PROJECT_2 vs Ch20 PROJECT_2

| | **PROJECT_1** | **PROJECT_2 (this folder)** | **Ch20 PROJECT_2** |
|---|---------------|----------------------------|---------------------|
| Focus | Learn embed + search | Agent + **persistent** memory | Task MCP agent only |
| Entry | `test_memory.py` | `runner.py` | `runner.py` |
| `memory.py` | Yes | **Same stack** (OpenAI, `min_score`, `max_results`) | No |
| Save after run | Manual in demo script | **Automatic** on finish | No |
| Retrieve before run | In `test_memory.py` only | **`loop.py`** at start | No |

**Do not mix** `memory.db` between folders if one was built with a different embedding model. Use separate dirs or delete `memory.db` when switching labs.

Search tuning: [`PROJECT_1` Search logic](../PROJECT_1/1_semantic_memory_lab.md#search-logic--min_score-max_results-and-the-loop).

---

## Who calls whom

| Order | Caller | Callee | Result |
|-------|--------|--------|--------|
| 1 | `runner.py` | `create_database` | Table ready |
| 2 | `runner.py` | `run_agent_loop` | Full run |
| 3 | `loop.py` | `search_semantic_memories` | `state["memories"]` |
| 4 | `loop.py` | `decompose_task` | `state["tasks"]` |
| 5 | `loop.py` | `planner` / MCP / `finish_and_remember` | Tools or final answer |
| 6 | `finish_and_remember` | `format_answer` → `finish` → `save_memory` | Row in SQLite for next session |

---

## Line by line — memory hooks in loop.py

| Block | Code idea |
|-------|-----------|
| After `create_state` | `search_semantic_memories(user_request, max_results=3)` — default **`min_score=0.20`** |
| Loop | `for memory in memories: add_memory(state, memory)` |
| `finish_and_remember` | One place for **`format_answer`**, **`finish`**, **`save_memory(user_request, answer)`** |
| `all_tasks_completed` branch | Calls **`finish_and_remember`** (was missing save before) |
| `decision == "FINISH"` branch | Same **`finish_and_remember`** |

---

## Limits

| Topic | Detail |
|-------|--------|
| Raw dicts in prompts | `state["memories"]` is printed as Python structures — fine for learning; format nicer strings in a later project |
| One save per run | Whole user line + final answer text — not per-tool micro-memories |
| `max_steps` | Default **8** in [`state.py`](./state.py) |
| Short tool lines (`roll dice`) | Need a **Task Plan** line + **Observation:** from MCP; if you only see **FINISH** with no Observation, update `task_planner.py` / `planner.py` (tool vs memory rules) |
| Pause before **Task Plan** | `search_semantic_memories` runs first (embed + score each row) |
| Debug prints | [`memory.py`](./memory.py) traces embed/search like PROJECT_1 (no giant `print(rows)` dump) |

**Next:** refine extraction (what to store), episodic vs semantic split, or vector DB at scale — see chapter intro §7.
