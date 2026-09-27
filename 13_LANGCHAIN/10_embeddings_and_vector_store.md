# Embeddings and vector store (Chroma)

Note **10** of **10** — folder `13_LANGCHAIN`.

**Previous:** [`9_agents.md`](./9_agents.md) · **Related:** [`6_indexes_loaders_retrievers_vector_stores.md`](./6_indexes_loaders_retrievers_vector_stores.md) · **Practice:** [`rag_langchain_chunks_vector_db_visualization.ipynb`](./rag_langchain_chunks_vector_db_visualization.ipynb)

---

## Generate embeddings and add to vector store

After documents are **chunked**, each chunk must become a **vector** before it can live in a vector database. That step is **embedding**: turn text into numbers that preserve **semantic** similarity.

### Vector vs embedding

**Vector** and **embedding** are closely related but not exactly the same.

#### Vector

A **vector** is simply a list of numbers:

```text
[0.21, -0.45, 0.87, 0.13, ...]
```

It is a mathematical representation.

#### Embedding

An **embedding** is a **vector that represents the meaning or features of some data** — text, image, audio, and so on.

```text
"I love this movie"
        ↓
   Embedding model
        ↓
[0.21, -0.45, 0.87, 0.13, ...]
```

So:

> **Every embedding is a vector, but not every vector is an embedding.**

Think of it like:

- **Vector** = format  
- **Embedding** = meaningful representation stored in that format  

For RAG:

```text
Document
   ↓
Embedding model
   ↓
Embedding vector
   ↓
Vector database
   ↓
Similarity search
```

The **vector database stores these embedding vectors** and uses them to find semantically similar content.

### Embeddings are multi-dimensional vectors

An **embedding is a multi-dimensional vector**.

A tiny 3-dimensional embedding could look like:

```text
"I love this movie"
        ↓
[0.2, -0.7, 0.9]
```

That is a **3-dimensional vector**.

Real embedding models usually have hundreds or thousands of dimensions:

```text
Text
 ↓
Embedding model
 ↓
[0.12, -0.43, 0.87, 0.21, ..., 0.56]
 ↑____________________________↑
        768 dimensions
```

Examples of dimensionality:

- **1D:** `[5]`
- **2D:** `[5, 3]`
- **3D:** `[5, 3, 8]`
- **768D:** `[x₁, x₂, x₃, ... x₇₆₈]`

The dimensions are **not** usually human-readable labels like “happiness”, “movie”, or “English”. The model learns numerical representations across those dimensions.

When we say two embeddings are **close**, we usually mean their vectors have **high similarity** (often **cosine similarity**), which suggests the underlying content is semantically similar. That is why chunk embeddings that sit near each other in vector space get retrieved together.

### Embedding models (LangChain)

To generate embeddings from text chunks you use an **embedding model**. In many labs that model is **`mxbai-embed-large-v1`** from Hugging Face: each chunk becomes a vector with **1024 dimensions**.

In LangChain you typically wrap the model in an **embeddings** class, for example:

| Approach | Example | Notes |
|----------|---------|--------|
| OpenAI API | `OpenAIEmbeddings(model="text-embedding-3-small")` | 1536 dimensions for `text-embedding-3-small`; needs API key |
| Hugging Face (local) | `HuggingFaceEmbeddings(model_name="mixedbread-ai/mxbai-embed-large-v1")` | 1024 dimensions; needs `torch` + `sentence-transformers` |
| Other providers | Community integrations | Same pattern: embed query and documents with the **same** model |

The embedding object does **not** embed all text at construction time. It is a **client** that LangChain (or you) call when building or querying the store.

---

## Exploring embeddings

Exploration means checking that vectors behave as you expect before you rely on them in production.

Useful checks:

- **Shape** — `len(vector)` should match the model’s dimension (e.g. 1024 or 1536).
- **Similarity** — embed two related sentences vs two unrelated ones; related pairs should have **higher** cosine similarity (or lower distance, depending on the API).
- **Visualization** — high-dimensional vectors are hard to plot directly; **t-SNE** (or UMAP) projects them to 2D so you can see whether chunks from the same topic cluster together.

The notebook [`rag_langchain_chunks_vector_db_visualization.ipynb`](./rag_langchain_chunks_vector_db_visualization.ipynb) loads chunks from `knowledge-base/`, embeds them, stores them in Chroma, and optionally plots embeddings with t-SNE.

---

## Vector store

### Why a vector store is needed

An **embedding by itself is just a vector**. You need somewhere to **store, index, and search** thousands or millions of those vectors **efficiently**.

#### Simple example

Suppose you have 100,000 documents:

```text
Document 1 → embedding [0.12, -0.4, ...]
Document 2 → embedding [0.81,  0.2, ...]
Document 3 → embedding [0.15, -0.3, ...]
...
Document 100,000 → embedding [...]
```

You want to ask:

> How do I reset my OpenShift password?

Your question is also converted into an embedding:

```text
Question → [0.14, -0.35, ...]
```

Now you need to find the documents whose vectors are **most similar** to this question.

That is what a **vector store** (vector database) is designed for.

```text
                 ┌── Document 1 → Vector
Documents ───────┼── Document 2 → Vector
                 ├── Document 3 → Vector
                 └── ...
                         ↓
                  VECTOR STORE
                         ↓
                 Similarity Search
                         ↓
              Top relevant documents
                         ↓
                       LLM
                         ↓
                      Answer
```

#### Why not just use a normal database?

A traditional DB is good at:

```text
WHERE employee_id = 123
WHERE country = 'India'
WHERE age > 30
```

A vector store is good at:

> Find documents **meaningfully similar** to this question.

It uses **vector similarity search** and often **approximate nearest-neighbor (ANN)** indexing so search stays fast at large scale.

#### In RAG

| Piece | Role |
|-------|------|
| **Embedding model** | Creates vectors from text |
| **Vector store** | Stores and searches those vectors |
| **LLM** | Uses retrieved text to generate the answer |

Summary:

- **Embedding** = representation  
- **Vector** = numerical representation  
- **Vector store** = place plus indexing and search for those vectors  

That is why vector stores are central to **RAG**.

You add **embeddings** and the corresponding **document chunks** to a vector store (often in-memory for labs, or **persisted on disk** for reuse).

### Milvus vs Chroma (common lab choices)

Two common options in courses and prototypes:

| Store | Typical use |
|-------|-------------|
| **Milvus** | Large-scale, complex deployments; built for very large vector workloads |
| **Chroma** | Simple, open source, easy on a single machine; good for learning and small apps |

Both can run in-memory for fast, low-latency **similarity search** in AI applications.

### Concepts (from simple counts to modern embeddings)

- **Vectors** are numerical representations of text that capture meaning beyond raw word counts.
- **Simple vectorization** (e.g. bag-of-words) counts occurrences but misses context.
- **Word2Vec** and **BERT** introduced **contextual** embeddings (meaning depends on surrounding words).
- **OpenAI embeddings** (and other API/local models) are current practice for RAG: one model embeds both **chunks** and **user queries** so retrieval compares like with like.

---

### Chroma DB

**Chroma** is a database aimed primarily at **vectors**. Many general databases now support vector search (for example **MongoDB** with vector indexes), but Chroma is designed around storing vectors, metadata, and document text together, with tooling aimed at LLM apps.

In LangChain, the integration is commonly `langchain_chroma.Chroma`.

---

### Test Chroma DB

Typical lab flow with **OpenAI** embeddings and **persistent** storage:

```python
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

embeddings = OpenAIEmbeddings()

chroma = Chroma.from_documents(
    documents,                    # chunked Document objects
    embeddings,
    persist_directory="vector_db",  # folder name on disk — any path you choose
)
```

What each piece does:

1. **`embeddings = OpenAIEmbeddings()`** — Creates a client for OpenAI’s embedding API (model and dimensions depend on the model you configure).
2. **`Chroma.from_documents(...)`** — For each document: compute an embedding, store the vector plus `page_content` and **metadata** in Chroma.

Arguments:

| Argument | Role |
|----------|------|
| `documents` | List of chunks (or whole documents) to index |
| `embeddings` | Embedding model used for every chunk (and later for queries) |
| `persist_directory` | Directory where Chroma saves data so you do not re-embed on every run |

**Chunks vs whole documents:** The lab creates one vector **per chunk**. You can instead embed **entire documents** (fewer vectors, coarser retrieval). Try both and compare separation in similarity search or in t-SNE plots.

**Refresh an existing index** (common in notebooks):

```python
Chroma(persist_directory="vector_db", embedding_function=embeddings).delete_collection()
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory="vector_db")
```

Without deleting the old collection, you risk stale or duplicate data when chunk counts or models change.

After indexing, verify count, for example `vectorstore._collection.count()` should match `len(chunks)`.

**Retrieval flow:**

```text
User question  →  embed question (same model)  →  Chroma similarity search  →  top-k chunks  →  prompt  →  LLM
```

---

### Other vector stores (Milvus and alternatives)

The same pattern applies to other vector stores: **embed documents → insert into store → embed query → search**.

- **Milvus** — Often used when scale, sharding, and ops maturity matter; LangChain exposes Milvus via community integrations.
- **FAISS** — In-process index, no separate server; good for experiments.
- **pgvector** — Vectors inside PostgreSQL when you want one database for app data and search.

Regardless of backend, keep these rules:

1. Use the **same embedding model** for indexing and for queries.
2. Store **metadata** (source file, page, tenant) so you can filter and cite results.
3. **Chunk size** and **overlap** strongly affect retrieval quality—tune them with real questions from your users.

---

## Quick reference — lab checklist

1. Load and split documents into **chunks**.
2. Choose an **embedding model** (e.g. `mxbai-embed-large-v1` at 1024-d, or OpenAI `text-embedding-3-small` at 1536-d).
3. **Embed** each chunk and write to **Chroma** (`persist_directory`).
4. Optionally **explore** vectors (similarity checks, t-SNE).
5. Build a **retriever** from the vector store for RAG (`vectorstore.as_retriever()`).

See also the end-to-end diagram in [`6_indexes_loaders_retrievers_vector_stores.md`](./6_indexes_loaders_retrievers_vector_stores.md).
