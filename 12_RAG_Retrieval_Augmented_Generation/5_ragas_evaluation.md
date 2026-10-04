# RAGAS — evaluating RAG pipelines

Chapter notes (folder `12_RAG_Retrieval_Augmented_Generation`).

**RAGAS** = **R**etrieval-**A**ugmented **G**eneration **A**ssessment — open-source framework to evaluate RAG **by component**, not only “did the user like the answer?”

- Site: [ragas.io](https://www.ragas.io/)  
- Use when: you need **metrics** for retrieval vs generation vs end-to-end quality  

**Read order:** `5` of `8` — after [`4_building_rag_challenges.md`](./4_building_rag_challenges.md) (evolution and metrics). Also read [`6_vector_store.md`](./6_vector_store.md) (after note **3** if you follow the embedding → storage path). **Next (classic IR metrics):** [`7_mrr_mean_reciprocal_rank.md`](./7_mrr_mean_reciprocal_rank.md) · [`8_recall_precision_at_k.md`](./8_recall_precision_at_k.md).

---

## Index

| # | Metric | What it measures |
|---|--------|------------------|
| 1 | [Faithfulness](#1-faithfulness) |
| 2 | [Answer relevancy](#2-answer-relevancy) |
| 3 | [Context recall](#3-context-recall) |
| 4 | [Context precision](#4-context-precision) |

Scores are typically on **0–1** (higher better) unless noted.

---

## Why RAGAS?

A RAG pipeline has **two failure modes**:

1. **Retriever** fetched wrong or incomplete context.  
2. **Generator** ignored good context or hallucinated anyway.  

RAGAS gives **separate signals** so you know which part to fix.

---

## 1. Faithfulness

**Question:** Is the **generated answer** factually consistent with the **retrieved context**?

- If claims in the answer can be **inferred from** the provided context → **faithful**.  
- Uses **answer** + **retrieved context**.  
- Scale **0–1**; higher is better.

**Layman:** “Did the model stick to the handout you gave it, or did it make things up?”

---

## 2. Answer relevancy

**Question:** Is the answer **on-topic** for the user’s question?

- Often estimated by generating **synthetic questions** from the answer and comparing similarity to the **original question**.  
- Vague, incomplete, or **padded** answers score lower.  
- Uses **question**, **context**, and **answer**.  
- Higher = more pertinent.

**Layman:** “Did it actually answer what was asked?”

---

## 3. Context recall

**Question:** Did retrieval include the context needed to support the **ground-truth** answer?

- Compare **retrieved context** to an **annotated** (reference) answer.  
- Uses **ground truth** + **retrieved context**.  
- **0–1**; higher = retrieved enough of what was needed.

**Layman:** “Did we fetch the right pages from the library?”

---

## 4. Context precision

**Question:** Are the **relevant** chunks ranked **near the top**?

- All ground-truth-relevant items in context should appear **high** in the ranking.  
- Irrelevant chunks ranked above relevant ones hurt precision.  
- Uses **question**, **ground truth**, and **contexts**.  
- **0–1**; higher = better ranking.

**Layman:** “Is the best evidence at the top of the pile, not buried under noise?”

---

## How this fits your learning path

1. Build a minimal RAG script (retrieve + chat).  
2. Collect a **small golden set** of questions + expected facts.  
3. Run **RAGAS** (or similar) when you change chunk size, embed model, or top-k.  

See [`1_introduction_to_rag.md`](./1_introduction_to_rag.md) for concepts; [`2_rag_architecture_and_workflow.md`](./2_rag_architecture_and_workflow.md) for where each metric applies in the pipeline.

**Related IR metrics:** [`7_mrr_mean_reciprocal_rank.md`](./7_mrr_mean_reciprocal_rank.md) · [`8_recall_precision_at_k.md`](./8_recall_precision_at_k.md).
