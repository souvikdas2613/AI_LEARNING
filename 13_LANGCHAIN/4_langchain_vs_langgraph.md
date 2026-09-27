# LangChain vs LangGraph

Note **4** of **10** — folder `13_LANGCHAIN`.

**Previous:** [`3_why_langchain_needed.md`](./3_why_langchain_needed.md) · **Next:** [`5_prompt_templates.md`](./5_prompt_templates.md)

Related: [`agents_and_tools.md`](../6_AGENTS_AND_TOOLS/agents_and_tools.md)

---

## LangGraph in one line

**LangGraph** is a framework for building **stateful, multi-step AI agents and workflows**.

Think of it as:

> **LLM + tools + state + control flow = LangGraph**

**LangGraph is not an LLM.** It is the **orchestration layer** that controls how an LLM and tools work together (what runs next, what gets remembered, when to loop or branch).

---

## Simple example — troubleshooting agent

Suppose you build an AI agent for ops support:

```text
User: "My OpenShift pod is failing"
              ↓
        ┌─────────────┐
        │   Analyze   │
        └──────┬──────┘
               ↓
        ┌─────────────┐
        │ Check logs  │
        └──────┬──────┘
               ↓
        ┌─────────────┐
        │ Find cause  │
        └──────┬──────┘
               ↓
        ┌─────────────┐
        │ Suggest fix │
        └──────┬──────┘
               ↓
            Answer
```

LangGraph lets you represent those steps explicitly as **nodes** (work units) and **edges** (what happens next). **State** carries context between steps — e.g. pod name, log snippets, hypothesis so far.

---

## Why “Graph”?

A real agent does not have to be a straight line. You need **branching**, **loops**, and **decisions**:

```text
             ┌──────────────┐
             │ Analyze issue│
             └──────┬───────┘
                    ↓
              Is more info
                 needed?
               /          \
             YES           NO
              ↓             ↓
        Check logs       Give answer
              ↓
        Analyze again
              │
              └──────────────→
```

That **looping, branching, and state management** is where LangGraph shines. LangChain **chains** are great for fixed pipelines; LangGraph is for workflows where the **path depends on intermediate results**.

---

## LangChain vs LangGraph

| | **LangChain** | **LangGraph** |
|---|----------------|----------------|
| **One line** | Components for building LLM applications | Orchestration for **complex / stateful** agent workflows |
| **Mental model** | `LLM + Prompt + Tools + Retriever` | Agent loop: reason → tool → result → reason again → … |
| **Control flow** | Mostly **linear** chains (you define the sequence) | **Graph**: nodes, edges, conditions, cycles |
| **State** | Memory helpers; you wire what goes in each call | **First-class graph state** across steps (and persistence options) |
| **Analogy** | **Toolbox** — models, prompts, RAG, tools | **Workflow engine** on top of that toolbox |

**LangChain** (straight pipeline):

```text
LLM + Prompt + Tools + Retriever
        → run in a sequence you designed
```

**LangGraph** (agent loop):

```text
       Agent (LLM decides)
         ↓
    Tool call
         ↓
      Result
         ↓
    Reason again
         ↓
    Another tool (maybe)
         ↓
      Final answer
```

You often put **LangChain** pieces (chat model, retriever, tools) **inside** LangGraph **nodes**.

---

## Course module vs next step

| Stage | What to learn |
|-------|----------------|
| **Notes 1–9** (`13_LANGCHAIN`) | LangChain — models, prompts, indexes, memory, chains, agents |
| **After that** | LangGraph when you need explicit graphs, **loops**, **multi-agent** flows, or **pause/resume** workflows |

---

## Learning example — simple app vs agentic workflow

A **simple** movie-style recommender might look like:

```text
User
 ↓
Python
 ↓
External API (e.g. movie DB)
 ↓
OpenAI
 ↓
Recommendation
```

One script, one path every time — LangChain (or plain API calls) is enough.

A **LangGraph-style** version could look like:

```text
User
 ↓
Understand request
 ↓
Search movie DB
 ↓
Evaluate candidates
 ↓
Call another tool if needed (ratings, filters, etc.)
 ↓
Generate recommendation
 ↓
Check response (quality / policy)
 ↓
Final answer
```

That moves you from a **single pipeline** to an **agentic workflow** — the model can **choose** extra steps instead of you hard-coding every branch.

---

## Quick recap

- **LangChain** = building blocks and integrations for LLM apps (RAG, chat, tools, chains).
- **LangGraph** = **graph + state** for agents that branch, loop, and coordinate multiple steps or agents.
- Use LangChain first; add LangGraph when control flow is too complex for a simple chain.
