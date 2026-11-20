# Hybrid project — Chroma + semantic + keyword

Folder **`HYBRID_PROJECT`** — retrieve by **meaning + words** together, then answer with a chat model. **No re-rank** here.

Learn the two signals separately first:

- [`../PROJECT_SEMANTIC_SEARCH/semantic_search.md`](../PROJECT_SEMANTIC_SEARCH/semantic_search.md) — embeddings + cosine  
- [`../PROJECT_KEYWORD_SEARCH/keyword_search.md`](../PROJECT_KEYWORD_SEARCH/keyword_search.md) — word overlap  

Next step (LLM re-rank → lean prompt): [`../RE_RANK_PROJECT/re_rank_project_flow.md`](../RE_RANK_PROJECT/re_rank_project_flow.md)

**Run this:** [`main.py`](./main.py)

**Knowledge files (shared):** [`../documents/`](../documents/)

| File | Topic |
|------|--------|
| `kubernetes.txt` | K8s / kubectl / Pods |
| `python.txt` | Python basics |
| `cpp.txt` | C++ basics |

---

## Why it is needed (utility)

Keyword alone misses paraphrases. Semantic alone can miss exact tokens (error codes, `kubectl`, product IDs). **Hybrid** blends both so each path can rescue the other.

| Why use it | Plain meaning |
|------------|----------------|
| **Two signals** | ~0.7 meaning (Chroma neighbors) + ~0.3 word overlap |
| **Same idea as production** | Many real RAG stacks: vector recall → lexical boost → shortlist → LLM |
| **Chroma, not a Python loop** | Vectors live in `./chroma_db`; `search` is the semantic half |
| **Teaching bridge** | After the two labs, before re-rank |

**Utility of *this* folder:** one runnable chat loop that indexes whole files into Chroma, scores hybrid, and generates — without a second LLM re-rank pass.

---

## Is it accurate?

**Depends what you mean by accurate.**

| Question | Answer for this project |
|----------|-------------------------|
| **Does the blend math run as written?** | **Yes.** `combined = 0.7 * semantic + 0.3 * keyword` in `retrieve`. |
| **Is Chroma the semantic search?** | **Yes.** `chroma_store.search` = nearest neighbors by embedding. No separate `semantic_search()` function here. |
| **Is whole-file indexing “best”?** | **Teaching only.** `main` uses `chunk=False` — one vector per file. Flip `chunk=True` later for smaller pieces. |
| **Production quality?** | **No.** Simple keyword overlap (not BM25), fixed weights, no re-rank, small demo corpus. |

**Short verdict:** correct **hybrid teaching pipeline**; not a full production retriever.

---

## What it does (one sentence)

Index docs into **Chroma**, for each question take Chroma’s nearest docs, blend **semantic** + **keyword** scores, then ask the chat model using that shortlist only.

---

## Formula used

### Semantic score (from Chroma distance)

Chroma returns **distance** (lower = closer). Hybrid needs a **higher-is-better** score:

```text
semantic = 1 / (1 + distance)
```

| Distance | Semantic |
|----------|----------|
| `0` | `1.0` (perfect) |
| grows | shrinks toward `0` |

### Keyword score (same as keyword lab)

```text
keyword_score = |query_words ∩ text_words| / |query_words|
```

### Combined (hybrid)

```text
combined = 0.7 * semantic + 0.3 * keyword
```

Sort by **combined** descending → keep `top_k`.

---

## Files (on disk)

| File | Role |
|------|------|
| [`main.py`](./main.py) | Load `.env`, index all `*.txt`, chat loop |
| [`hybrid_rag.py`](./hybrid_rag.py) | `build_rag` (index) + `retrieve` (hybrid blend) |
| [`chroma_store.py`](./chroma_store.py) | Persist vectors + **semantic** `search` |
| [`embeddings.py`](./embeddings.py) | `text-embedding-3-small` |
| [`retriever.py`](./retriever.py) | `keyword_score` only |
| [`chunker.py`](./chunker.py) | Word-window split — used only if `chunk=True` |
| [`generator.py`](./generator.py) | Chat answer from shortlist |
| `hybrid_project_flow.md` | This note |

**No** `reranker.py`. **No** in-memory `semantic_search` / `hybrid_search` — deleted on purpose; semantic is Chroma `search`.

---

## Functions — main job

| Function | File | Job |
|----------|------|-----|
| `main()` | `main.py` | Index docs → loop: retrieve → generate |
| `build_rag(text, source, chunk=False)` | `hybrid_rag.py` | Optional chunk → embed → Chroma upsert |
| `retrieve(query, top_k=5)` | `hybrid_rag.py` | Chroma neighbors → blend → print scores → return |
| `add_chunks(chunks)` | `chroma_store.py` | Upsert text + embeddings + metadata |
| `search(query_embedding, top_k)` | `chroma_store.py` | **Semantic search** (vector nearest neighbors) |
| `create_embedding` / `embed_chunks` | `embeddings.py` | String(s) → vector(s) |
| `keyword_score(query, text)` | `retriever.py` | Overlap ratio |
| `create_chunks(...)` | `chunker.py` | Split words into windows (off by default) |
| `generate_answer(query, results)` | `generator.py` | Prompt chat model with context |

---

## Full pipeline map

```text
documents/*.txt
      │
      ▼
 build_rag (chunk=False → one “chunk” per file)
      │
      ▼
 embed_chunks  →  add_chunks (Chroma upsert → ./chroma_db)
      │
      ▼
 user query
      │
      ├─► create_embedding(query)
      │         │
      │         ▼
      │   search(...)     ← semantic (Chroma)
      │         │
      │         ▼
      │   distance → 1/(1+d)
      │         │
      └─► keyword_score(query, text)
                │
                ▼
        combined = 0.7*sem + 0.3*kw
                │
                ▼
        print scores → generate_answer
```

---

## Line-by-line — [`main.py`](./main.py)

### Imports and paths (lines 1–12)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 1–2 | `os`, `Path` | Env checks + document folder paths. |
| 4 | `load_dotenv` | Read `.env` for API key / model. |
| 6–7 | `build_rag`, `retrieve`, `generate_answer` | Index + hybrid retrieve + chat. |
| 9–10 | Two `load_dotenv` calls | First: `AI_LEARNING` root `.env` (`parents[2]`); second: local override. |
| 12 | `DOCUMENTS_DIR` | `../documents/` (chapter shared corpus). |

### `main()` (lines 15–36)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 16–19 | Exit if missing `OPENAI_API_KEY` / `OPENAI_MODEL` | Fail fast before any API / index work. |
| 20–22 | `glob("*.txt")` | Sorted list of knowledge files; exit if empty. |
| 23–27 | Loop paths → `build_rag(..., chunk=False)` | **Whole file** indexed (chunker not used). Print each source. |
| 28 | Ready banner | Hybrid only — reminder there is **no** re-rank. |
| 29–36 | `while True` chat | Read query; `quit`/`exit` breaks; `retrieve` then `generate_answer`; print `RAG :`. |

### Entry (39–40)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 39–40 | `if __name__ == "__main__": main()` | Running `python main.py` starts the app; import does not. |

---

## Line-by-line — [`hybrid_rag.py`](./hybrid_rag.py)

### Imports (lines 1–4)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 1 | `create_chunks` | Only used when `chunk=True`. |
| 2 | `embed_chunks`, `create_embedding` | Index path + query embedding. |
| 3 | `add_chunks`, `search` | Chroma write + **semantic** query (same name as in `chroma_store`). |
| 4 | `keyword_score` | Lexical half of the blend. |

### `build_rag` (lines 7–14)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 8–9 | `if chunk:` | Call `create_chunks` (200 words, overlap 50). |
| 10–11 | `else:` | One dict: full `text`, `source`, `chunk_id=0`. **This is what `main` uses today.** |
| 12 | `embed_chunks(chunks)` | Each piece → OpenAI embedding. |
| 13 | `add_chunks(...)` | Upsert into Chroma. |
| 14 | `return embedded_chunks` | Handy for debugging; `main` ignores the return. |

### `retrieve` (lines 17–50) — the hybrid heart

| Line(s) | Code | What happens |
|---------|------|----------------|
| 19 | `create_embedding(query)` | Query → vector. |
| 20 | `search(query_embedding, top_k)` | **Semantic search** via Chroma. |
| 22–24 | Unpack `documents` / `metadatas` / `distances` | Chroma nests results under `[0]` for the first (only) query. |
| 25–28 | Loop each neighbor | Pull text, metadata, distance. |
| 29 | `semantic = 1 / (1 + distance)` | Distance → higher-is-better score. |
| 30 | `keyword = keyword_score(...)` | Overlap on that neighbor’s text. |
| 31 | `combined = 0.7 * semantic + 0.3 * keyword` | **Only place** the blend lives (no duplicate hybrid helper). |
| 32–39 | Append candidate dict | text, source, chunk_id, three scores. |
| 40–41 | Sort + slice | Best combined first; keep `top_k`. |
| 42–49 | Print | Each line: `semantic=`, `keyword=`, `combined=`. |
| 50 | `return candidates` | Passed to `generate_answer`. |

---

## Line-by-line — [`chroma_store.py`](./chroma_store.py)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 1 | `import chromadb` | Vector DB client. |
| 3 | `PersistentClient(path="./chroma_db")` | Data survives across runs (folder next to cwd). |
| 4 | `get_or_create_collection("documents")` | One named collection for this demo. |
| 7–19 | Build lists in `add_chunks` | `documents`, `embeddings`, `ids` (`source_chunk_id`), `metadatas`. |
| 20–25 | `collection.upsert(...)` | Insert or update by `id` (safe re-runs). |
| 28–32 | `search(...)` | `collection.query` — **this is semantic search** for the project. Returns neighbors + distances. |

---

## Line-by-line — [`embeddings.py`](./embeddings.py)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 7–8 | `load_dotenv` | Same root + local `.env` habit. |
| 10–12 | `OpenAI` client + `text-embedding-3-small` | Embedding model only (chat model is in `generator`). |
| 15–17 | `create_embedding(text)` | One string → one vector list. |
| 20–30 | `embed_chunks(chunks)` | Loop chunks; copy text/source/chunk_id; attach `embedding`. |

---

## Line-by-line — [`retriever.py`](./retriever.py)

Only **`keyword_score`** remains (in-memory semantic/hybrid helpers removed).

| Line(s) | Code | What happens |
|---------|------|----------------|
| 2–3 | Lowercase + `split` → sets | Tokenize query and text. |
| 4–5 | Empty query → `0.0` | Avoid divide-by-zero. |
| 6–7 | Intersection / \|query\| | Fraction of query words found in text. |

Same teaching formula as [`../PROJECT_KEYWORD_SEARCH/keyword_search.md`](../PROJECT_KEYWORD_SEARCH/keyword_search.md).

---

## Line-by-line — [`chunker.py`](./chunker.py)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 2 | `words = text.split()` | Word list for windowing. |
| 6–15 | Sliding window | `chunk_size` words; advance by `chunk_size - overlap`. |
| 9–13 | Each chunk dict | `text`, `source`, `chunk_id`. |

**Today:** unused while `main` passes `chunk=False`. Keep for when you flip chunking on.

---

## Line-by-line — [`generator.py`](./generator.py)

| Line(s) | Code | What happens |
|---------|------|----------------|
| 7–12 | Env + `OPENAI_MODEL` | Chat model name from `.env`. |
| 16 | Join `result["text"]` | Shortlist → one context string. |
| 17–31 | Prompt | Answer **only** from context; no inventing. |
| 32–36 | `chat.completions.create` | User message = prompt; return stripped answer. |

---

## Execution order (what runs when)

1. `python main.py` → load `.env`  
2. For each `documents/*.txt` → `build_rag(..., chunk=False)` → embed → Chroma upsert  
3. Wait for `You :`  
4. `retrieve` → embed query → Chroma `search` → keyword on each neighbor → blend → print three scores  
5. `generate_answer` → print `RAG :`  
6. Repeat until `quit` / `exit`

---

## Console flow (what you see)

```text
Building → indexed each .txt → ready banner → You : → Hybrid candidates → RAG :
```

---

## Sample run output

Captured from a real run of `python main.py` (scores can drift slightly if embeddings change).

```text
python main.py
Building hybrid RAG knowledge base (whole files, chunking off for now)...
  indexed cpp.txt
  indexed kubernetes.txt
  indexed python.txt

Hybrid RAG is ready (no re-rank).

You : what is Python ?

Hybrid candidates (semantic + keyword):
- python.txt  semantic=0.539  keyword=0.500  combined=0.528
- cpp.txt  semantic=0.393  keyword=0.250  combined=0.350
- kubernetes.txt  semantic=0.366  keyword=0.250  combined=0.331

RAG :
Python is a high-level language known for readable syntax and a large standard library.

You : quit
```

### What to notice in this run

| Line | Meaning |
|------|---------|
| `indexed …` three files | Whole-file ingest (`chunk=False`) into Chroma |
| `python.txt` #1 | Highest **combined** — right topic for “what is Python?” |
| `semantic=0.539` | Chroma distance converted with `1/(1+d)` |
| `keyword=0.500` | Half of the query tokens overlapped that file |
| `combined=0.528` | `0.7*0.539 + 0.3*0.500` |
| `RAG :` answer | Generator used the hybrid shortlist as context |

---

## How to run

```bash
pip install chromadb openai python-dotenv
python main.py
```

Needs `OPENAI_API_KEY` and `OPENAI_MODEL` in `.env` (repo `AI_LEARNING` root).

---

## Compare with the labs

| | Keyword lab | Semantic lab | **This hybrid project** |
|---|-------------|--------------|-------------------------|
| Match | Token overlap | Cosine in memory | Chroma distance + keyword |
| Store | None | Python list | `./chroma_db` |
| Answer LLM | No | No | Yes (`generator`) |
| Re-rank | No | No | No (see `RE_RANK_PROJECT`) |

---

## Interview one-liner

**Hybrid RAG** = vector (semantic) neighbors + lexical keyword score, blended (here **0.7 / 0.3**) into one ranking — meaning *and* exact words get a path into the prompt.
