# Cross-encoder — `ms-marco-MiniLM-L-6-v2`

Concept note for **`RE_RANK_PROJECT`**. The model used in [`reranker.py`](./reranker.py) is:

`cross-encoder/ms-marco-MiniLM-L-6-v2`

It is a **pre-trained local model that scores how relevant a document is to a query**. In this folder it is the **re-ranking engine** (second pass after hybrid search).

**Links:** [Hugging Face model card](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2) · [Sentence-Transformers cross-encoder docs](https://www.sbert.net/examples/cross_encoder/applications/README.html)

**Project walkthrough:** [`re_rank_project_flow.md`](./re_rank_project_flow.md)

---

## Why it is needed (utility)

Hybrid search builds a **candidate shortlist** (meaning + keywords). That pool can still include weak or off-topic docs.

| Why use it | Plain meaning |
|------------|----------------|
| **Precision after recall** | Hybrid finds; cross-encoder chooses what enters the answer prompt |
| **Joint scoring** | Sees **query + document together** — stronger relevance signal than cosine alone |
| **Leaner prompt** | Keep top **2–3** only → fewer junk tokens for the chat model |
| **Cheap second pass** | Small local MiniLM — **no extra chat-LLM calls** just to score candidates |

**Utility of this model here:** second-stage ranker over the hybrid shortlist in [`reranker.py`](./reranker.py).

---

## Is it accurate?

| Question | Answer for this project |
|----------|-------------------------|
| **Does it jointly score query+doc?** | **Yes.** That is what a cross-encoder does. |
| **Are scores 0–100?** | **No.** Raw **logits** (can be negative). Higher = more relevant. Use **order**, not absolute magnitude. |
| **Is it a chat / understanding model?** | **No.** Passage-ranking specialist (MS MARCO). |
| **Whole-file indexing?** | **Yes today** in this project (`chunk=False`). Long text can hit the **512**-token limit (query + doc). |

**Short verdict:** good teaching / demo re-ranker; relative ranking is what matters.

---

## Breaking down the name

| Name | Meaning |
|------|---------|
| `cross-encoder` | Jointly processes a query and a document |
| `ms-marco` | Trained on Microsoft **MS MARCO** passage ranking |
| `MiniLM` | Compact distilled Transformer |
| `L-6` | Six Transformer layers |
| `v2` | Version 2 |

One job: **“How relevant is this document to the user’s question?”**

---

## Where it fits in the pipeline

Example query: *How do I check running pods in Kubernetes?*

Hybrid might return five candidates. The cross-encoder then scores each pair `(query, doc)` and you keep the winners.

```text
hybrid shortlist (e.g. top 5)
        │
        ▼
 CrossEncoder: for each candidate
   input  = (query, candidate_text)
   output = relevance logit
        │
        ▼
 sort high → low → keep top_k=3
        │
        ▼
 generate_answer (winners only)
```

Illustrative scores (not a real run of this repo):

| Candidate | Score | Rank |
|-----------|-------|------|
| `kubectl get pods` | 8.6 | 1 |
| Troubleshooting pod failures | 5.2 | 2 |
| Kubernetes architecture | 1.8 | 3 |
| Deployment configuration | 0.9 | 4 |
| Cluster networking | -2.1 | 5 |

**Negative scores are normal** — weak match, not a bug.

---

## Cross-encoder vs embedding model

| Feature | OpenAI `text-embedding-3-small` | MiniLM cross-encoder |
|---------|----------------------------------|----------------------|
| Purpose | Generate embeddings | Rank query–document pairs |
| Input | Text alone | Query **+** document together |
| Output | Vector | Relevance score (logit) |
| Used for | Initial semantic retrieval (Chroma / FAISS) | Second-stage re-ranking |
| Encodes independently? | Yes | No — joint |

- **Embedding model** → finds *potentially* relevant docs  
- **Cross-encoder** → decides which of those are *more* relevant  

They **complement** each other. Do **not** replace embeddings with the cross-encoder.

---

## Model facts (this checkpoint)

- ~6 layers, ~22.7M parameters (small)  
- Max sequence length **512** tokens (query + doc together)  
- English passage ranking (MS MARCO)  
- Runs locally on CPU or GPU  
- Scoring does **not** need `OPENAI_API_KEY` (embeddings + answer generation still do)

---

## Minimal example

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

query = "How do I check running pods in Kubernetes?"
candidates = [
    "Kubernetes architecture overview",
    "kubectl get pods lists running pods",
    "Kubernetes deployment configuration",
    "Troubleshooting pod failures",
    "Kubernetes cluster networking",
]

pairs = []
for doc in candidates:
    pairs.append((query, doc))

scores = model.predict(pairs)

ranked = []
for i in range(len(candidates)):
    ranked.append((candidates[i], float(scores[i])))

ranked.sort(key=lambda item: item[1], reverse=True)

for doc, score in ranked[:3]:
    print(f"{score:.4f} - {doc}")
```

Same idea in this folder: [`reranker.py`](./reranker.py) ← [`rerank_rag.py`](./rerank_rag.py) ← [`main.py`](./main.py).

---

## Files

| File | Role |
|------|------|
| [`reranker.py`](./reranker.py) | Loads this model; `rerank()` |
| [`rerank_rag.py`](./rerank_rag.py) | Hybrid shortlist → `rerank` |
| [`re_rank_project_flow.md`](./re_rank_project_flow.md) | Full project notes |
| [`main.py`](./main.py) | Runnable chat loop |

---

## How to run

```bash
pip install sentence-transformers chromadb openai python-dotenv
python main.py
```

First run downloads the MiniLM weights once into the Hugging Face cache.

---

## Interview one-liner

**Cross-encoder re-rank** = second pass that jointly scores `(query, document)` pairs over a hybrid shortlist so only the best few chunks enter the answer prompt — better precision, fewer tokens, without chat-LLM scoring calls.
