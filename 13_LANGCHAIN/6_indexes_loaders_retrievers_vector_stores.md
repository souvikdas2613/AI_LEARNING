# Structuring documents with indexes

Note **6** of **10** — folder `13_LANGCHAIN`.

**Previous:** [`5_prompt_templates.md`](./5_prompt_templates.md) · **Next:** [`7_memory.md`](./7_memory.md)

Related: [`2_rag_architecture_and_workflow.md`](../12_RAG_Retrieval_Augmented_Generation/2_rag_architecture_and_workflow.md) · [`10_embeddings_and_vector_store.md`](./10_embeddings_and_vector_store.md) · **Practice:** [`rag_langchain_chunks_vector_db_visualization.ipynb`](./rag_langchain_chunks_vector_db_visualization.ipynb) → [`rag_langchain_retriever_qa_gradio.ipynb`](./rag_langchain_retriever_qa_gradio.ipynb)

---

## Document loaders

For **RAG**, you must **load** documents from sources the LLM can index and retrieve later.

**Document loaders** in LangChain read from:

- local files and folders,
- databases,
- web URLs,
- cloud object storage (e.g. **Amazon S3**),
- and many other integrations.

Each loader typically yields **`Document`** objects (page content + metadata).

### Example — load from S3 (`S3FileLoader`)

```python
from langchain_community.document_loaders import S3FileLoader

loader = S3FileLoader(
    bucket="my-docs-bucket",
    key="policies/handbook.pdf",
)

documents = loader.load()
# Next steps (not shown here): split → embed → store in vector DB
```

---

## Retriever

A **retriever** fetches **relevant documents** for a user query.

Flow:

1. User submits a query.
2. Retriever searches the **index** (often vector similarity).
3. Top-k chunks go to the app for **augmentation** (added to the prompt).

Retrievers are usually built **from** a vector store: `vectorstore.as_retriever()`.

### `as_retriever()` — what it is

`as_retriever()` is a LangChain helper that turns a **vector store** into a **Retriever** — an object whose job is: **given a question string, return relevant `Document` chunks** (not an LLM answer).

#### What you have before

```python
vectorstore = Chroma(persist_directory=db_name, embedding_function=embeddings)
```

`vectorstore` knows how to:

- store vectors + text in Chroma
- run **similarity search** (embed the query, find nearest chunk vectors)

That API is “database-ish”: you often call things like `similarity_search("Who is Avery?", k=4)`.

#### What `as_retriever()` does

```python
retriever = vectorstore.as_retriever()
```

It wraps the same store in the **Retriever** interface LangChain uses everywhere in RAG:

- one main method: **`retriever.invoke(question)`** (or `.get_relevant_documents(question)` in older code)
- returns a **list of `Document`** objects (`page_content` + `metadata`)

Example:

```python
docs = retriever.invoke(question)
```

Means: embed `question` → Chroma top‑k similar chunks → those chunks as `Document`s.

#### Why not call Chroma directly?

1. **Same shape as other retrievers** — keyword, hybrid, multi-query, etc. all implement “question → docs”. Chains and tools expect that.
2. **Composable** — swap `vectorstore.as_retriever()` for `vectorstore.as_retriever(search_kwargs={"k": 8})` or a different retriever without rewriting most of your Q&A logic.
3. **Fits LangChain RAG patterns** — retriever → stuff context into prompt → LLM.

#### Default behavior

`as_retriever()` with no arguments typically uses something like **`k=4`**: four chunks per question. You can change it:

```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
```

Other `search_kwargs` depend on the vector store (e.g. score threshold, metadata filters).

#### Mental model

| Object | Role |
|--------|------|
| `OpenAIEmbeddings` | text → vector (for queries and, at index time, for chunks) |
| `Chroma` / `vectorstore` | **store** vectors and run similarity search |
| `retriever` | **thin adapter**: “user question” → “best matching documents” |
| `ChatOpenAI` | reads those docs in the prompt and **writes** the answer |

```text
question
   → retriever.invoke(question)     # retrieval only
   → [Document, Document, ...]
   → join page_content → context
   → LLM with system + human messages
   → answer string
```

`retriever.invoke(question)` is the **R** in RAG. Without it you’d only have `llm.invoke(question)` — no guaranteed grounding in your knowledge base.

### `retriever.invoke` vs `llm.invoke`

Both objects expose **`invoke()`**, but they do **totally different jobs**. Same method name, different meaning.

| | `retriever.invoke("Who is Avery?")` | `llm.invoke("Who is Avery?")` |
|--|------------------------------------|-------------------------------|
| **What it does** | **Search** your vector store | **Generate** text with a chat model |
| **Talks to** | Chroma (+ embedding API for the query) | OpenAI chat API (`ChatOpenAI`) |
| **Uses your knowledge base?** | **Yes** — finds chunks in `vector_db/` | **No** — only the model’s training knowledge |
| **Returns** | `list[Document]` (chunk text + metadata) | `AIMessage` (natural-language answer) |
| **Writes a final answer?** | No — only returns source text | Yes — but may be wrong / generic for InsureLLM |
| **RAG role** | **R**etrieval | **G**eneration (when given context) |

#### Side by side

```python
# Retrieval only — no prose answer
docs = retriever.invoke("Who is Avery?")
# → [Document(... Avery Lancaster ...), Document(...), ...]

# Generation only — no company docs
msg = llm.invoke("Who is Avery?")
# → AIMessage(content="Avery is a given name...")  # generic, not your CEO file
```

#### Full RAG uses both

```text
retriever.invoke(question)  →  Documents
        ↓
join into {context}
        ↓
llm.invoke([SystemMessage(... context ...), HumanMessage(question)])
        ↓
answer grounded in your docs
```

So:

- **`retriever.invoke`** = “find me relevant passages”
- **`llm.invoke`** = “write an answer from what I give you (or from what you already know)”

Same question string, two different pipelines until you wire them together in `answer_question`.

See practice: [`rag_langchain_retriever_qa_gradio.ipynb`](./rag_langchain_retriever_qa_gradio.ipynb).

---

## Vector stores

Question-answering bots work better when the LLM sees **your** data in context.

LangChain supports:

- **Open source** stores (e.g. Chroma, FAISS, and others via community packages),
- **Managed / cloud** options — e.g. **Amazon OpenSearch Serverless** vector engine,
- **PostgreSQL** with **pgvector** on **Amazon Aurora**.

The **vector stores** component wraps insert, similarity search, and (optionally) metadata filters.

---

## How loaders, stores, and retrievers connect

```text
Document loaders  →  split/chunk  →  embeddings  →  vector store
                                                      ↓
User query  →  retriever  →  relevant docs  →  prompt  →  LLM
```
