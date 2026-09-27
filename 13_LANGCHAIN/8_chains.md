# Using chains to sequence components

Note **8** of **10** — folder `13_LANGCHAIN`.

**Previous:** [`7_memory.md`](./7_memory.md) · **Next:** [`9_agents.md`](./9_agents.md)

---

## Why chain?

Complex apps rarely need **one** model call. You might:

1. Ask the LLM to **draft a blog** on a topic.
2. Pass that draft into a second step to **generate a title**.

**Chains** run LangChain components **in sequence** — LLM calls, retrievers, memory, APIs, or **nested chains**.

---

## What is a chain?

At the core, a **chain** is a set of components that run together.

Each step has:

- a defined **input** format,
- an **output** passed to the next step (or returned to the user).

**LLMChain** (classic pattern) combines:

- an **LLM** (or chat model),
- a **prompt template**,
- values for the template variables,

and returns the model output (sometimes via an **output parser** for structured data).

Modern code often uses **LCEL** (`prompt | model | parser`) for the same idea; this module focuses on the **concept** of sequencing.

---

## Chaining with memory and retrievers

Examples of multi-component chains:

| Pattern | Steps |
|---------|--------|
| **RAG chain** | Retrieve docs → build prompt with context → LLM answer |
| **Conversational RAG** | Load memory → retrieve → prompt → LLM → update memory |
| **Two-step content** | LLM body → LLM title (or summarize → translate) |

---

## Minimal mental model

```text
Input → [Component A] → [Component B] → … → Output
              ↑              ↑
           LLMChain      another chain or tool
```
