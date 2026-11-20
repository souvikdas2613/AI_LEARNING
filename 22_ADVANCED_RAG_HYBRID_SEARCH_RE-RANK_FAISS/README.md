# Advanced RAG — hybrid search, re-rank, FAISS

Chapter notes for **Souvik’s** AI learning journey (folder `22_ADVANCED_RAG_HYBRID_SEARCH_RE-RANK_FAISS`).

**Topic 12** introduced RAG — embeddings, cosine similarity, vector stores, and evaluation metrics.  
**Topic 13** built a LangChain **Chroma** index under `13_LANGCHAIN/vector_db/`.  
**This chapter** adds **FAISS**, **hybrid retrieval**, and **re-ranking** as separate project folders.

Related earlier chapters:

- RAG path — [`12_RAG_Retrieval_Augmented_Generation/`](../12_RAG_Retrieval_Augmented_Generation/)
- LangChain embeddings + Chroma — [`10_embeddings_and_vector_store.md`](../13_LANGCHAIN/10_embeddings_and_vector_store.md)
- Semantic memory — [`1_introduction_to_memory_engineering.md`](../21_MEMORY_ENGINEERING/1_introduction_to_memory_engineering.md)

---

## Read order

| # | File | Topic |
|---|------|--------|
| 1 | [`1_what_is_faiss.md`](./1_what_is_faiss.md) · [`faiss_demo.py`](./faiss_demo.py) · [`faiss_demo.md`](./faiss_demo.md) | FAISS concept + demo + explained notes |
| 1b | [`FAISS_PROJECT/`](./FAISS_PROJECT/) (`rag.py` + `knowledge/`) | Same shape as topic-12 naive `rag.py` — **FAISS** replaces the cosine loop |
| 2 | [`PROJECT_SEMANTIC_SEARCH/`](./PROJECT_SEMANTIC_SEARCH/) | **Semantic** only |
| 3 | [`PROJECT_KEYWORD_SEARCH/`](./PROJECT_KEYWORD_SEARCH/) | **Keyword** only |
| 4 | [`HYBRID_PROJECT/`](./HYBRID_PROJECT/) | **Hybrid** — Chroma + 0.7 semantic + 0.3 keyword (no re-rank) |
| 5 | [`RE_RANK_PROJECT/`](./RE_RANK_PROJECT/) | **Re-rank** — hybrid shortlist → LLM score → top 3 → answer |

**Documents:** [`documents/`](./documents/) — `kubernetes.txt`, `python.txt`, `cpp.txt` (shared by hybrid + re-rank).

| Folder | Keep (core) | Not here |
|--------|-------------|----------|
| `HYBRID_PROJECT/` | `main` · `hybrid_rag` · `retriever` · `embeddings` · `chroma_store` · `chunker` · `generator` | no `reranker` |
| `RE_RANK_PROJECT/` | `main` · `rerank_rag` · `reranker` · `generator` · slim `retriever` (`keyword_score` only) · shared store/embed/chunk | no lab-style `semantic_search` / `hybrid_search` helpers |

**Suggested path:** semantic lab → keyword lab → [`HYBRID_PROJECT/`](./HYBRID_PROJECT/) → [`RE_RANK_PROJECT/`](./RE_RANK_PROJECT/).

Start here if you are new to FAISS: [`1_what_is_faiss.md`](./1_what_is_faiss.md).  
Hybrid notes: [`HYBRID_PROJECT/hybrid_project_flow.md`](./HYBRID_PROJECT/hybrid_project_flow.md).  
Re-rank notes: [`RE_RANK_PROJECT/re_rank_project_flow.md`](./RE_RANK_PROJECT/re_rank_project_flow.md).
