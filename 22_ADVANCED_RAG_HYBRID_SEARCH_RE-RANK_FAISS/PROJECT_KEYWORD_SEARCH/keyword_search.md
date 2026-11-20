# Keyword search lab — one file

Folder **`PROJECT_KEYWORD_SEARCH`** — retrieve by **shared words** only (no embeddings, no API).

---

## Why it is needed (utility)

RAG has to **find the right text** before the LLM answers. Keyword (lexical) search is one retrieval leg — not optional in real systems that mix **keyword + vector** (hybrid search).

| Why use it | Plain meaning |
|------------|----------------|
| **Exact tokens** | User names a command, error code, SKU, or API (`kubectl`, `RAII`, `OSAC-4795`). Embedding search can drift; **if the word is in the doc, keyword search can surface it**. |
| **Fast and cheap** | No embedding API, no vector index — split strings, count overlap, sort. Good for **baselines**, tests, and offline labs (this folder). |
| **Hybrid RAG** | [`../HYBRID_PROJECT/`](../HYBRID_PROJECT/) and many production stacks **blend** keyword score + semantic score so paraphrases *and* exact spellings both have a path to rank. This lab isolates the **keyword half** so you see it clearly. |
| **Interpretable** | Score = “what fraction of my question words appear here?” You can explain a hit without a black-box model. |
| **Complement to semantic** | Semantic search wins when the user **rephrases**; keyword wins when they **copy the same words** as the doc. See [`../PROJECT_SEMANTIC_SEARCH/semantic_search.md`](../PROJECT_SEMANTIC_SEARCH/semantic_search.md). |

**Utility of *this* script:** a minimal teaching implementation of that idea — same overlap logic as the keyword path in [`../HYBRID_PROJECT/retriever.py`](../HYBRID_PROJECT/retriever.py), not production BM25.

---

## Is it accurate?

**Depends what you mean by accurate.**

| Question | Answer for this lab |
|----------|---------------------|
| **Does it correctly implement its own rule?** | **Yes.** It tokenizes query and doc, takes the **set intersection**, and divides by **number of query words**. Empty query → 0. Higher score always means more query tokens matched. |
| **Is the rule a good model of “relevance”?** | **Sometimes.** Good when the query shares **important words** with the right file (e.g. “list pods kubectl” → `kubernetes.txt`). **Poor** when the user paraphrases, uses synonyms, or asks in different words than the doc — overlap can be **0** even when the answer is in the corpus. |
| **Is this script “production accurate”?** | **No.** It is deliberately simple: no stemming (`running` vs `run`), no stop-word handling, no BM25 (term frequency, doc length), no phrase matching, punctuation sticks to tokens (`kubectl?` ≠ `kubectl`). Production keyword layers fix those; this file teaches the **core overlap idea** only. |
| **Whole-file vs chunking** | Docs are **entire `.txt` files**. A short relevant sentence buried in a long unrelated file does not get its own score — chunking in the full project changes what “accurate” feels like. |

**Short verdict:** **arithmetically accurate** for overlap ratio; **relevance-accurate only when lexical overlap matches user intent**. For paraphrase and meaning, rely on semantic/hybrid retrieval — not keyword alone.

**Real run that shows the limit:** [Worked example — `What is RAII in C++?`](#worked-example--what-is-raii-in-c-insights)

---

**Semantic lab:** [`../PROJECT_SEMANTIC_SEARCH/semantic_search.md`](../PROJECT_SEMANTIC_SEARCH/semantic_search.md)  
**Hybrid (combined):** [`../HYBRID_PROJECT/hybrid_project_flow.md`](../HYBRID_PROJECT/hybrid_project_flow.md)

| File | Role |
|------|------|
| [`keyword_search.py`](./keyword_search.py) | **Run this** — score by word overlap, print top-k (script uses **top 3**) |

**Knowledge files (shared):** [`../documents/`](../documents/) — one **whole file** per topic (no chunking yet):

| File | Topic |
|------|--------|
| `kubernetes.txt` | K8s / kubectl / Pods |
| `python.txt` | Python basics |
| `cpp.txt` | C++ basics |

Chunking comes later in [`../HYBRID_PROJECT/`](../HYBRID_PROJECT/) (`build_rag(..., chunk=True)`).

---

## What it does (one sentence)

Split query and each doc into **words**; score how many **query words appear** in the doc; return the highest scores.

---

## Formula used

### Tokenize (simple)

```text
query_words = set(lowercase(query).split())
text_words  = set(lowercase(doc).split())
```

### Keyword score (overlap ratio)

```text
matches = query_words ∩ text_words

keyword_score = |matches| / |query_words|
```

| Piece | Meaning |
|-------|---------|
| **Intersection** | Words that appear in **both** query and doc |
| **Divide by \|query_words\|** | “What **fraction** of my question words did this doc hit?” |
| **Empty query** | Score **0** (avoid divide-by-zero) |

| Score | Meaning |
|-------|---------|
| **1.0** | Every query word appears in the doc |
| **0.0** | No shared words |
| **Higher is better** | Sort **descending**, take top-k |

This is a **teaching** scorer (like `keyword_score` in [`HYBRID_PROJECT/retriever.py`](../HYBRID_PROJECT/retriever.py)), not full BM25.

---

## Worked example — `What is RAII in C++?` (insights)

This is from a real run of [`keyword_search.py`](./keyword_search.py) (`DEMO_QUERIES` includes this question). It shows **correct math** but **weak relevance checking**.

### Sample output (ranked summary from `main`)

```text
Query: What is RAII in C++?

  1. score=0.4000 cpp.txt: C++ is a compiled systems language used for performance-critical software. Source files are often...
  2. score=0.4000 python.txt: Python is a high-level language known for readable syntax and a large standard library. Common ty...
  3. score=0.2000 kubernetes.txt: Kubernetes (K8s) runs containerized applications across a cluster of machines. A Pod is the small...
```

### Query tokens (5 words)

After `query.lower().split()`:

```text
['what', 'is', 'raii', 'in', 'c++?']
```

| Query token | Matched in `cpp.txt`? | Why |
|-------------|----------------------|-----|
| `what` | No | Word not in file |
| `is` | Yes | e.g. “C++ **is** a compiled…” |
| `raii` | **No** | File has `RAII:` → token **`raii:`** (colon attached) — not equal to `raii` |
| `in` | Yes | e.g. “common **in** game engines…” |
| `c++?` | **No** | File has `c++`, `c++17` — no `?` on those tokens |

The line that *defines* RAII in [`../documents/cpp.txt`](../documents/cpp.txt) is:

```text
  - RAII: constructors acquire resources, destructors release them
```

So a human knows `cpp.txt` is the right file — but this scorer **does not count** `raii` for that reason.

### Scores per file

| File | Tokens that match query | Calculation | Score |
|------|-------------------------|-------------|-------|
| `cpp.txt` | `is`, `in` | 2 ÷ 5 | **0.4000** |
| `python.txt` | `is`, `in` | 2 ÷ 5 | **0.4000** |
| `kubernetes.txt` | `is` only | 1 ÷ 5 | **0.2000** |

### Why both #1 and #2 show **0.4000**

They are a **tie**: same two **generic** English tokens (`is`, `in`), not because both answer RAII. Python is not a C++ doc; it just happens to contain “**is**” and “**in**” in normal sentences.

`cpp.txt` is listed **first** only because of **sort stability** when scores are equal — **not** because it matched `raii` or `c++` better.

### Insights — what is this good for “checking”?

| You want to check… | This keyword overlap… |
|--------------------|------------------------|
| Did the code compute the formula correctly? | **Yes** — reproducible token sets and 2/5, 1/5, etc. |
| Did we retrieve the **right** doc for the user? | **Often no** — best content file ties with an unrelated file |
| Does the doc contain the **concept** RAII? | **Unreliable here** — `raii` ≠ `raii:` |
| Exact copy-paste terms (`kubectl get pods`) | **Better** — when tokens align, scores separate clearly |

**Takeaway:** Treat this score as a **literal word-overlap check**, not a **quality check** for RAG retrieval. For “did we get the right answer doc?”, use **semantic search**, **hybrid** ranking, or human review — see [Compare with semantic lab](#compare-with-semantic-lab).

---

## Functions — main job

| Function | Job |
|----------|-----|
| `keyword_score(query, text)` | One doc, one number (formula above). |
| `load_documents()` | Read every `*.txt` from [`../documents/`](../documents/). |
| `keyword_search(query, docs, top_k)` | Score all docs, sort, return top-k. Also **prints debug** (per-doc name + full ranked dump). |
| `main()` | Load files, run demo queries, print final ranks + preview. |

No `create_embedding` — **no cost**, works offline.

---

## Line-by-line — [`keyword_search.py`](./keyword_search.py)

Your recent edits add **typing import**, **`set[Any](...)`** on the query side, **per-document prints** inside search, a **verbose “Results” block** (full text + score for every doc), and **`top_k=3`** in `main` (was 2). The table below walks the file in run order.

### Imports and paths (lines 1–12)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 1 | `from typing import Any` | Pulls `Any` from the type-hint module. Only used on line 39 below. |
| 4 | `from pathlib import Path` | `Path` = file/folder paths without hard-coding OS slashes. |
| 6 | `DOCUMENTS_DIR = Path(__file__).resolve().parents[1] / "documents"` | `__file__` is this `.py` file. `resolve()` makes it absolute. `parents[1]` goes **up two** folders (`PROJECT_KEYWORD_SEARCH` → `22_ADVANCED_RAG_...`), then into **`documents/`** (same folder as hybrid/re-rank projects). |
| 8–12 | `DEMO_QUERIES = [...]` | Three fixed questions the demo runs automatically — one tuned to each `.txt` topic. |

### `load_documents()` (lines 15–28)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 16 | `docs = []` | Empty list; each item will be one dict per file. |
| 17 | `for doc_id, path in enumerate(sorted(...glob("*.txt"))):` | `glob("*.txt")` finds every text file in `DOCUMENTS_DIR`. `sorted(...)` makes order stable (`cpp.txt`, `kubernetes.txt`, `python.txt` alphabetically). `enumerate` gives **0, 1, 2, …** as `doc_id`. |
| 18–22 | `docs.append({...})` | One record: numeric **`doc_id`**, filename **`source`**, full file body **`text`** via `read_text(encoding="utf-8")`. |
| 24–27 | `print(...)` | Startup log: count, then **two lines per doc** (id, then name). Helps you see what was loaded before any query runs. |
| 28 | `return docs` | List of 3 dicts (if three `.txt` files exist). |

### `preview(text, length=100)` (lines 31–35)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 32 | `" ".join(text.split())` | Collapses newlines/tabs/extra spaces into **one line** of words. |
| 33–34 | `if len(one_line) <= length` | Short text → return as-is. |
| 35 | `one_line[: length - 3] + "..."` | Long text → first **97** chars + **`...`** so `main()`’s final print line stays readable (not the full file). |

### `keyword_score(query, text)` (lines 38–44)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 39 | `query_words = set[Any](query.lower().split())` | Lowercase query, split on whitespace → **unique** query tokens. **`set[Any](...)`** is the same as **`set(...)`** at runtime; the `[Any]` is a type hint on the constructor (unusual style — idiomatic Python is just `set(query.lower().split())`). |
| 40 | `text_words = set(text.lower().split())` | Same tokenization for the **whole document** (entire `.txt`). |
| 41–42 | `if not query_words: return 0.0` | Empty query after split → avoid **divide by zero** later. |
| 43 | `matches = query_words & text_words` | **Set intersection** — words that appear in **both** query and doc. Order does not matter; repeats in the doc do not add extra matches. |
| 44 | `return len(matches) / len(query_words)` | **Overlap ratio**: fraction of **query** words found in the doc. Denominator is **only** query word count, not doc length. |

Worked example — query `"How do I list pods with kubectl?"`:

```text
query_words ≈ {how, do, i, list, pods, with, kubectl?}   # 7 tokens (punctuation sticks)
vs kubernetes.txt → matches often include list, pods, with → score 3/7 ≈ 0.43
```

**Punctuation caveat:** `kubectl?` from the question ≠ `kubectl` in the file unless you normalize punctuation (this teaching script does not).

### `keyword_search(query, docs, top_k=2)` (lines 47–65)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 48 | `results = []` | Will hold one dict per doc with score attached. |
| 49–57 | `for doc in docs:` loop | Visit **every** loaded file. |
| 50 | `print(f"Doc: {doc['source']}")` | **Your edit** — while scoring, prints which file is being scored (e.g. `Doc: kubernetes.txt`). |
| 51 | `score = keyword_score(...)` | Single float for this doc. |
| 52–57 | `results.append({...})` | Copy `doc_id`, `source`, `text`, plus **`keyword_score`**. |
| 58 | `results.sort(..., reverse=True)` | Highest score first; ties keep stable-ish order from Python’s sort. |
| 59–64 | **Your edit** — debug block | Prints **all** docs after sort: filename, **full `text`**, raw score, blank lines. This is for **learning/debug**; it is noisy compared to production RAG. |
| 65 | `return results[:top_k]` | Slice: only the first **`top_k`** dicts go back to the caller (default **2** if you omit the argument). |

**Important:** `main()` passes **`top_k=3`**, so the return value has **three** hits, but the debug prints still show **all** docs every time.

### `main()` and entry point (lines 68–85)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 69 | `docs = load_documents()` | Load + print inventory. |
| 70–71 | `if not docs: raise SystemExit(...)` | Fail fast if `documents/` is empty. |
| 72 | `print(f"Keyword search — ...")` | Banner: whole-file retrieval, no chunking. |
| 74–75 | `for query in DEMO_QUERIES` | Run all three demo questions. |
| 76 | `hits = keyword_search(query, docs, top_k=3)` | **Your edit** — retrieve **top 3** (all files when you only have three). Triggers per-doc + full Results debug inside `keyword_search`. |
| 77–81 | `for rank, hit in enumerate(hits, ...)` | **Second** output pass: clean one-liners with **4-decimal score**, filename, **`preview(text)`** (not full body). |
| 84–85 | `if __name__ == "__main__": main()` | Running `python keyword_search.py` executes `main()`; importing the module does **not** auto-run. |

### Console flow (what you see when you run)

```text
Loaded N documents + id/source lines
Keyword search banner

For each DEMO_QUERY:
  Query: ...
  Doc: cpp.txt
  Doc: kubernetes.txt
  Doc: python.txt

  Results:
    (every file, full text, score — your debug block)

  1. score=0.xxxx source: preview...
  2. ...
  3. ...
```

So one query produces **three layers** of output: load list, **scoring debug**, **sorted dump**, then **ranked summary** from `main()`.

---

## How to run

```bash
python keyword_search.py
```

No `.env` required.

---

## Compare with semantic lab

Both labs read the same three files under [`../documents/`](../documents/). Run:

```bash
# folder PROJECT_KEYWORD_SEARCH
python keyword_search.py

# folder PROJECT_SEMANTIC_SEARCH
python semantic_search.py
```

**Keyword weakness:** question *“What language is used for scripting?”* may not share tokens with *“Python is a high-level programming language.”* → score **0**.

**Semantic strength:** embeddings can still rank the Python line high.

**Keyword strength:** exact product names, IDs, error codes — words must match.

---

## Interview one-liner

**Keyword search** = overlap of query tokens and document tokens — fast and exact, weak when the user **paraphrases**.