# What is FAISS?

**FAISS** (Facebook AI Similarity Search) — chapter notes for **Souvik’s** AI learning journey (folder `22_ADVANCED_RAG_HYBRID_SEARCH_RE-RANK_FAISS`).

**FAISS** is an open-source library developed by **Meta AI**. It is used in AI applications to perform **fast similarity searches** across large collections of **vector embeddings**.

In simple terms, FAISS helps an AI application **find information that is semantically similar** to a user’s question.

Related earlier chapters:

- RAG intro — [`1_introduction_to_rag.md`](../12_RAG_Retrieval_Augmented_Generation/1_introduction_to_rag.md)
- Embeddings — [`3_lm_types_and_embeddings.md`](../12_RAG_Retrieval_Augmented_Generation/3_lm_types_and_embeddings.md) · [`text_embedding_3_small.md`](../12_RAG_Retrieval_Augmented_Generation/text_embedding_3_small.md)
- Cosine similarity — [`cosine_similarity.md`](../12_RAG_Retrieval_Augmented_Generation/cosine_similarity.md)
- Vector store — [`6_vector_store.md`](../12_RAG_Retrieval_Augmented_Generation/6_vector_store.md)
- Semantic memory (embeddings + search) — [`1_introduction_to_memory_engineering.md`](../21_MEMORY_ENGINEERING/1_introduction_to_memory_engineering.md)

Source conversation (reference): [ChatGPT share](https://chatgpt.com/s/t_6af87dae75708191b40e338f389bd076)

---

## Index

| # | Topic |
|---|--------|
| 1 | [Why do we need FAISS in AI?](#1-why-do-we-need-faiss-in-ai) |
| 2 | [How FAISS works in RAG](#2-how-faiss-works-in-rag) |
| 3 | [Simple Python example](#3-simple-python-example) |
| 4 | [FAISS vs other vector databases](#4-faiss-vs-other-vector-databases) |
| 5 | [Where FAISS fits in your AI learning journey](#5-where-faiss-fits-in-your-ai-learning-journey) |
| 6 | [Suggested project](#6-suggested-project) |

---

## 1. Why do we need FAISS in AI?

Imagine you have **100,000 documents**.

A user asks:

> “How do I configure an OpenShift cluster?”

Your AI application needs to:

1. Convert the question into a **vector** (numerical representation).
2. Search for **similar document vectors**.
3. Retrieve the most **relevant documents**.
4. Send those documents to an **LLM**.
5. Generate an answer.

**FAISS helps with step 2** — fast nearest-neighbor search over embeddings.

Without a vector index like FAISS (or another vector DB), comparing the query to every document embedding one-by-one becomes too slow as the corpus grows.

---

## 2. How FAISS works in RAG

| Component | Responsibility |
|-----------|----------------|
| **Documents** | Your knowledge source |
| **Chunking** | Split documents into smaller pieces |
| **Embedding model** | Convert text into vectors |
| **FAISS** | Find similar vectors |
| **LLM** | Generate the final answer |

FAISS is commonly used as the **vector search component** in a **RAG** pipeline.

**Layman:** embeddings turn text into points in space; FAISS is the **fast map** that finds the nearest points to your question; the LLM reads those nearby chunks and writes the answer.

---

## 3. Simple Python example

### Install

```bash
pip install faiss-cpu numpy
```

For **Part 2** you also need `openai`, `python-dotenv`, and `OPENAI_API_KEY` in `.env` — same as [`HYBRID_PROJECT/main.py`](./HYBRID_PROJECT/main.py). Part 2 embeds the strings in the `DOCS` list in [`faiss_demo.py`](./faiss_demo.py) (no import from the project folders).

### Hands-on script

[`faiss_demo.py`](./faiss_demo.py) (chapter folder, not inside `HYBRID_PROJECT/` / `RE_RANK_PROJECT/`) runs two parts in one file.  
Line-by-line notes (including **`np.array`** and **why the toy numbers**): [`faiss_demo.md`](./faiss_demo.md).

| Part | What it does |
|------|----------------|
| **1 — toy** | Three 3-D vectors, `IndexFlatL2`, search with no API |
| **2 — OpenAI** | Four sentences → `text-embedding-3-small` → FAISS → top-2 matches for a RAG-style question |

### What the FAISS calls mean

| Call | Meaning |
|------|---------|
| `IndexFlatL2(dim)` | Exact search using **L2 (Euclidean) distance** — simple and good for learning |
| `index.add(vectors)` | Store a matrix of shape `(n_vectors, dim)` as `float32` |
| `index.search(query, k)` | Return **k** nearest row indices + distances |

Chroma and many vector DBs use similar math under the hood; FAISS exposes the index API directly.

### How to run

```bash
python faiss_demo.py
```

Run from this chapter folder (`22_ADVANCED_RAG_HYBRID_SEARCH_RE-RANK_FAISS/`), not from `HYBRID_PROJECT/` / `RE_RANK_PROJECT/`.

---

## 4. FAISS vs other vector databases

| Technology | What it does |
|------------|--------------|
| **FAISS** | High-performance vector similarity search (library; you often manage storage yourself) |
| **ChromaDB** | Vector database, convenient for RAG |
| **Pinecone** | Managed cloud vector database |
| **Milvus** | Distributed vector database |
| **Qdrant** | Vector database with filtering capabilities |

**Interview one-liner:** FAISS is a **similarity-search library**; Chroma/Pinecone/Milvus/Qdrant are fuller **vector databases** (persistence, APIs, filters, ops). Many RAG tutorials start with FAISS because it is fast and local.

---

## 5. Where FAISS fits in your AI learning journey

Given work with Python, SQLite, LLMs, MCP, and AI agents, a sensible sequence:

| Step | Topic | Goal |
|------|--------|------|
| 1 | **Embeddings** | Understand how text becomes numerical vectors |
| 2 | **Vector similarity** | Cosine similarity and Euclidean distance |
| 3 | **FAISS** | Build an index and run similarity searches |
| 4 | **RAG** | Connect FAISS with an LLM to answer from documents |
| 5 | **AI agents** | Give an agent access to your RAG knowledge base |

You already covered much of steps 1–2 and basic RAG in folder `12_RAG_Retrieval_Augmented_Generation`. This chapter deepens **FAISS** and later topics named in this folder (hybrid search, re-ranking).

---

## 6. Suggested project

**Hands-on in this chapter:** [`HYBRID_PROJECT/`](./HYBRID_PROJECT/) (hybrid) then [`RE_RANK_PROJECT/`](./RE_RANK_PROJECT/) (LLM re-rank). Note 1’s FAISS snippet is the minimal index; those projects use **Chroma** for the same retrieval stage at production-like scale.

**Stretch idea — OpenShift Documentation RAG**

1. Feed it **OpenShift documentation**.
2. Ask questions.
3. Use **FAISS** or **Chroma** for retrieval.
4. Use an **LLM** for answering.

---

## Interview one-liner

**FAISS** is Meta’s open-source library for **fast nearest-neighbor search over embeddings** — the usual “find similar chunks” engine inside many local RAG demos.
