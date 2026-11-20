# Re-rank project — hybrid shortlist → LLM re-rank → lean prompt

Folder **`RE_RANK_PROJECT`** — same hybrid shortlist as [`../HYBRID_PROJECT/`](../HYBRID_PROJECT/), then an **LLM re-rank** keeps **top 3** for the answer prompt.

Do hybrid alone first: [`../HYBRID_PROJECT/hybrid_project_flow.md`](../HYBRID_PROJECT/hybrid_project_flow.md)

**Run this:** [`main.py`](./main.py)

**Knowledge files (shared):** [`../documents/`](../documents/)

| File | Topic |
|------|--------|
| `kubernetes.txt` | K8s / kubectl / Pods |
| `python.txt` | Python basics |
| `cpp.txt` | C++ basics |

---

## Why it is needed (utility)

Hybrid improves the **candidate pool**. It can still leave weak / off-topic docs in the shortlist. **Re-rank** is a second pass: score each candidate for “does this answer the query?” and keep only the winners in the prompt.

| Why use it | Plain meaning |
|------------|----------------|
| **Precision after recall** | Hybrid finds; re-rank chooses what the LLM sees |
| **Leaner prompt** | Top **3** instead of dumping the whole hybrid top-5 |
| **Energy angle** | Fewer junk tokens → less inference work for the answer call |
| **Explicit scores** | LLM returns **0–100** per candidate — easy to show in a demo |

**Talk line:** Hybrid finds. Re-rank chooses what enters the prompt.

---

## Is it accurate?

| Question | Answer for this project |
|----------|-------------------------|
| **Does hybrid math match HYBRID_PROJECT?** | **Yes.** Chroma `search` → `1/(1+d)` + `keyword_score` → `0.7 / 0.3`. |
| **Does re-rank keep top 3?** | **Yes.** `rerank(..., top_k=3)` after the hybrid shortlist. |
| **Is the 0–100 score perfect?** | **No.** Teaching LLM judge; can fail to parse → score `0`. |
| **Whole-file indexing?** | **Yes today** — `chunk=False` in `main`. |

**Short verdict:** correct **re-rank teaching pipeline** on top of hybrid; not production BM25 + cross-encoder.

---

## What it does (one sentence)

Index docs into Chroma, build a **hybrid top-5**, ask the chat model to score each candidate **0–100**, keep **top 3**, answer from those only.

---

## Formula / rules used

### Hybrid (same as HYBRID_PROJECT)

```text
semantic = 1 / (1 + chroma_distance)
keyword  = |query_words ∩ text_words| / |query_words|
combined = 0.7 * semantic + 0.3 * keyword
```

### Re-rank

```text
For each hybrid candidate:
  LLM → relevance 0..100  (number only)
Sort by rerank_score descending → keep top_k=3
```

| Score | Meaning (prompt instructions) |
|-------|-------------------------------|
| **100** | Directly answers the query |
| **0** | Completely irrelevant |

---

## Files (on disk)

| File | Role |
|------|------|
| [`main.py`](./main.py) | Index + chat; prints **Ranking** after re-rank |
| [`rerank_rag.py`](./rerank_rag.py) | `build_rag` + `retrieve` (hybrid → `rerank`) |
| [`reranker.py`](./reranker.py) | LLM 0–100 per candidate; return top 3 |
| [`generator.py`](./generator.py) | Answer from **winners only** |
| [`retriever.py`](./retriever.py) | `keyword_score` only |
| [`embeddings.py`](./embeddings.py) | `text-embedding-3-small` |
| [`chroma_store.py`](./chroma_store.py) | Persist + semantic `search` |
| [`chunker.py`](./chunker.py) | Ready if you set `chunk=True` |
| `re_rank_project_flow.md` | This note |

**No** leftover in-memory `semantic_search` / `hybrid_search`. Semantic = Chroma `search`.

---

## Wired

| Piece | Used by `main.py`? |
|-------|---------------------|
| `chroma_store.search` | Yes — via `rerank_rag.retrieve` |
| `retriever.keyword_score` | Yes — hybrid blend |
| `reranker.rerank` | Yes — end of `retrieve` |
| `generator.generate_answer` | Yes — winners only |
| `chunker` | Imported; not run while `chunk=False` |

---

## Functions — main job

| Function | File | Job |
|----------|------|-----|
| `main()` | `main.py` | Index → loop: `retrieve` → print ranking → generate |
| `build_rag(...)` | `rerank_rag.py` | Optional chunk → embed → Chroma upsert |
| `retrieve(query, top_k=5)` | `rerank_rag.py` | Hybrid top-k → print scores → `rerank(..., 3)` |
| `rerank(query, candidates, top_k=3)` | `reranker.py` | LLM score each → sort → slice |
| `search` / `add_chunks` | `chroma_store.py` | Semantic store + query |
| `keyword_score` | `retriever.py` | Lexical overlap |
| `generate_answer` | `generator.py` | Chat from re-ranked context |

---

## Full pipeline map

```text
documents/*.txt
      │
      ▼
 build_rag (chunk=False)
      │
      ▼
 embed → Chroma upsert
      │
      ▼
 user query
      │
      ▼
 Chroma search → semantic + keyword → combined   (hybrid top 5)
      │
      ▼
 print Hybrid candidates (semantic / keyword / combined)
      │
      ▼
 rerank → LLM 0–100 each → keep top 3
      │
      ▼
 print Ranking (rerank=…)
      │
      ▼
 generate_answer (winners only)
```

---

## Line-by-line — [`main.py`](./main.py)

| Line(s) | What happens |
|---------|----------------|
| 6–7 | Import `build_rag`, `retrieve`, `generate_answer`. |
| 9–12 | Load `.env`; `DOCUMENTS_DIR` = `../documents/`. |
| 16–19 | Exit if missing `OPENAI_API_KEY` / `OPENAI_MODEL`. |
| 20–27 | Index every `*.txt` with `chunk=False`. |
| 29–39 | Chat loop: `retrieve` → print winners with `rerank=` → `generate_answer`. |
| 42–43 | `python main.py` entry point. |

---

## Line-by-line — [`rerank_rag.py`](./rerank_rag.py)

| Line(s) | What happens |
|---------|----------------|
| 1–5 | Imports: chunker, embeddings, Chroma `add_chunks`/`search`, `keyword_score`, `rerank`. |
| 8–15 | `build_rag` — same as hybrid (whole file when `chunk=False`). |
| 18–20 | Embed query; Chroma `search` (semantic neighbors). |
| 26–40 | Per neighbor: `semantic = 1/(1+d)`, keyword, `combined = 0.7/0.3`. |
| 41–42 | Sort by combined; keep hybrid `top_k` (default 5). |
| 43–51 | Print hybrid scores (no `chunk 0`); announce LLM re-rank. |
| 52 | **`return rerank(query, candidates, top_k=3)`** — this is the extra step vs hybrid. |

---

## Line-by-line — [`reranker.py`](./reranker.py)

| Line(s) | What happens |
|---------|----------------|
| 7–12 | `.env` + chat `MODEL` from `OPENAI_MODEL`. |
| 15–17 | Loop each hybrid candidate. |
| 18–33 | Prompt: score relevance **0–100**; return **number only**. |
| 34–38 | `chat.completions.create` (`temperature=0`). |
| 39–44 | Parse float; on failure use `0`; attach `rerank_score`. |
| 45–46 | Sort high→low; return first `top_k` (3). |

---

## Line-by-line — other modules

| File | Notes |
|------|--------|
| [`chroma_store.py`](./chroma_store.py) | Same as hybrid: `upsert` + `search`. |
| [`embeddings.py`](./embeddings.py) | `create_embedding` / `embed_chunks`. |
| [`retriever.py`](./retriever.py) | `keyword_score` only. |
| [`chunker.py`](./chunker.py) | Unused while `chunk=False`. |
| [`generator.py`](./generator.py) | Joins winner texts → grounded chat answer. |

---

## Execution order (what runs when)

1. `python main.py` → load `.env`  
2. Index `documents/*.txt` → Chroma  
3. Query → hybrid top 5 (print scores)  
4. LLM re-rank each → keep 3 (print `rerank=`)  
5. Generate from those 3 only  
6. Repeat until `quit` / `exit`

---

## Sample run output

Captured from a real run of `python main.py`. Whole files are indexed (no real chunking) — prints show **file + scores**, not `chunk 0`.

```text
python main.py
Building re-rank RAG (whole files → Chroma)...
  indexed cpp.txt
  indexed kubernetes.txt
  indexed python.txt

Ready — hybrid shortlist, then LLM re-rank keeps top 3 for the prompt.

You : what is python ?

1) Hybrid shortlist (before re-rank):
- python.txt  semantic=0.543  keyword=0.500  combined=0.530
- cpp.txt  semantic=0.392  keyword=0.250  combined=0.349
- kubernetes.txt  semantic=0.364  keyword=0.250  combined=0.330

2) LLM re-rank → keep top 3 (scores 0–100)...

3) Winners after re-rank (enter the prompt):
- python.txt  rerank=90.0
- cpp.txt  rerank=0.0
- kubernetes.txt  rerank=0.0

RAG :
Python is a high-level language known for readable syntax and a large standard library.

You : quit
```

### What to notice — this proves re-rank ran

| Step | What you see | Why it matters |
|------|----------------|----------------|
| **1)** | Hybrid `combined=` order | First pass only (meaning + keywords) |
| **2)** | “LLM re-rank → keep top 3” | Second pass starts (extra LLM calls) |
| **3)** | `rerank=90` vs `rerank=0` | Judge scored relevance; weak docs get **0** |
| **RAG :** | Answer from winners | Prompt uses step **3**, not the raw hybrid dump |

---

## How to run

```bash
pip install chromadb openai python-dotenv
python main.py
```

Needs `OPENAI_API_KEY` and `OPENAI_MODEL` in `.env` (repo `AI_LEARNING` root).

---

## Compare with HYBRID_PROJECT

| | Hybrid only | **This re-rank project** |
|---|-------------|---------------------------|
| Shortlist | Chroma + 0.7/0.3 | Same |
| Extra pass | No | LLM 0–100 → top 3 |
| Prompt context | Hybrid top-k texts | **Re-rank winners only** |
| Entry | `hybrid_rag.retrieve` | `rerank_rag.retrieve` → `rerank` |

---

## Interview one-liner

**Re-rank** = second-pass scoring of a hybrid shortlist so only the best **2–3** chunks enter the answer prompt — better precision, fewer tokens.
