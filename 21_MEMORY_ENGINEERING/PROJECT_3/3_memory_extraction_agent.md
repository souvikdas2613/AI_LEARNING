# Memory extraction + MCP agent

**PROJECT_3** = everything in [`PROJECT_2`](../PROJECT_2/2_mcp_agent_semantic_memory.md) **plus** an **extractor LLM** that decides whether to store a **short fact** (not only the full Q&A transcript).

| Layer | What |
|--------|------|
| **Retrieve** | `search_semantic_memories` at start of `loop.py` (same as PROJECT_2) |
| **Episodic save** | `save_memory(user_request, answer)` — full turn |
| **Semantic fact save** | `extract_memory` → if not `NONE`, `save_semantic_memory(fact)` |

**Read first:** [`PROJECT_1`](../PROJECT_1/1_semantic_memory_lab.md) · [`PROJECT_2`](../PROJECT_2/2_mcp_agent_semantic_memory.md) · [`1_introduction_to_memory_engineering.md`](../1_introduction_to_memory_engineering.md).

| File | Role |
|------|------|
| [`runner.py`](./runner.py) | **Entry** — `python runner.py` |
| [`loop.py`](./loop.py) | Agent loop; **`finish_and_remember`** = answer + dual save |
| [`memory_extractor.py`](./memory_extractor.py) | LLM #3 — one fact or **`NONE`** |
| [`memory.py`](./memory.py) | OpenAI embeddings; `save_memory` + **`save_semantic_memory`** |
| [`test_memory_extractor.py`](./test_memory_extractor.py) | Extractor-only smoke (no MCP) |
| [`test_memory.py`](./test_memory.py) | Same seed demo as PROJECT_2 (Souvik) |
| MCP stack | Same as PROJECT_2 — `server.py`, `mcp_client.py`, … |

Run from **`PROJECT_3`** so `memory.db` and `server.py` resolve correctly.

---

## Index

| # | Topic |
|---|--------|
| 1 | [Two saves on finish](#two-saves-on-finish) |
| 2 | [Requirements](#requirements) |
| 3 | [How to run](#how-to-run) |
| 4 | [PROJECT_2 vs PROJECT_3](#project_2-vs-project_3) |
| 5 | [Who calls whom](#who-calls-whom) |
| 6 | [Empty database](#empty-database) |

---

## Two saves on finish

```text
finish_and_remember(state, user_request, format_answer)
    │
    ├─ format_answer(state)     → final text for user
    ├─ finish(state, answer)
    ├─ save_memory(user, answer)     PROJECT_2 style — whole turn embedded
    ├─ fact = extract_memory(user, answer)
    └─ if fact != "NONE":
           save_semantic_memory(fact)   compact row: user_message=fact, assistant=""
```

**Why two rows?**

| Save | Good for | Skip when |
|------|----------|-----------|
| **Full turn** | Exact wording of Q&A | Never on successful finish (same as PROJECT_2) |
| **Extracted fact** | “User’s name is Souvik”, “User works on OSAC” | Extractor returns **`NONE`** (time/dice/password runs) |

Search still scans **one** `memories` table; both row types participate in cosine search.

Example extractor output:

| User | Assistant | Typical extract |
|------|-----------|-----------------|
| `What is the current time?` | `It is 10 PM.` | **`NONE`** |
| `My name is Souvik.` | `Nice to meet you!` | **`User's name is Souvik.`** |
| `roll dice` (after tool run) | answer mentions dice `4` | **`NONE`** (tool noise) |

---

## Requirements

```bash
pip install fastmcp openai python-dotenv numpy
```

`.env` (repo root):

```env
OPENAI_API_KEY=your_key_here
MODEL_NAME=gpt-4o-mini
```

Chat: `task_planner`, `planner`, `answer`, **`memory_extractor`**.  
Embeddings: `memory.py` (`text-embedding-3-small`).

---

## How to run

From **`PROJECT_3`**:

**1 — Optional seed (name question works on first ask):**

```bash
python test_memory.py
```

**2 — Extractor smoke (no MCP):**

```bash
python test_memory_extractor.py
```

**3 — Agent:**

```bash
python runner.py
```

Same input matrix as PROJECT_2 — see [Multi-run checklist](../PROJECT_2/2_mcp_agent_semantic_memory.md#multi-run-checklist-after-python-test_memorypy).

**Extra check after a intro run:**

```bash
python test_memory.py   # or list via sqlite — you may see extra rows where assistant_message is empty (facts)
```

After **`My name is Souvik and I work on OSAC.`** + FINISH, expect extractor print + **`save_semantic_memory`** line in the log.

---

## PROJECT_2 vs PROJECT_3

| | **PROJECT_2** | **PROJECT_3** |
|---|---------------|---------------|
| Retrieve at start | Yes | Yes |
| `save_memory` on finish | Yes | Yes |
| **`extract_memory`** | No | Yes |
| **`save_semantic_memory`** | No | Yes |
| MCP task loop | Yes | Yes (aligned `task_planner` / `planner`) |

---

## Who calls whom

| Step | Function | File |
|------|----------|------|
| 1 | `search_semantic_memories` | `memory.py` |
| 2 | Agent loop / MCP | `loop.py` … |
| 3 | `finish_and_remember` | `loop.py` |
| 4 | `save_memory` | `memory.py` |
| 5 | `extract_memory` | `memory_extractor.py` |
| 6 | `save_semantic_memory` (conditional) | `memory.py` |

---

## Empty database

Same as PROJECT_2: empty `memory.db` + **`What is my name?`** → search **`[]`**, no Souvik until **`test_memory.py`** or a prior intro run that finished and saved.

Each **`finish_and_remember`** adds at least one **full turn** row; may add a **second fact** row when the extractor does not return **`NONE`**.

---

## Limits

| Topic | Detail |
|-------|--------|
| Extractor quality | Depends on `MODEL_NAME`; may over-store or return `NONE` wrongly — tune prompt in `memory_extractor.py` |
| Duplicate facts | No dedup — same fact twice creates two rows |
| Tool runs | Extractor instructed to skip tool results; full turn still saved in `save_memory` |

**Next:** dedup, separate `facts` table, or Mem0-style policies — see chapter intro §7.
