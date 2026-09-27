# Storing and retrieving data with memory

Note **7** of **10** — folder `13_LANGCHAIN`.

**Previous:** [`6_indexes_loaders_retrievers_vector_stores.md`](./6_indexes_loaders_retrievers_vector_stores.md) · **Next:** [`8_chains.md`](./8_chains.md)

Related: [`README_LLM_STATELESS_NO_MEMORY.md`](../3_LLMs_and_TOKENS/README_LLM_STATELESS_NO_MEMORY.md) · [`gradio_chatbot.md`](../4_GRADIO/gradio_chatbot.md)

---

## Why memory?

Conversational assistants feel natural when they **remember** prior turns. LLMs **do not** hold state between calls — so the app must **inject** history into the prompt (or use a chain that does this for you).

**LangChain memory** stores (and optionally **summarizes**) prior messages so later invocations include the right **context**.

Memory utilities are **modular** — you can combine them with prompts, models, and chains.

---

## Common memory types

| Type | Behavior |
|------|----------|
| **ConversationBufferMemory** | Keeps the **full** conversation history (most common in intro material). |
| **ConversationSummaryMemory** | Summarizes older turns to save tokens. |
| **Buffer window** | Keeps only the last *k* messages. |

Full list: [Memory types](https://python.langchain.com/docs/concepts/memory/) in LangChain docs.

---

## ConversationChain

**ConversationChain** is a chain **designed for chat**: it wires an LLM, a prompt that includes **history**, and memory (often `ConversationBufferMemory`).

---

## Example — `ConversationBufferMemory`

```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI  # or your Bedrock chat model

llm = ChatOpenAI(model="gpt-4o-mini")

memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True,
)

# Turn 1 — mention a city
conversation.predict(input="I am planning a trip to Los Angeles next month.")

# Turn 2 — ask without naming the city; model should use history
conversation.predict(input="What is the weather usually like there in that season?")
```

**Exercise (from course):** Ask a follow-up **without** saying “Los Angeles” and check whether the answer refers to the city from turn 1.

---

## Memory vs RAG memory

| | **Chat memory** | **RAG / vector store** |
|---|-----------------|-------------------------|
| Stores | Dialogue turns | Document chunks |
| Purpose | Same session context | External knowledge |

Both can appear in one app.
