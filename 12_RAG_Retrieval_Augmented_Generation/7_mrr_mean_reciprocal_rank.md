# Mean Reciprocal Rank (MRR)

Chapter notes (folder `12_RAG_Retrieval_Augmented_Generation`).

**MRR** is a metric used to evaluate **search, recommendation, and information-retrieval systems**.

**Read order:** `7` of `8` — after [`5_ragas_evaluation.md`](./5_ragas_evaluation.md) — another way to score **retrieval quality** (where the first correct hit lands). **Next:** [`8_recall_precision_at_k.md`](./8_recall_precision_at_k.md).

---

## Simple idea

MRR asks:

> **"How high in the ranked results did the first correct answer appear?"**

For each query:

$$
RR = \frac{1}{\text{rank of first relevant result}}
$$

Then:

$$
\boxed{MRR = \frac{1}{N}\sum_{i=1}^{N}\frac{1}{rank_i}}
$$

---

## Example

Suppose you have 4 searches:

| Query | First relevant result | Reciprocal Rank |
| ----- | --------------------: | --------------: |
| Q1    |                   1st |  1/1 = **1.00** |
| Q2    |                   2nd |  1/2 = **0.50** |
| Q3    |                   4th |  1/4 = **0.25** |
| Q4    |                   5th |  1/5 = **0.20** |

So:

$$
MRR = \frac{1+0.5+0.25+0.2}{4}
=\boxed{0.4875}
$$

So **MRR = 0.4875**.

---

## Why reciprocal?

Because being correct at the top is much better:

* Rank 1 → **1.00**
* Rank 2 → **0.50**
* Rank 3 → **0.33**
* Rank 10 → **0.10**

So MRR strongly rewards systems that put the correct result **near the top**.

---

## In RAG / LLMs

Imagine asking:

> "What is the refund policy?"

Your vector database retrieves 5 documents:

1. Product overview ❌
2. Pricing ❌
3. **Refund policy ✅**
4. FAQ ❌
5. Contact information ❌

The first relevant document is at **rank 3**.

$$
RR = 1/3 = 0.333
$$

Across hundreds of questions, averaging those reciprocal ranks gives your **MRR**.

---

## One important distinction

MRR cares about the **first relevant result only**.

If you need to evaluate *all* relevant documents in the ranking, metrics such as **Recall@K, Precision@K, MAP, or NDCG** are often more appropriate.

**Related:** [`8_recall_precision_at_k.md`](./8_recall_precision_at_k.md) — Recall@K & Precision@K · [`5_ragas_evaluation.md`](./5_ragas_evaluation.md) — Faithfulness, Answer relevancy, Context recall, Context precision.
