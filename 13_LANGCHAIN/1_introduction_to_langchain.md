# Introduction to LangChain

Chapter notes (folder `13_LANGCHAIN`) — note **1** of **10**.

**Read in order:** `1_` → `10_` (this file is **1**).

| # | Note | Topics |
|---|------|--------|
| 1 | **This file** | What LangChain is, languages, components, LCEL |
| 2 | [`2_key_abstractions_in_langchain.md`](./2_key_abstractions_in_langchain.md) | LLM, Retriever, Memory |
| 3 | [`3_why_langchain_needed.md`](./3_why_langchain_needed.md) | Limits of raw LLMs, chaining, lifecycle |
| 4 | [`4_langchain_vs_langgraph.md`](./4_langchain_vs_langgraph.md) | Framework vs graph orchestration |
| 5 | [`5_prompt_templates.md`](./5_prompt_templates.md) | Reusable prompts, variables |
| 6 | [`6_indexes_loaders_retrievers_vector_stores.md`](./6_indexes_loaders_retrievers_vector_stores.md) | RAG building blocks in LangChain |
| 7 | [`7_memory.md`](./7_memory.md) | ConversationBufferMemory, ConversationChain |
| 8 | [`8_chains.md`](./8_chains.md) | Sequencing components, LLMChain |
| 9 | [`9_agents.md`](./9_agents.md) | Tools, reasoning, actions |
| 10 | [`10_embeddings_and_vector_store.md`](./10_embeddings_and_vector_store.md) | Embeddings, Chroma, Milvus, indexing chunks |

**Practice notebooks:** [`rag_langchain_chunks_vector_db_visualization.ipynb`](./rag_langchain_chunks_vector_db_visualization.ipynb) (chunks, embeddings, Chroma, t-SNE) then [`rag_langchain_retriever_qa_gradio.ipynb`](./rag_langchain_retriever_qa_gradio.ipynb) (retriever + chat UI) — best after note **6**.

**Official docs:** [LangChain Python introduction](https://python.langchain.com/docs/introduction/) · [GitHub — langchain-ai/langchain](https://github.com/langchain-ai/langchain)

Related: [`1_introduction_to_rag.md`](../12_RAG_Retrieval_Augmented_Generation/1_introduction_to_rag.md) · [`agents_and_tools.md`](../6_AGENTS_AND_TOOLS/agents_and_tools.md)

---

## What is LangChain?

**LangChain** is an open-source framework for developing applications powered by **large language models (LLMs)**.

- Available in **Python**, **TypeScript**, and **JavaScript**.
- Created in **late 2022**; goal is to let you build LLM apps quickly by **stitching** functionality into a **chain** of processing steps.

LangChain simplifies AI app development by providing a **standard way** to connect language models with:

- external data sources,
- prompt templates,
- indexes and retrievers,
- memory,
- chains,
- agents and tools.

---

## Components vs chains

| Idea | Meaning |
|------|--------|
| **Components** | Modular, reusable building blocks — e.g. **Models**, **Prompt Templates**, **Output Parsers**. |
| **Chains** | A **workflow** for a task (Q&A, summarization, etc.) built by linking components. |

**LangChain Expression Language (LCEL)** lets you connect components so data flows from user input to final output. This course does **not** use LCEL extensively; knowing it exists is enough for now.

---

## Focus of this module

| Area | Role |
|------|------|
| **Models** | Call LLMs, chat models, embeddings |
| **Prompt templates** | Parameterized, reusable prompts |
| **Indexes** | Load documents, embed, store, retrieve |
| **Memory** | Conversation history in context |
| **Chains** | Sequence steps (e.g. draft blog → generate title) |
| **Agents** | LLM decides which tools to call and in what order |
