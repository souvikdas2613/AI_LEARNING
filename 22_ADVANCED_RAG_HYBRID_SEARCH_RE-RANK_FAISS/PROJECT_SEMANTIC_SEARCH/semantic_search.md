# Semantic search lab — one file

Folder **`PROJECT_SEMANTIC_SEARCH`** — retrieve by **meaning** (OpenAI embeddings + cosine similarity).

| File | Role |
|------|------|
| [`semantic_search.py`](./semantic_search.py) | **Run this** — embed docs, cosine score, debug + top-**3** ranks |

**Knowledge files (shared):** [`../documents/`](../documents/) — one **whole file** per topic (no chunking yet):

| File | Topic |
|------|--------|
| `kubernetes.txt` | K8s / kubectl / Pods |
| `python.txt` | Python basics |
| `cpp.txt` | C++ basics |

Chunking comes later in [`../HYBRID_PROJECT/`](../HYBRID_PROJECT/).

**Hybrid (Chroma + blend):** [`../HYBRID_PROJECT/hybrid_project_flow.md`](../HYBRID_PROJECT/hybrid_project_flow.md)

---

## Why it is needed (utility)

Keyword search only sees **shared words**. RAG still has to find useful context when users **paraphrase**, ask in natural language, or use words that never appear in the doc. **Semantic search** is that second leg — and it is what vector DBs and FAISS index in production.

| Why use it | Plain meaning |
|------------|----------------|
| **Meaning, not spelling** | “How do I define a function in Python?” can rank `python.txt` high even without copying exact sentences from the file. |
| **Same stack as real RAG** | Embed chunks → store vectors → embed query → nearest neighbors. This lab does the same flow in memory (no Chroma/FAISS yet). |
| **Hybrid RAG** | [`../HYBRID_PROJECT/hybrid_project_flow.md`](../HYBRID_PROJECT/hybrid_project_flow.md) blends **~0.7 semantic + ~0.3 keyword**. This folder isolates the **semantic half**. |
| **Teaches cosine + embeddings** | Same primitives as [`faiss_demo.py`](../faiss_demo.py) and topic **12** / **21** — only the index backend differs here (loop + numpy, not FAISS). |

**Utility of *this* script:** offline-readable twin of the keyword lab — same three [`../documents/`](../documents/) files, same `DEMO_QUERIES`, so you can **compare** scores side by side.

**Keyword lab:** [`../PROJECT_KEYWORD_SEARCH/keyword_search.md`](../PROJECT_KEYWORD_SEARCH/keyword_search.md)

---

## Why embeddings? (what they do)

A language model **embedding** turns a string into a long list of numbers (a **vector**) such that texts with **similar meaning** end up with vectors that point in **similar directions** in high-dimensional space.

| Without embedding | With embedding |
|-------------------|----------------|
| Compare word lists | Compare **1536-D vectors** from `text-embedding-3-small` |
| `raii` must match `raii:` exactly | “What is RAII?” can sit near a paragraph that **explains** RAII |
| Synonyms and paraphrases often score **0** | “list pods” can align with a doc that says `kubectl get pods` |

**In this file:**

```text
doc text  →  create_embedding()  →  vector stored in index["embedding"]
question  →  create_embedding()  →  query vector
score     →  cosine_similarity(query, doc)   # how aligned are the directions?
```

Embeddings cost **API calls** and are **opaque** (hard to explain per dimension), but they encode **context** that token overlap misses.

More depth: [`text_embedding_3_small.md`](../../12_RAG_Retrieval_Augmented_Generation/text_embedding_3_small.md) · cosine: [`cosine_similarity.md`](../../12_RAG_Retrieval_Augmented_Generation/cosine_similarity.md)

---

## Is it accurate?

**Depends what you mean by accurate.**

| Question | Answer for this lab |
|----------|---------------------|
| **Does cosine math match the formula?** | **Yes.** `dot(q,d) / (norm(q)*norm(d))` in `cosine_similarity()`. |
| **Does top-1 usually match the right topic file?** | **Often yes** on the three demo queries — see [Sample run output](#sample-run-output-ranked-summary) and contrast with the [RAII keyword tie](../PROJECT_KEYWORD_SEARCH/keyword_search.md#worked-example--what-is-raii-in-c-insights). |
| **Is it always “correct” for the user?** | **No.** Whole-file embedding **averages** all topics in one vector; chunking in [`../HYBRID_PROJECT/`](../HYBRID_PROJECT/) behaves differently. Wrong model, stale index, or ambiguous queries still give bad hits. |
| **Same as production search quality?** | **Teaching scope only** — no reranker, no hybrid keyword, no BM25, in-memory brute force (not FAISS at scale). |

**Short verdict:** **stronger relevance signal than naive keyword overlap** for paraphrased questions; **not perfect** — use hybrid + chunking + optional rerank in the full project.

**Contrast (same query):** *What is RAII in C++?*

| Method | Top result | Issue or win |
|--------|------------|----------------|
| Keyword | `cpp.txt` and `python.txt` tied **0.4** | Generic words `is`, `in`; `raii` ≠ `raii:` |
| **Semantic (this lab)** | **`cpp.txt` score ~0.40**, others ~0.11–0.12 | **Separates** the C++ file as #1 |

---

## What it does (one sentence)

Turn each doc into a **vector**, turn the **question** into a vector, pick the docs whose vectors point **most like** the question — even when words differ.

---

## Formula used

### Step 1 — embedding (OpenAI)

Each text → vector in \(\mathbb{R}^{1536}\) via **`text-embedding-3-small`**.

```text
embedding = API(text)   →   [0.02, -0.11, ...]   # length 1536
```

### Step 2 — cosine similarity (semantic score)

For query vector \(\mathbf{q}\) and document vector \(\mathbf{d}\):

```text
semantic_score = (q · d) / (||q|| × ||d||)
```

| Score (typical range here) | Meaning |
|----------------------------|---------|
| **Higher** | More aligned meaning (not necessarily 1.0 on real text) |
| **~0.1–0.2** | Weak / mostly unrelated whole-file match |
| **~0.4–0.6** | Stronger match for this small corpus |

Sort **descending**, return **top-k**. Default in `semantic_search()` is `top_k=3`; `main()` passes **`top_k=3`** for the final ranked lines.

---

## Functions — main job

| Function | Job |
|----------|------|
| `create_embedding(text)` | One string → one vector (OpenAI). |
| `cosine_similarity(v1, v2)` | One float: alignment of two vectors. |
| `load_documents()` | Read every `*.txt` from [`../documents/`](../documents/). |
| `build_index(docs)` | Embed **each whole file**; store `embedding` on each record; **debug prints** (id, source, full text). |
| `semantic_search(query, index, top_k)` | Embed query, score rows, **debug Results block**, return `results[:top_k]`. |
| `preview(text)` | Short one-line snippet for final rank print in `main()`. |
| `main()` | Requires `OPENAI_API_KEY`; load → build index → three demo queries. |

---

## Line-by-line — [`semantic_search.py`](./semantic_search.py)

Your edits mirror the keyword lab: **verbose index build**, **`BEGINNING SEARCH`**, **`top_k=3`**, and a **Results** dump inside `semantic_search` before the compact rank lines in `main()`.

### Imports and config (lines 1–20)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 1–6 | `os`, `Path`, `numpy`, `dotenv`, `OpenAI` | API client + math for cosine. |
| 8–9 | `load_dotenv(...parents[2]...)` + `load_dotenv()` | Loads `AI_LEARNING/AI_LEARNING/.env` then local `.env`. |
| 11–12 | `client`, `EMBEDDING_MODEL` | **`text-embedding-3-small`**. |
| 14 | `DOCUMENTS_DIR` | `../documents/` (parent of this folder). |
| 16–20 | `DEMO_QUERIES` | Same three questions as keyword lab. |

### `load_documents()` (23–31)

Same pattern as keyword lab: sorted `*.txt` → `doc_id`, `source`, full `text`. **No** print here (prints happen in `main()`).

### `create_embedding` / `cosine_similarity` (41–49)

| Function | Role |
|----------|------|
| `create_embedding` | `client.embeddings.create` → `response.data[0].embedding` (list of floats). |
| `cosine_similarity` | NumPy dot product divided by product of L2 norms → value in **[-1, 1]**, usually positive for related text. |

### `build_index(docs)` (52–68)

| Line(s) | What happens |
|---------|----------------|
| 55 | `embedding = create_embedding(doc["text"])` — **one API call per whole file**. |
| 56–61 | `record` dict with keys: `doc_id`, `source`, `text`, **`embedding`**. |
| 62 | Append to `indexed` list (in-memory “index”). |
| 63–68 | Debug: `Indexed`, id, source, **`embedding dim: {len(embedding)}`** (1536 for `text-embedding-3-small`), then **full text**. Full vector is **not** printed — avoids 1536 numbers × 3 files. |

### `semantic_search` (71–89)

| Step | What happens |
|------|----------------|
| 72–73 | Embed the **query** (another API call per question); prints **`Query embedding dim: …`**. |
| 74–81 | Cosine score vs each row’s `embedding`. |
| 82 | Sort by `semantic_score` descending. |
| 83–88 | **Debug** — every file, full text, raw score. |
| 89 | Return only first **`top_k`** dicts to `main()`. |

### `main()` (92–123)

| Step | What happens |
|------|----------------|
| 93–94 | Exit if no API key. |
| 96–104 | Load docs; list sources. |
| 106–110 | `build_index` — slowest phase (3 embeddings). |
| 112–118 | Per query: `semantic_search(..., top_k=3)` then **clean** lines: rank, 4-decimal score, `preview(text)`. |

### Console flow

```text
Loaded N documents + file list
Building index...  →  Indexed blocks (full text each)
Index built with N documents
BEGINNING SEARCH...

Per query:
  Query: ...
  Results: (all docs, full text, score)   ← debug
  1. score=.... source: preview...        ← summary
  2. ...
  3. ...
```

---

## Sample run output (ranked summary)

Captured from a real run of `python semantic_search.py` (scores vary slightly if the API returns tiny embedding drift).

### Startup (short)

```text
Loaded 3 documents
Semantic search — embedding 3 whole files (no chunking).
  - cpp.txt
  - kubernetes.txt
  - python.txt

Building index...
Indexed:
 cpp.txt
  ...
Indexed:
 kubernetes.txt
  ...
Indexed:
 python.txt
  ...

Index built with 3 documents
BEGINNING SEARCH...
```

(Index build also prints **full file text** for each doc — omitted here for length.)

### Query 1

```text
Query: How do I list pods with kubectl?

  1. score=0.5663 kubernetes.txt: Kubernetes (K8s) runs containerized applications across a cluster of machines. A Pod is the small...
  2. score=0.1253 python.txt: Python is a high-level language known for readable syntax and a large standard library. Common ty...
  3. score=0.1002 cpp.txt: C++ is a compiled systems language used for performance-critical software. Source files are often...
```

**Read:** `kubernetes.txt` clearly wins — question matches cluster / kubectl / pods **by meaning**, not only token overlap.

### Query 2

```text
Query: How do I define a function in Python?

  1. score=0.4387 python.txt: Python is a high-level language known for readable syntax and a large standard library. Common ty...
  2. score=0.1436 cpp.txt: C++ is a compiled systems language used for performance-critical software. Source files are often...
  3. score=0.0860 kubernetes.txt: Kubernetes (K8s) runs containerized applications across a cluster of machines. A Pod is the small...
```

### Query 3 (compare to keyword lab)

```text
Query: What is RAII in C++?

  1. score=0.4025 cpp.txt: C++ is a compiled systems language used for performance-critical software. Source files are often...
  2. score=0.1229 kubernetes.txt: Kubernetes (K8s) runs containerized applications across a cluster of machines. A Pod is the small...
  3. score=0.1125 python.txt: Python is a high-level language known for readable syntax and a large standard library. Common ty...
```

Keyword lab tied **cpp** and **python** at **0.4** on this query; semantic search puts **`cpp.txt` first** with a much larger gap to the others — that is the pedagogical payoff of embeddings.

---

## How to run

```bash
pip install openai python-dotenv numpy
python semantic_search.py
```

`.env` (e.g. `AI_LEARNING/AI_LEARNING/.env`):

```env
OPENAI_API_KEY=your_key_here
```

---

## Compare with keyword lab

Same files and demo queries as [`keyword_search.py`](../PROJECT_KEYWORD_SEARCH/keyword_search.py).

```bash
# folder PROJECT_KEYWORD_SEARCH
python keyword_search.py

# folder PROJECT_SEMANTIC_SEARCH
python semantic_search.py
```

| | Keyword | Semantic (this lab) |
|---|---------|---------------------|
| Cost | Free, offline | OpenAI embedding calls |
| Match rule | Token intersection | Vector direction |
| RAII query | cpp **tied** with python | **cpp** ranked #1 |
| Exact error code / SKU | Often good | May miss if wording differs |

Full pipeline: **`0.7 × semantic + 0.3 × keyword`** in [`../HYBRID_PROJECT/`](../HYBRID_PROJECT/).

---

## Interview one-liner

**Semantic search** = embed query and docs, rank by **cosine similarity** — finds relevant text by **meaning**, not spelling; pair with keyword search for production **hybrid** RAG.