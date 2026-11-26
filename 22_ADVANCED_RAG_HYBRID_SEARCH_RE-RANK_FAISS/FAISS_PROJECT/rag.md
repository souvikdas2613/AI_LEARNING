# `rag.py` — every step explained (FAISS twin)

Walkthrough of [`rag.py`](./rag.py) in this folder (`FAISS_PROJECT`).

**Same shape** as the topic-12 naive demo  
[`MULTI_DOCS_FULL_REAL_RAG_EXAMPLE/rag.py`](../../12_RAG_Retrieval_Augmented_Generation/MULTI_DOCS_FULL_REAL_RAG_EXAMPLE/rag.py)  
— only the **middle** changes: cosine loop → **FAISS** `IndexFlatL2` + `add` / `search`.

```text
knowledge/*.txt  →  embed once at startup  →  FAISS index.add
user question    →  embed
FAISS index.search (all docs)  →  print every L2  →  pick best file (rank 1)
best file text + question  →  chat model  →  answer
```

Related: [`../1_what_is_faiss.md`](../1_what_is_faiss.md) · [`../faiss_demo.py`](../faiss_demo.py) · [`../faiss_demo.md`](../faiss_demo.md) · naive walkthrough [`../../12_RAG_Retrieval_Augmented_Generation/MULTI_DOCS_FULL_REAL_RAG_EXAMPLE/rag.md`](../../12_RAG_Retrieval_Augmented_Generation/MULTI_DOCS_FULL_REAL_RAG_EXAMPLE/rag.md)

---

## What this script does (one sentence)

Loads text files from `knowledge/`, embeds them with `text-embedding-3-small`, stores the vectors in a **FAISS** index, and for each user message runs `index.search` over **all** docs (prints every L2), then asks a **chat** model to answer using only the **rank-1** file as context.

---

## Prerequisite — get the FAISS package

Python does **not** ship FAISS. You install Meta’s package from PyPI before `import faiss` works:

```bash
pip install faiss-cpu
```

| Package | What you get |
|---------|----------------|
| `faiss-cpu` | CPU build of FAISS (what this project uses) |
| `faiss` (import name) | After install, `import faiss` in `rag.py` |

Also need `numpy`, `openai`, and `python-dotenv` (same stack as the naive twin). Full one-liner is under [How to run](#how-to-run).

---

## Index

| # | Topic |
|---|--------|
| 0 | [Prerequisite — get the FAISS package](#prerequisite--get-the-faiss-package) |
| 1 | [Naive vs this file](#naive-vs-this-file) |
| 1b | [Did FAISS improve cosine similarity?](#did-faiss-improve-cosine-similarity) |
| 1c | [What is L2 (Euclidean) distance?](#what-is-l2-euclidean-distance) |
| 2 | [Line map (`rag.py`)](#line-map-ragpy) |
| 3 | [Execution order](#execution-order-what-runs-when) |
| 4 | [Code — step by step](#step-1--imports) |
| 5 | [Full RAG map](#full-rag-map-for-this-file) |
| 6 | [If we still dump the full doc, how is FAISS helpful?](#if-we-still-dump-the-full-doc-how-is-faiss-helpful) |
| 7 | [Limits (on purpose)](#limits-of-this-faiss-twin-on-purpose) |
| 8 | [How to run](#how-to-run) |
| 9 | [Example output](#example-output-sample-run) |

---

## Naive vs this file

| Piece | Naive `MULTI_DOCS…/rag.py` | This `FAISS_PROJECT/rag.py` |
|-------|----------------------------|-----------------------------|
| Docs | `knowledge/*.txt` | Same files (copied here) |
| Embed | `text-embedding-3-small` | Same |
| Retrieve | Manual cosine loop over all docs | **FAISS** `IndexFlatL2` + `search` |
| Score | Cosine similarity (**higher** = better) | L2 distance (**lower** = better) |
| Pick | Best filename by max score | Row `indices[0][0]` → `filenames[row]` |
| Prompt + chat | Whole best file as `RAG_Context` | Same |

**Talk line:** Same app. Same docs. Same prompt. Smarter index in the middle.

---

## Did FAISS improve cosine similarity?

**Short answer: No.** This FAISS twin does **not** improve cosine. We simply **did not call** your `cosine_similarity()` function here.

| | Naive `rag.py` | This `FAISS_PROJECT/rag.py` |
|--|----------------|-----------------------------|
| Your code | `cosine_similarity(question, doc)` in a Python loop | **No** `cosine_similarity` function |
| What runs instead | You compute `dot / (norm × norm)` yourself | FAISS `IndexFlatL2` + `index.search` |
| Metric in use | **Cosine** (higher = better) | **L2 distance** (lower = better) |
| Did cosine get “better”? | — | **No** — cosine isn’t used in this demo |

### So what *did* improve?

- **How we search:** DIY loop → engineered **index** (`add` / `search`)  
- **Scale story:** better when there are many vectors (FAISS is built for that)  
- **Not improved by this change alone:** answer quality from “better cosine,” leaner prompts, or token cost (we still dump the whole best file)

### Is “we don’t use cosine_similarity” a FAISS pro?

**No.** Avoiding that Python function is not a marketing win.

- Cosine is still a valid, common way to compare embeddings.  
- FAISS can do **cosine-like** search too (e.g. `IndexFlatIP` + normalized vectors).  
- This file picked **L2** because it’s the classic FAISS starter (`IndexFlatL2` in `faiss_demo.py`) — a **metric choice**, not “cosine was bad.”

| Metric | Typical FAISS setup | “Better” means |
|--------|---------------------|----------------|
| **L2** (this file) | `IndexFlatL2` | **Lower** distance |
| **Cosine-like** | e.g. `IndexFlatIP` + normalized vectors | Higher inner product / cosine |

**Talk line:** FAISS didn’t upgrade cosine — we swapped the slow DIY similarity loop for an index. In *this* demo the index uses L2, not our hand-written cosine.

---

## What is L2 (Euclidean) distance?

**L2 / Euclidean distance** = straight-line distance between two points (vectors) in space.

For two vectors \(a\) and \(b\):

\[
\text{L2}(a,b) = \sqrt{(a_1-b_1)^2 + (a_2-b_2)^2 + \cdots + (a_n-b_n)^2}
\]

**Tiny example (2-D):** \(a = [0, 0]\), \(b = [3, 4]\) → \(\sqrt{3^2 + 4^2} = 5\).

**In this demo**
- Each embedding is a point with ~1536 numbers (`text-embedding-3-small`)  
- L2 asks: “How far is the question point from each doc point?”  
- **Smaller number = closer = more similar** (unlike cosine, where **higher** is better)

**vs cosine (naive `rag.py`)**  
- Cosine → same **direction**? (ignore length)  
- L2 → how far apart in space?  

Both can work for “nearest doc”; `IndexFlatL2` uses this L2 formula for you — you don’t code the square-root sum yourself.

---

## Line map (`rag.py`)

| Lines | What |
|-------|------|
| 1–6 | Imports (includes `faiss`) |
| 8–11 | `load_dotenv` (chapter + cwd) + read `OPENAI_API_KEY` |
| 13–17 | Embedding vs chat model + `OpenAI()` client |
| 19–26 | `load_documents` |
| 29–34 | `create_embedding` |
| 37–45 | Load docs → `filenames` (list) → `TOP_K = len(filenames)` → `vectors` (NumPy `float32`) |
| 47–50 | **FAISS** `IndexFlatL2` → `add` → print size |
| 52–54 | Banner |
| 56–60 | Loop start + `quit` |
| 62–70 | Embed question → `search` → print **all** L2 ranks → `best_document` |
| 72–77 | `RAG_DOC_CONTENT` + build/print `prompt` |
| 79–89 | Chat completion + print answer |

---

## Execution order (what runs when)

1. Imports  
2. Load `.env`, set models, create `OpenAI()` client  
3. Define `load_documents`, `create_embedding`  
4. `documents = load_documents()`  
5. Build `filenames` + set `TOP_K = len(filenames)` + embed every file into a NumPy `float32` matrix  
6. Create FAISS index, `index.add(vectors)`  
7. Print banner  
8. Forever: `input` → quit? → embed question → `index.search` → print every L2 rank → map best row → filename → print context → prompt → chat → answer  

---

## Step 1 — Imports

```python
from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
import faiss
from pathlib import Path
```

| Line | Role |
|------|------|
| `OpenAI` | Embeddings **and** chat |
| `load_dotenv` | Keys / `MODEL_NAME` from `.env` |
| `numpy` | Matrix of vectors FAISS expects |
| `faiss` | Fast nearest-neighbor index (`IndexFlatL2`) |
| `Path` | `knowledge/` next to this script |

---

## Step 2 — Env and two different models

```python
load_dotenv(Path(__file__).resolve().parents[2] / ".env")
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = os.getenv("MODEL_NAME")
client = OpenAI()
```

| Piece | Meaning |
|-------|---------|
| First `load_dotenv(...)` | Also try the `AI_LEARNING` root `.env` (same habit as `faiss_demo.py`) |
| Second `load_dotenv(override=True)` | Cwd / local `.env` can override |
| `EMBEDDING_MODEL` | All `embeddings.create` calls |
| `CHAT_MODEL` | Only `chat.completions.create` — from `MODEL_NAME` in `.env` |

`TOP_K` is set later (after `filenames`) to `len(filenames)` so the demo prints **every** doc’s L2 — like naive RAG printing every cosine score. The LLM still uses rank 1 only.

---

## Step 3 — `load_documents` / `create_embedding`

Same idea as naive RAG:

- `documents` = `{ "python.txt": "<full text>", ... }`  
- `create_embedding(text)` → one vector (list of floats) from `text-embedding-3-small`

`knowledge/` is resolved next to `rag.py`, so the script works no matter what your shell cwd is (as long as you run this file).

---

## Step 4 — Build the FAISS matrix (startup)

```python
documents = load_documents()

# Stable row order so FAISS index i ↔ filenames[i] ↔ documents[name]
filenames = list(documents.keys())
TOP_K = len(filenames)  # print L2 for every doc (best is still indices[0][0])
vectors = np.array(
    [create_embedding(documents[name]) for name in filenames],
    dtype="float32",
)
```

FAISS only stores **numbers** (vectors). It does **not** store file names. So you keep two structures in the **same order**:

| Name | Type | Array? | Role |
|------|------|--------|------|
| `filenames` | Python **list** of strings | List, not a NumPy array | File names in a fixed order |
| `vectors` | NumPy **array** (`float32`) | Yes — 2D shape `(n_docs, dim)` | One embedding row per file, same order |
| `TOP_K` | `int` | — | `len(filenames)` → search returns **all** docs so you can print every L2 |

```python
filenames = ["python.txt", "cpp.txt", ...]          # list
vectors   = np.array([...], dtype="float32")        # array shape (N, 1536)
```

| Piece | Why it matters |
|-------|----------------|
| `filenames` | Stable row order: FAISS returns a **row index**, not a file name → later `filenames[row]` |
| `vectors` | NumPy `float32` matrix — what FAISS `add` / `search` need |
| `dtype="float32"` | What FAISS expects for the index |
| Same order | Row `i` ↔ `filenames[i]` ↔ that file’s text |
| Embed once at startup | Same as naive: don’t re-embed every file on every question |

**Layman / slide one-liner:** Same order matters — FAISS row `i` ↔ `filenames[i]` ↔ document text.

**Talk line:** `filenames` = list · `vectors` = NumPy array · lined up so search results can become file names again.

---

## Step 5 — FAISS in the middle

Those lines **build the filing cabinet**, then file every document vector into it — once at startup.

```python
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)
print(f"FAISS index ready: {index.ntotal} vectors, dim={vectors.shape[1]}")
```

### 1. `faiss.IndexFlatL2(vectors.shape[1])`

- Creates an **empty** FAISS index.
- `vectors.shape[1]` = **dimension** of each embedding (e.g. 1536 for `text-embedding-3-small`).
- **Flat** = store vectors as-is and compare **exactly** (no approximate shortcut).
- **L2** = score with Euclidean distance:
  \(\sqrt{(a-b)^2 + \ldots}\)
  → **smaller distance = more similar**.

**Layman:** empty filing cabinet labeled “vectors of length `dim`.”

### 2. `index.add(vectors)`

- Puts your matrix into the cabinet.
- `vectors` shape is `(n_docs, dim)` — one row per file (`filenames[i]` ↔ row `i`).
- After this, FAISS can answer: “which rows are closest to this query vector?”

### 3. The print

- `index.ntotal` = how many vectors were added (should equal the number of `.txt` files).
- `dim` = embedding length — must match the query vector later or `search` fails.

| Call | Meaning |
|------|---------|
| `IndexFlatL2(dim)` | Exact search with **L2 (Euclidean) distance**. `dim` = length of each embedding |
| `index.add(vectors)` | Store all document vectors as rows |
| `index.ntotal` | How many vectors are in the index |

**Slide paste:**

```text
index = FAISS filing cabinet (IndexFlatL2 = exact L2 search)
index.add(vectors) → store every doc embedding as a row
index.ntotal       → how many vectors are in the index
dim = vectors.shape[1]  (e.g. 1536 for text-embedding-3-small)
```

**One-liner:** Create empty FAISS index → add all vectors → ready to search.

**Later in the loop:** embed the question → `index.search(query, k=TOP_K)` with `TOP_K = len(filenames)` → print **every** L2 → map best row → filename → dump that file into the prompt.

This **replaces** the naive `for filename, embedding in document_embeddings.items(): cosine_similarity(...)` loop. Same “find nearest doc” job; here the loop lives inside FAISS instead of your Python cosine loop.

**Note:** Naive used **cosine** (direction). This demo uses **L2** (classic FAISS starter index from `faiss_demo.py`). Both find “nearby” embeddings; scores are not interchangeable — here **smaller distance = closer**. See also [Did FAISS improve cosine similarity?](#did-faiss-improve-cosine-similarity) and [What is L2 (Euclidean) distance?](#what-is-l2-euclidean-distance).

---

## Step 6 — Query loop: search → print all L2 → best doc → chat

```python
question_embedding = create_embedding(user_input)
query = np.array([question_embedding], dtype="float32")
distances, indices = index.search(query, k=TOP_K)

for rank, row in enumerate(indices[0]):
    print(f"Rank {rank + 1}: {filenames[row]}  (L2 distance: {distances[0][rank]:.4f})")

best_document = filenames[indices[0][0]]
RAG_DOC_CONTENT = documents[best_document]
```

| Piece | Meaning |
|-------|---------|
| `query` shape `(1, dim)` | FAISS always wants a **batch** of queries (even if batch size is 1) |
| `TOP_K = len(filenames)` | Return **all** docs so the demo can print every L2 (teaching parallel to naive’s per-doc cosine scores) |
| `distances` | L2 distances for the neighbors (**lower** is better) |
| `indices` | Row numbers into `filenames` / `vectors` (best first) |
| `indices[0][0]` | Best match for the first (only) query — still what the LLM uses |
| Prompt + chat | Identical idea to naive: whole best file as `RAG_Context` |

### The print loop (why it exists)

After `index.search`, FAISS returns:
- `indices[0]` — row numbers of nearest docs (**best first**)
- `distances[0]` — L2 distance for each of those rows (**lower = closer**)

```python
for rank, row in enumerate(indices[0]):
    # rank = 0, 1, 2…  → print as Rank 1, 2, 3…
    # row  = FAISS row index → filenames[row] is the file name
    print(f"Rank {rank + 1}: {filenames[row]}  (L2 distance: {distances[0][rank]:.4f})")
```

**Example output**

```text
Rank 1: python.txt  (L2 distance: 0.8123)
Rank 2: cpp.txt     (L2 distance: 1.2045)
...
```

**Slide one-liner:** Loop over FAISS results → map row → file name → print L2 for each.

Then `client.chat.completions.create(...)` answers using only the **rank-1** file as context.

Type `quit` to exit.

---

## Full RAG map for this file

```text
┌─────────────┐     embed      ┌──────────────┐
│ knowledge/  │ ─────────────► │ float32 rows │
│  *.txt      │                └──────┬───────┘
└─────────────┘                       │ index.add
                                      ▼
                               ┌──────────────┐
                               │ FAISS Index  │
                               │  Flat L2     │
                               └──────▲───────┘
                                      │ index.search
┌─────────────┐     embed      ┌──────┴───────┐
│ user text   │ ─────────────► │ query vector │
└─────────────┘                └──────────────┘
                                      │
                                      ▼
                               best filename
                                      │
                                      ▼
                         whole file → prompt → chat LLM
```

---

## If we still dump the full doc, how is FAISS helpful?

Honest answer: **in this twin, the prompt is the same fat habit** — so FAISS is **not** saving tokens yet.

You still send the whole `RAG_DOC_CONTENT` into the chat prompt (same as naive). That is **on purpose** for a fair compare: same docs, same prompt shape, only the retrieval engine changes.

### What FAISS helps here

- The **search** step: find nearest vectors **fast**, especially when you have many docs or chunks  
- Replaces “score every file in a Python loop” with an index built for that job  
- Same app shape so you can say: *only the middle changed*

### What FAISS does *not* fix by itself

- Dumping the **whole** best file into the prompt  
- Wrong / noisy context  
- Retry loops from weak grounding  

That’s why the meetup story has **three parts**: FAISS → Hybrid → Re-rank.

| Part | What it improves |
|------|------------------|
| **FAISS** | Faster / scalable **retrieve** |
| **Hybrid** | Better **candidates** (meaning + keywords) |
| **Re-rank + top 2–3** | **Leaner prompt** → fewer tokens (the energy angle) |

**Talk line:** FAISS makes retrieval scalable. It doesn’t automatically make the prompt thin — that’s why we still need smarter selection *after* FAISS.

So this `rag.py` is the **fair compare** to naive. The energy win shows up later in this chapter (hybrid + re-rank + lean chunks) — see [`../HYBRID_PROJECT/`](../HYBRID_PROJECT/) and [`../RE_RANK_PROJECT/`](../RE_RANK_PROJECT/).

---

## Limits of this FAISS twin (on purpose)

- Still dumps the **entire** best `.txt` into the prompt (same overspend habit as naive) — see section above.  
- `TOP_K = len(filenames)` prints **all** L2 ranks for the demo; the LLM still uses only rank 1. No hybrid, no re-rank yet (those come later in this chapter). For a real app you might set `TOP_K = 1` (or a small k).  
- `IndexFlatL2` is exact and simple — great for learning; huge corpora often use approximate indexes.  
- No persistence: index is rebuilt in memory every run.

Energy-aware path later: hybrid + re-rank + lean top 2–3 chunks (see `HYBRID_PROJECT/` then `RE_RANK_PROJECT/`).

---

## How to run

**Prerequisite:** install FAISS first (see [above](#prerequisite--get-the-faiss-package)) — without `faiss-cpu`, `import faiss` fails.

```bash
pip install faiss-cpu numpy openai python-dotenv
python rag.py
```

Needs `OPENAI_API_KEY` and `MODEL_NAME` in `.env` (same as other chapter demos).

---

## Example output (sample run)

```text
python rag.py

FAISS index ready: 4 vectors, dim=1536

========================================
      My AI Assistant (FAISS)
========================================

You : what is python ?
Rank 1: python.txt              (L2 distance: 0.7979)
Rank 2: machine_learning.txt   (L2 distance: 1.1024)
Rank 3: mysql.txt              (L2 distance: 1.1856)
Rank 4: weather.txt            (L2 distance: 1.3012)
Best document: python.txt

RAG_DOC_CONTENT: Python is a high-level programming language.

It is widely used for Artificial Intelligence,
Machine Learning,
Data Science,
Automation,
and Web Development.

AI_ASSISTANT_PROMPT: Use ONLY the Context below to answer.
If the user typed a topic or keyword (not a full question), briefly explain what it is using the Context.
If the Context truly has nothing relevant, say 'I don't know.'

RAG_Context: Python is a high-level programming language.

It is widely used for Artificial Intelligence,
Machine Learning,
Data Science,
Automation,
and Web Development.

USER_INPUT: what is python ?

AI : Python is a high-level programming language that is widely used for various applications, including Artificial Intelligence, Machine Learning, Data Science, Automation, and Web Development.

You : quit

AI  : Goodbye! Have a great day.
```

### What to notice in this run

| Line | Meaning |
|------|---------|
| `4 vectors, dim=1536` | Four `knowledge/*.txt` files; each embedding has 1536 numbers (`text-embedding-3-small`) |
| `Rank 1…4` with L2 | Demo prints **every** doc (`TOP_K = len(filenames)`) — **lower** L2 = closer |
| `Best document` / `RAG_DOC_CONTENT` | Still rank 1 only → whole matching file (same fat-prompt habit as naive) |
| `AI_ASSISTANT_PROMPT` | Context + user text sent to the **chat** model |
| `AI : …` | Answer grounded on that file only |
