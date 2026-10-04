# RAG architecture and workflow

Chapter notes (folder `12_RAG_Retrieval_Augmented_Generation`).

**Read order:** `2` of `8` — start with [`1_introduction_to_rag.md`](./1_introduction_to_rag.md).

Embeddings background (note **3**): [`3_lm_types_and_embeddings.md`](./3_lm_types_and_embeddings.md)

---

## Index


| #   | Topic                                                                                |
| --- | ------------------------------------------------------------------------------------ |
| 1   | [Key idea vs “FM only”](#1-key-idea-vs-fm-only)                                      |
| 2   | [Phase A — Data ingestion](#2-phase-a--data-ingestion)                               |
| 3   | [Phase B — Retrieve relevant information](#3-phase-b--retrieve-relevant-information) |
| 4   | [Phase C — Augment the prompt](#4-phase-c--augment-the-prompt)                       |
| 5   | [Phase D — Generation](#5-phase-d--generation)                                       |
| 6   | [End-to-end diagram](#6-end-to-end-diagram)                                          |
| 7   | [RAG workflow (numbered steps)](#7-rag-workflow-numbered-steps)                      |
| 8   | [Autoencoder vs autoregressive (and encoder–decoder)](#8-autoencoder-vs-autoregressive-and-encoderdecoder) |


---



## 1. Key idea vs “FM only”

**Without RAG:** user query → **foundation model (FM)** → answer (only what the FM learned in training).

**With RAG:** user query → **retrieve** from external store → **combine** query + retrieved text → FM → answer.

The FM is the same **generator** (usually a chat **LLM** — see [`1_introduction_to_rag.md`](./1_introduction_to_rag.md) §1); RAG adds a **knowledge path** you control.

---



## 2. Phase A — Data ingestion

External data goes beyond the FM’s original training set. Sources can include:

- APIs  
- Databases  
- Document repositories (PDF, HTML, SharePoint, S3, …)

Formats vary: files, records, long text.

### Steps

1. **Load** raw content from sources.
2. **Chunk** — split documents into smaller segments (manageable for embedding and for context limits).
3. **Embed** — an **embeddings model** (often an autoencoding-style encoder) turns each chunk into a **vector** (numeric representation of meaning).
4. **Store** vectors (+ original text + metadata) in a **vector database**.

```text
Sources (APIs, DB, files)
        │
        ▼
   Chunk documents
        │
        ▼
   Embeddings model  →  vectors
        │
        ▼
   Vector database
```

**Practical check:** confirm the **embedding model supports the languages** in your corpus before production ingest.

---



## 3. Phase B — Retrieve relevant information

After ingest, each user question triggers a **relevance search**:

1. Embed the **user query** with the **same** embeddings model used at ingest.
2. Run **semantic search** in the vector DB (distance / similarity in vector space).
3. Return the **top-k** chunks whose vectors are closest to the query vector.

**Example:** HR assistant — *“What are my healthcare benefits?”*  
Retriever should surface **benefit plan documents** and (if indexed) **that employee’s enrollment** metadata — not unrelated policies.

Relevance is **mathematical** (vector similarity), not simple keyword match — though many systems add **hybrid** keyword + vector search.

---



## 4. Phase C — Augment the prompt

Retrieved passages are **inserted into the prompt** as **context**, together with the user’s question.

This step is **prompt engineering**:

- Instruct the FM to use context faithfully (“answer from context only”).  
- Structure: system rules + `Context:` block + `Question:` (or chat turns).

Output: an **augmented / expanded prompt** ready for the generator.

---



## 5. Phase D — Generation

The augmented prompt is sent to the **foundation model** (autoregressive LM — GPT, Claude, etc.).

The model **generates** the final natural-language answer, ideally grounded in retrieved text.

---



## 6. End-to-end diagram

RAG is really **two pipelines**: one you run **ahead of time** (build the library) and one you run **every time someone asks a question** (use the library). The diagram below shows both.

```text
┌─────────────────────────────────────────────────────────┐
│                    OFFLINE / BATCH                       │
│  External data → chunk → embed → vector store            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    ONLINE (per query)                    │
│                                                          │
│  User query ──► embed query ──► vector search ──► chunks │
│                                      │                   │
│                                      ▼                   │
│              augment prompt (context + question)         │
│                                      │                   │
│                                      ▼                   │
│              Foundation model ──► answer               │
└─────────────────────────────────────────────────────────┘
```

### Top box — OFFLINE / BATCH (ingestion)

This is **Phase A** ([§2](#2-phase-a--data-ingestion)). It does **not** run when the user types a question (except when you **refresh** the index).

| Step in the box | What happens |
|-----------------|--------------|
| **External data** | PDFs, wikis, DB exports, API snapshots — your company knowledge. |
| **Chunk** | Long docs are cut into smaller pieces so each piece fits embedding + context limits. |
| **Embed** | Each chunk becomes a vector (list of numbers = “meaning coordinates”). |
| **Vector store** | Vectors + original text (+ metadata) are saved in a **vector database** (Chroma, Pinecone, pgvector, etc.). |

**Layman:** you **index** your handbook once (or on a schedule). Users do not wait for full PDF parsing on every chat message.

**When it runs again:** new policies, new products, fixed typos — you **re-ingest** or update affected chunks so search stays current.

### Bottom box — ONLINE (per query)

This runs **on every user question** — **Phases B, C, D** ([§3](#3-phase-b--retrieve-relevant-information)–[§5](#5-phase-d--generation)).

| Step in the box | What happens |
|-----------------|--------------|
| **User query** | Plain text question, e.g. *“What is our PTO policy?”* |
| **Embed query** | Same embedding model as ingest turns the question into a vector **in the same space** as your chunks. |
| **Vector search** | DB finds chunks whose vectors are **closest** to the question vector (semantic “nearest neighbors”). |
| **Chunks** | You get back **top-k** text snippets (e.g. 3–10 passages), not the whole corpus. |
| **Augment prompt** | Those snippets are pasted into the prompt as **context**, plus instructions and the user question. |
| **Foundation model** | The chat LLM reads context + question and **writes** the final answer in natural language. |

**Layman:** user asks → system **looks up** the right pages → **hands those pages to the FM** → FM **summarizes / answers** in its own words.

### How the two boxes connect

```text
  OFFLINE                          ONLINE
  ───────                          ──────

  Your docs  ──► vector store ◄───  "search here"
                      │
                      └── stored text of each chunk
                              │
                              └──► copied into prompt as Context
```

The vector store is the **bridge**: offline work **fills** it; online work **queries** it. The FM never “browses” your SharePoint directly — it only sees **whatever text retrieval put in the prompt** for that request.

### Timing and cost (intuition)

| Part | Typical cost pattern |
|------|----------------------|
| **Offline** | Heavier up front (embed millions of tokens once); cheap per chat afterward if index is stable. |
| **Online** | Pay per query: embed one question + FM tokens for context + answer. Bigger **k** or huge chunks → slower and pricier. |

### One-line summary

**Offline:** build the searchable index. **Online:** **Retrieve** chunks → **Augment** the prompt → **Generate** the answer.

---



## 7. RAG workflow (numbered steps)

At query time, in order:

1. User submits a **question**.
2. Question is converted to a **vector** (same embedding space as the index).
3. **Vector database** is queried for vectors **close** to the question vector.
4. **Original text** for those vectors is retrieved.
5. Retrieved text is **inserted into the LLM prompt** as context.
6. The **LLM generates** a response using that extra context.

Steps 1–4 = **retrieval**; 5 = **augmentation**; 6 = **generation**.

---

## 8. Autoencoder vs autoregressive (and encoder–decoder)

Two fundamental ways neural networks / transformers are trained — they show up everywhere when you learn LLM architecture and **RAG** (embed with encoder-style models, answer with autoregressive chat models).

### 8.1 Autoencoder

An **autoencoder** learns to **compress information and then reconstruct it**.

```text
Input
  ↓
Encoder
  ↓
Compressed representation
  ↓
Decoder
  ↓
Reconstructed input
```

Example:

```text
"I love machine learning"
          ↓
       Encoder
          ↓
     [latent vector]
          ↓
       Decoder
          ↓
"I love machine learning"
```

The model learns:

> **What information do I need to retain to reconstruct this?**

A famous NLP example is **BERT**, which uses **masked language modeling** (related to the autoencoding idea). For example:

```text
The cat [MASK] on the mat.
```

The model learns to predict:

```text
sat
```

BERT is **encoder-only**.

Typical uses:

- Understanding text  
- Classification  
- Embeddings  
- Semantic search  
- Sentiment analysis  

In **RAG**, embedding models used at ingest/query time are often this family (represent meaning as vectors).

### 8.2 Autoregressive model

An **autoregressive** model generates the sequence **one token at a time**, using previous tokens to predict the next.

```text
The
 ↓
The cat
 ↓
The cat is
 ↓
The cat is sitting
 ↓
The cat is sitting on
 ...
```

Mathematically:

**P(x₁, x₂, …, xₙ) = Π P(xᵢ | x₁, …, xᵢ₋₁)**

In simple words:

> **Predict the next token based on everything generated so far.**

This is the basic idea behind **GPT-style LLMs**.

```text
Prompt:
"The capital of France is"

             ↓

          GPT
             ↓
           "Paris"
```

Then the model can use `Paris` as part of the context to generate the next token.

In **RAG**, the **generator** in Phase D is usually autoregressive (GPT, Claude, Gemini, etc.) — it writes the final answer after context is in the prompt.

### 8.3 Easiest way to remember

| | Autoencoder / encoder | Autoregressive |
|---|------------------------|----------------|
| Main idea | **Understand / represent** | **Generate** |
| Direction | Input → representation | Previous tokens → next token |
| Example | **BERT** | **GPT** |
| Typical architecture | Encoder-only | Decoder-only |
| Great for | Embeddings, classification | Text generation |
| Generation | Not its primary purpose | **Core purpose** |

### 8.4 Third category — encoder–decoder

```text
Input
 ↓
Encoder
 ↓
Representation
 ↓
Decoder
 ↓
Output
```

Examples: **T5**, the original **Transformer** paper architecture.

Especially useful when you **transform one sequence into another**, e.g. translation:

```text
English → Encoder → Decoder → French
```

### 8.5 Mental model (three boxes)

| Style | One line |
|-------|----------|
| **Encoder-only** | Understand |
| **Decoder-only / autoregressive** | Generate |
| **Encoder–decoder** | Transform one sequence into another |

Useful shorthand: **BERT vs GPT vs T5**.

More on embeddings and which model plays which RAG role: [`3_lm_types_and_embeddings.md`](./3_lm_types_and_embeddings.md).