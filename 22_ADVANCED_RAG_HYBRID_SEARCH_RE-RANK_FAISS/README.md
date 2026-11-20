# Advanced RAG — hybrid search, re-rank, FAISS

Chapter notes for **Souvik’s** AI learning journey (folder `22_ADVANCED_RAG_HYBRID_SEARCH_RE-RANK_FAISS`).

**Topic 12** introduced RAG — embeddings, cosine similarity, vector stores, and evaluation metrics.  
**Topic 13** built a LangChain **Chroma** index under `13_LANGCHAIN/vector_db/`.  
**This chapter** adds **FAISS** concepts, **hybrid retrieval**, **re-ranking**, and a **`project/`** pipeline that uses **Chroma + OpenAI** end to end.

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
| 2 | [`PROJECT_SEMANTIC_SEARCH/`](./PROJECT_SEMANTIC_SEARCH/) | One file — **semantic** only (`semantic_search.py` + `.md`, cosine + embeddings) |
| 3 | [`PROJECT_KEYWORD_SEARCH/`](./PROJECT_KEYWORD_SEARCH/) | One file — **keyword** only (`keyword_search.py` + `.md`, word overlap) |
| 4 | [`project/advanced_rag_project_flow.md`](./project/advanced_rag_project_flow.md) | **Combined** — Chroma + hybrid (0.7 semantic + 0.3 keyword) + rerank + answer |

**Documents:** [`documents/`](./documents/) — `kubernetes.txt`, `python.txt`, `cpp.txt` (whole files; chunking later).

**Suggested path:** semantic lab → keyword lab → compare → full [`project/`](./project/) (`python main.py`).

Start here if you are new to FAISS: [`1_what_is_faiss.md`](./1_what_is_faiss.md).  
Start here for the full pipeline: [`project/advanced_rag_project_flow.md`](./project/advanced_rag_project_flow.md).