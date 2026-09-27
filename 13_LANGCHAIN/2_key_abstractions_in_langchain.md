# Key abstractions in LangChain

Note **2** of **10** — folder `13_LANGCHAIN`.

**Previous:** [`1_introduction_to_langchain.md`](./1_introduction_to_langchain.md) · **Next:** [`3_why_langchain_needed.md`](./3_why_langchain_needed.md)

LangChain defines several abstractions so you do not wire providers and data stores by hand every time. Three are used most often in this course:

---

## 1. LLM

- Represents a **language model** (e.g. OpenAI GPT, Amazon Titan on Bedrock).
- Encapsulates the **model interface** — same pattern across providers.
- In modern LangChain you often use **chat models** (`ChatOpenAI`, `ChatBedrock`, etc.) instead of legacy string-in/string-out `LLM` classes; the mental model is the same: **one abstraction for “call the model.”**

---

## 2. Retriever

- Interface to a **vector store** or search index (e.g. Chroma, OpenSearch, pgvector).
- Used in **RAG**: given a user query, fetch **relevant documents** to put into the prompt.
- Enriches prompts with **retrieved context** instead of relying only on the model’s training data.

See also: [`2_rag_architecture_and_workflow.md`](../12_RAG_Retrieval_Augmented_Generation/2_rag_architecture_and_workflow.md).

---

## 3. Memory

- Represents **conversation history** for a chatbot.
- Abstracts the underlying structure (usually a **list of messages**).
- **Manages context** across turns because the LLM itself does not remember prior calls.

See: [`7_memory.md`](./7_memory.md).

---

## How they fit together (mental model)

```text
User input
    → (optional) Memory loads prior messages
    → (optional) Retriever fetches documents
    → Prompt template combines everything
    → LLM / Chat model generates output
```

Chains and agents (later notes) are how you **wire** these abstractions into a full app.
