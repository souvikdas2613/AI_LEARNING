# MCP agent loop

Chapter notes for **Souvik’s** AI learning journey (folder `20_MCP_AGENT_LOOP`).

**Topic 19 PROJECT_3** is a **one-shot** MCP agent: planner picks **one** tool, MCP runs it, a second LLM answers.  
**This chapter** adds what production agents actually need: a **state object**, a **while loop**, and a planner that sees **past actions + observations** until it returns `FINISH`.

Related earlier chapters:

- Mini agent (local tools, one tool per chat turn) — [`18_AI_AGENTS_INTRO/`](../18_AI_AGENTS_INTRO/)
- MCP theory + labs — [`19_MCP_MODEL_CONTEXT_PROTOCOL/`](../19_MCP_MODEL_CONTEXT_PROTOCOL/)
- One-shot MCP agent — [`9_mcp_agent_lab.md`](../19_MCP_MODEL_CONTEXT_PROTOCOL/PROJECT_3/9_mcp_agent_lab.md)

---

## Hands-on project

| Folder | Files | Topic |
|--------|--------|--------|
| [`PROJECT_1/`](./PROJECT_1/) | [`runner.py`](./PROJECT_1/runner.py) · [`loop.py`](./PROJECT_1/loop.py) · [`state.py`](./PROJECT_1/state.py) · [`planner.py`](./PROJECT_1/planner.py) · [`executor.py`](./PROJECT_1/executor.py) · [`mcp_client.py`](./PROJECT_1/mcp_client.py) · [`server.py`](./PROJECT_1/server.py) · [`test_state.py`](./PROJECT_1/test_state.py) · notes [`1_mcp_agent_loop.md`](./PROJECT_1/1_mcp_agent_loop.md) | Looping MCP agent — plan → act → remember until `FINISH` |
| [`PROJECT_2/`](./PROJECT_2/) | [`runner.py`](./PROJECT_2/runner.py) · [`loop.py`](./PROJECT_2/loop.py) · [`state.py`](./PROJECT_2/state.py) · [`task_planner.py`](./PROJECT_2/task_planner.py) · [`planner.py`](./PROJECT_2/planner.py) · [`executor.py`](./PROJECT_2/executor.py) · [`answer.py`](./PROJECT_2/answer.py) · [`mcp_client.py`](./PROJECT_2/mcp_client.py) · [`server.py`](./PROJECT_2/server.py) · notes [`2_mcp_task_agent_loop.md`](./PROJECT_2/2_mcp_task_agent_loop.md) | Task decomposition + `TASK`/`TOOL` loop until all tasks done |

Start here: [`PROJECT_1/1_mcp_agent_loop.md`](./PROJECT_1/1_mcp_agent_loop.md).  
Next: [`PROJECT_2/2_mcp_task_agent_loop.md`](./PROJECT_2/2_mcp_task_agent_loop.md) (decompose → task-aware planner → answer in `answer.py`).  
Why `python runner.py` + `time` prints the planner **twice** then `FINISH`: [Real run — `User : time`](./PROJECT_1/1_mcp_agent_loop.md#real-run--user--time).

---

## Quick start

```bash
pip install fastmcp openai python-dotenv
```

`.env`:

```env
OPENAI_API_KEY=your_key_here
MODEL_NAME=gpt-4o-mini
```

From **`PROJECT_1`** or **`PROJECT_2`**:

```bash
python test_state.py    # PROJECT_1 only
python runner.py
```

You do **not** start `server.py` in a second terminal.
