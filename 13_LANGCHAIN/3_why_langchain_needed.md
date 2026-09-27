# Why LangChain is needed

Note **3** of **10** — folder `13_LANGCHAIN`.

**Previous:** [`2_key_abstractions_in_langchain.md`](./2_key_abstractions_in_langchain.md) · **Next:** [`4_langchain_vs_langgraph.md`](./4_langchain_vs_langgraph.md)

---

## What LLMs do well — and where they struggle

LLMs are pretrained on large text collections. They can:

- generate text,
- summarize,
- answer questions,
- do sentiment analysis,
- and more.

They struggle when the task needs:

- **Out-of-domain or private data** (your docs, live DB, today’s prices).
- **Conversational context** across multiple turns (the model does not retain state between API calls).

That often leads to **hallucinations** or **inaccurate** answers. A **single** prompt is not always enough; you may need **several steps** (retrieve → reason → call a tool → answer).

---

## What LangChain provides

LangChain is a framework for **LLM-powered applications**. It offers **building blocks** so you do not implement everything from scratch.

It aims to simplify the full **lifecycle**:

| Stage | LangChain helps with |
|-------|----------------------|
| **Development** | Prompts, chains, integrations |
| **Production** | Patterns for memory, retrieval, agents |
| **Deployment** | Ecosystem of connectors (cloud, vector DBs, tools) |

---

## State and multistep reasoning

**LLMs do not retain state** between invocations. Your app must supply context — e.g. full chat history in the prompt for a natural chat experience.

For **multistep** problems (find info → calculate → summarize), the app must **sequence** steps. LangChain provides components for:

- **Managing context** (memory),
- **Sequencing** interactions (chains),
- **Choosing actions** (agents + tools).

---

## Plain English

Without LangChain you can still call an LLM API in a loop. With LangChain you get **named patterns** (retriever, memory, chain, agent) that match how real products are built — especially **RAG** and **tool-using assistants**.
