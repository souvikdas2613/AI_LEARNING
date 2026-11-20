# `faiss_demo.py` — every step explained

Walkthrough of [`faiss_demo.py`](./faiss_demo.py) in folder `22_ADVANCED_RAG_HYBRID_SEARCH_RE-RANK_FAISS`.

Concepts: [`1_what_is_faiss.md`](./1_what_is_faiss.md) · embeddings: [`text_embedding_3_small.md`](../12_RAG_Retrieval_Augmented_Generation/text_embedding_3_small.md)

---

## What this script does (one sentence)

**Part 1** stores three hand-made 3-D vectors in FAISS and searches for neighbors with **no API**. **Part 2** embeds four strings with OpenAI, puts them in FAISS, and prints the **top-2** lines closest to a RAG-style question.

---

## Easy map — what each function is for

Think of RAG retrieval in two steps: **(A) turn text into numbers**, **(B) find the closest numbers to your question**. This file practices **(B)** with FAISS; Part 2 also does **(A)** with OpenAI.

| Name | One job (layman) | When it runs |
|------|------------------|--------------|
| **`create_embedding(text)`** | **Text → list of numbers** that capture meaning (for one sentence). | Part 2 only — for every `DOCS` line and for your question. |
| **`demo_toy_vectors()`** | **Teach FAISS with fake 3-number points** — no internet, no API. You learn `add` + `search`. | Always (Part 1). |
| **`demo_openai_faiss()`** | **Real mini-RAG retrieve** — embed `DOCS`, build index, embed question, print the **2 best matching sentences**. | Part 2 (needs `OPENAI_API_KEY`). |
| **`main()`** | **Run Part 1, then Part 2** in order. | When you `python faiss_demo.py`. |

### Inside the demos — FAISS pieces (not separate functions, but important)

| Code | One job (layman) |
|------|------------------|
| **`np.array(..., dtype="float32")`** | Pack many vectors into **one table** FAISS can read. |
| **`faiss.IndexFlatL2(dim)`** | Create an **empty filing cabinet** for vectors; `dim` = how many numbers per vector. |
| **`index.add(vectors)`** | **File away** all document vectors (one row = one chunk). |
| **`index.search(query, k=2)`** | **“Which k rows are closest to my question?”** → returns row numbers + how far. |

### Story in one flow (Part 2)

```text
You write DOCS (sentences)
    → create_embedding  (each sentence → vector)
    → np.array          (stack vectors)
    → index.add         (store in FAISS)

You ask a question
    → create_embedding  (question → vector)
    → index.search      (find nearest DOCS rows)
    → print DOCS[row]   (show the actual text)
```

**Main utility of the whole file:** show that **retrieval** in RAG is “**find the closest vectors**” — FAISS is the fast engine for that step. The LLM answer step is **not** in this file (see `HYBRID_PROJECT/main.py` / `RE_RANK_PROJECT/main.py`).

---

## How to run

```bash
pip install faiss-cpu numpy openai python-dotenv
python faiss_demo.py
```

### `.env`

| Key | Used in |
|-----|---------|
| `OPENAI_API_KEY` | Part 2 only (`OpenAI` client) |

Part 1 runs even if the key is missing.

---

## Index

| # | Topic |
|---|--------|
| 0 | [Easy map — what each function is for](#easy-map--what-each-function-is-for) |
| 1 | [`DOCS` list](#1-docs-list) |
| 2 | [`vectors = np.array(...)`](#2-vectors--nparray) |
| 3 | [Why those toy numbers in Part 1?](#3-why-those-toy-numbers-in-part-1) |
| 4 | [Part 1 — FAISS calls](#4-part-1--faiss-calls) |
| 5 | [Part 2 — real embeddings](#5-part-2--real-embeddings) |
| 6 | [Part 1 vs Part 2](#6-part-1-vs-part-2) |

---

## 1. `DOCS` list

```python
DOCS = [
    "Python is a high-level programming language.",
    ...
]
```

| Idea | Meaning |
|------|---------|
| **Plain text** | What a human reads — not vectors yet |
| **Part 1** | `DOCS` is **not used** (toy numbers only) |
| **Part 2** | Each string → `create_embedding(text)` → one row in the FAISS matrix |

**Layman:** `DOCS` is your mini knowledge base as sentences. FAISS never sees the words — only the **numbers** produced by the embedding model.

---

## 2. `vectors = np.array(...)`

FAISS `index.add()` expects a **2-D table of floats**, shape `(number_of_vectors, dimension)`, dtype **`float32`**.

### Part 1 — you write the numbers

```python
vectors = np.array(
    [
        [0.1, 0.2, 0.3],
        [0.9, 0.8, 0.7],
        [0.2, 0.3, 0.4],
    ],
    dtype="float32",
)
```

| Piece | Meaning |
|-------|---------|
| **Each inner list** | One **vector** (one point) |
| **3 rows** | **3 items** in the index |
| **3 numbers per row** | **3 dimensions** (toy only; real embeddings use 1536) |
| **`dtype="float32"`** | FAISS requires 32-bit floats |
| **Shape** | `(3, 3)` → 3 vectors × 3 dims |

### Part 2 — embeddings build the rows

```python
vectors = np.array([create_embedding(text) for text in DOCS], dtype="float32")
```

| Piece | Meaning |
|-------|---------|
| List comprehension | One API call per `DOCS` line → one Python list of ~1536 floats |
| **`np.array(...)`** | Stack those lists into a matrix |
| **Typical shape** | `(4, 1536)` — 4 docs in `DOCS` |

### Why not a plain Python list of lists?

NumPy gives a **fixed-shape numeric matrix** that FAISS can search quickly. A nested Python list is the wrong type for `index.add()`.

### Query vector uses the same idea

```python
query = np.array([[0.1, 0.2, 0.3]], dtype="float32")
```

Shape **`(1, 3)`** — batch of **one** query. FAISS always expects a batch dimension (even when you only search once).

---

## 3. Why those toy numbers in Part 1?

These values are **not magical** — they are **picked for teaching**.

```python
[0.1, 0.2, 0.3],   # row 0
[0.9, 0.8, 0.7],   # row 1
[0.2, 0.3, 0.4],   # row 2
```

The query in the script is **`[0.1, 0.2, 0.3]`** — the same as **row 0**.

| Row | Vector | Intended role |
|-----|--------|----------------|
| **0** | `[0.1, 0.2, 0.3]` | **Exact match** to the query → L2 distance **0** |
| **1** | `[0.9, 0.8, 0.7]` | **Far away** → should **not** appear in top-2 |
| **2** | `[0.2, 0.3, 0.4]` | **Close** to the query → 2nd neighbor, small distance |

### Example output

```text
query matches rows: [0 2] | L2 distances: [0.   0.03]
```

That one line is the print of `index.search(query, k=2)`. FAISS returns two arrays, and the script prints the **first query’s** slice of each (`indices[0]` and `distances[0]`). There is only one query here, so that slice is the whole answer.

Read the two arrays **in lockstep**, left to right. Position 0 is the winner; position 1 is second place. `k=2` is why you see **two** numbers, not three.

| Slot | Row id | Squared L2 | What it means |
|------|--------|------------|----------------|
| 1st (closest) | **0** | **0.** | Stored vector equals the query. Every coordinate difference is 0, so distance is 0. |
| 2nd | **2** | **0.03** | Next-nearest stored vector. Small, so it is nearby, but not identical. |
| not shown | **1** | *(would be 1.16)* | Farther than both of the above, so it loses the top-2 cutoff. |

The brackets have **spaces, not commas**, because NumPy prints an array that way (`[0 2]`), not a Python list (`[0, 2]`).

**Row ids are positions in the matrix you `add`ed**, counting from 0:

| Row you stored | Vector | Role vs query `[0.1, 0.2, 0.3]` |
|----------------|--------|----------------------------------|
| 0 | `[0.1, 0.2, 0.3]` | Same point |
| 1 | `[0.9, 0.8, 0.7]` | Other side of the toy space |
| 2 | `[0.2, 0.3, 0.4]` | Each coordinate is 0.1 higher |

**`IndexFlatL2` reports squared Euclidean distance** (sum of squared gaps), not the square root. That is why the second number is exactly `0.03`:

```text
row 0: (0.1-0.1)² + (0.2-0.2)² + (0.3-0.3)² = 0

row 2: (0.2-0.1)² + (0.3-0.2)² + (0.4-0.3)²
     = 0.01 + 0.01 + 0.01
     = 0.03

row 1: (0.9-0.1)² + (0.8-0.2)² + (0.7-0.3)²
     = 0.64 + 0.36 + 0.16
     = 1.16
```

`1.16` is much larger than `0.03`, so with `k=2` FAISS keeps rows **0** and **2** and drops row **1**.

**Smaller distance = closer.** `0.` means “this chunk *is* the query.” `0.03` means “almost the same point.” In Part 2 the same pair of arrays comes back, only the row id is used to look up `DOCS[row]` and print the sentence.

### Why only 3 dimensions?

Real `text-embedding-3-small` vectors have **1536** numbers — hard to sketch on paper. **3-D** is the smallest space where “near vs far” still feels like geometry (like x, y, z).

**One line:** Part 1 is a **toy map** — point A equals the query, point C is near A, point B is far — so FAISS output is predictable when you run the script.

---

## 4. Part 1 — FAISS calls

| Call | Meaning |
|------|---------|
| `faiss.IndexFlatL2(3)` | Index for **3-D** vectors; **exact** search using **Euclidean (L2) distance** |
| `index.add(vectors)` | Load all rows of `vectors` into the index |
| `index.search(query, k=2)` | Find **2** nearest rows to the query; return **row indices** + **distances** |

Row index `i` maps back to row `i` of the matrix you built (here, row 0 / 1 / 2 of the toy data).

---

## 5. Part 2 — real embeddings

```text
DOCS[i]  →  create_embedding  →  row i of vectors  →  index.add
user question  →  create_embedding  →  query_vec  →  index.search
```

| Step | Meaning |
|------|---------|
| Embed each `DOCS` line | Same model as the rest of your learning path: **`text-embedding-3-small`** |
| `IndexFlatL2(vectors.shape[1])` | Dimension = **1536**, read from data |
| Print `DOCS[row]` | Turn FAISS **row number** back into the **sentence** you stored |

Similar sentences should land near each other in embedding space, so a question about “vector search in RAG” tends to rank the FAISS / RAG lines highest.

---

## 6. Part 1 vs Part 2

| | Part 1 | Part 2 |
|---|--------|--------|
| Numbers | You type them | OpenAI embedding model |
| Dimensions | 3 | 1536 |
| API | None | `OPENAI_API_KEY` |
| Text in script | Ignored | `DOCS` + user question |
| Teaches | FAISS API (`add`, `search`) | Same API + real RAG-style retrieval |

Hybrid (no re-rank): [`HYBRID_PROJECT/hybrid_project_flow.md`](./HYBRID_PROJECT/hybrid_project_flow.md).  
Re-rank pipeline: [`RE_RANK_PROJECT/re_rank_project_flow.md`](./RE_RANK_PROJECT/re_rank_project_flow.md).

---

## Interview one-liner

**`np.array(..., dtype=float32)`** turns a batch of embeddings into the matrix FAISS searches; **`index.search`** returns **which rows** (which docs) are **nearest** to the query vector in distance.