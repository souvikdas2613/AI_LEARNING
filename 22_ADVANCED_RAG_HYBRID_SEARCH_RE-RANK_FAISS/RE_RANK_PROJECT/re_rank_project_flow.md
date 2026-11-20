# Re-rank project — hybrid shortlist → LLM re-rank → lean prompt

Folder: `RE_RANK_PROJECT/` (chapter `22_ADVANCED_RAG_HYBRID_SEARCH_RE-RANK_FAISS`).

**This folder = re-rank focus.** Hybrid still builds the shortlist; then `reranker.py` scores each candidate 0–100 and keeps top 3 for generation.

Do hybrid alone first: [`../HYBRID_PROJECT/`](../HYBRID_PROJECT/).

---

## Files (on disk)

| File | Role |
|------|------|
| `main.py` | Build index + chat loop |
| `rerank_rag.py` | `build_rag` + `retrieve` (hybrid → `rerank`) |
| `reranker.py` | LLM relevance 0–100 per candidate; keep top 3 |
| `generator.py` | Answer from **winners only** |
| `retriever.py` | `keyword_score` only (for hybrid blend) |
| `embeddings.py` | `text-embedding-3-small` |
| `chroma_store.py` | Persist / query Chroma (`./chroma_db`) |
| `chunker.py` | Word-window chunks (`chunk=True` later) |
| `re_rank_project_flow.md` | This note |

**Knowledge:** chapter [`../documents/`](../documents/).

---

## Wired vs unused

| Piece | Used by `main.py`? |
|-------|---------------------|
| Hybrid shortlist in `rerank_rag.retrieve` | Yes |
| `reranker.rerank` | Yes |
| `generator.generate_answer` | Yes |
| `retriever.keyword_score` | Yes |
| `chunker` (`chunk=False` today) | Imported; path ready when you flip `chunk=True` |

No separate semantic/hybrid lab helpers here. Semantic = Chroma `search`; keyword = `keyword_score`. Labs: `PROJECT_SEMANTIC_SEARCH` / `PROJECT_KEYWORD_SEARCH`.

---

## Flow

1. Hybrid candidates (Chroma + 0.7 / 0.3) — printed as **Candidates**  
2. `rerank(query, candidates, top_k=3)` — printed as **Ranking**  
3. `generate_answer` uses only the re-ranked top 3  

**Talk line:** Hybrid finds. Re-rank chooses what enters the prompt.

---

## How to run

```bash
pip install chromadb openai python-dotenv
python main.py
```

Needs `OPENAI_API_KEY` and `OPENAI_MODEL` in `.env`.
