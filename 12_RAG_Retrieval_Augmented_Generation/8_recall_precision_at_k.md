# Recall@K and Precision@K

Chapter notes (folder `12_RAG_Retrieval_Augmented_Generation`).

**Recall@K** and **Precision@K** are metrics used to evaluate **search and information-retrieval systems** — especially the **top K retrieved results**.

**Read order:** `8` of `8` — after [`7_mrr_mean_reciprocal_rank.md`](./7_mrr_mean_reciprocal_rank.md) — metrics that look at *all* relevant hits in the top K, not just the first one.

---

## Simple idea

Think of them as answering two different questions about the **top K retrieved results**.

| Metric          | Question                                      |
| --------------- | --------------------------------------------- |
| **Recall@K**    | Did I **find most of the relevant stuff**?    |
| **Precision@K** | Are the things I **found actually relevant**? |
| **MRR**         | How **high was the first relevant result**?   |

---

## Example

Suppose there are **5 relevant documents** in the entire database.

Your RAG system retrieves the **top 4**:

1. Relevant ✅
2. Irrelevant ❌
3. Relevant ✅
4. Irrelevant ❌

So among the top 4, you found **2 relevant documents**.

---

## Recall@K

> **"Of all the relevant documents that existed, how many did I retrieve?"**

$$
Recall@K = \frac{\text{Relevant documents retrieved in top K}}{\text{Total relevant documents}}
$$

Here:

$$
Recall@4 = \frac{2}{5} = \boxed{0.40}
$$

So **40% recall**.

---

## Precision@K

> **"Of the K documents I retrieved, how many were actually relevant?"**

$$
Precision@K = \frac{\text{Relevant documents retrieved in top K}}{K}
$$

Here:

$$
Precision@4 = \frac{2}{4} = \boxed{0.50}
$$

So **50% precision**.

---

## In RAG / LLMs

Imagine your vector store has **10 relevant chunks** for a question.

Your retriever returns top-5:

1. Relevant ✅
2. Relevant ✅
3. Irrelevant ❌
4. Irrelevant ❌
5. Irrelevant ❌

Then:

$$
Recall@5 = 2/10 = 20\%
$$

$$
Precision@5 = 2/5 = 40\%
$$

So your retriever is finding **some relevant information**, but it's missing a lot of relevant chunks.

---

## One important distinction

Recall@K requires knowing the **total number of relevant documents/chunks** (the ground truth). That's why RAG evaluation datasets usually need annotated relevant documents.

MRR cares about the **first relevant result only**. Recall@K and Precision@K look at **how many** relevant items landed in the top K.

**Related:** [`7_mrr_mean_reciprocal_rank.md`](./7_mrr_mean_reciprocal_rank.md) · [`5_ragas_evaluation.md`](./5_ragas_evaluation.md) — Faithfulness, Answer relevancy, Context recall, Context precision.
