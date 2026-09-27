# LangChain agents

Note **9** of **10** — folder `13_LANGCHAIN`.

**Previous:** [`8_chains.md`](./8_chains.md) · **Next:** [`10_embeddings_and_vector_store.md`](./10_embeddings_and_vector_store.md)

Related: [`agents_and_tools.md`](../6_AGENTS_AND_TOOLS/agents_and_tools.md) · [`tool_functions_1.md`](../5_TOOLS_FUNCTIONS/tool_functions_1.md)

---

## Limits of LLMs alone

LLMs excel at language from pretraining but are **weak** at:

- exact **math** and symbolic logic,
- **live** facts (unless retrieved or tool-fed),
- **rule-based** workflows without tools.

For those cases you need **external systems**: search, calculators, APIs, databases, or **code execution**.

---

## What is an agent?

A **LangChain agent** acts as a **reasoning engine**:

1. Reads the user goal and context.
2. **Decides** which **action** to take (often which **tool** to call).
3. **Observes** the tool result.
4. Repeats until it can produce a final answer.

An **action** might be:

- run a **search**,
- call a **calculator**,
- query a **database**,
- invoke a custom **API**.

**LLMChain** is a **basic chain** (fixed steps). An **agent** chooses steps **dynamically**.

---

## Agents vs chains

| | **Chain** | **Agent** |
|---|-----------|-----------|
| Control flow | **Fixed** by you | **LLM-planned** (with tool loop) |
| Best for | Pipelines you can diagram upfront | Open-ended tasks needing tools |
| Risk | Predictable | Must guard tools, limits, and parsing |

---

## How this connects to the module

| Piece | Role in agent apps |
|-------|---------------------|
| **Models** | Decide next action and final reply |
| **Tools** | Search, math, APIs (see topic 5 & 6 in repo) |
| **Memory** | Multi-turn agent context |
| **Retrievers** | RAG as a tool or chain step |
