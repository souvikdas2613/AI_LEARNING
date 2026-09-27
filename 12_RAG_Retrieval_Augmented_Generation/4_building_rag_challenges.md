# Challenges building RAG applications

Chapter notes (folder `12_RAG_Retrieval_Augmented_Generation`).

**Read order:** `4` of `6` — after notes **1–3**.

Related: [`1_introduction_to_rag.md`](./1_introduction_to_rag.md) · [`5_ragas_evaluation.md`](./5_ragas_evaluation.md)

---

## Index

| # | Challenge | Summary |
|---|-----------|---------|
| 1 | [Updating external data](#1-updating-external-data) |
| 2 | [Scalability](#2-scalability) |
| 3 | [Relevance and accuracy](#3-relevance-and-accuracy) |
| 4 | [Bias and fairness](#4-bias-and-fairness) |
| 5 | [Evolution and metrics](#5-evolution-and-metrics) |
| 6 | [Managed knowledge bases (optional)](#6-managed-knowledge-bases-optional) |

---

## 1. Updating external data

Business docs, policies, and catalogs **change**. If the vector index is stale, RAG answers from **old** chunks.

**Mitigations:** scheduled re-ingest, event-driven updates when files change, versioning, clear “as of” dates in metadata.

---

## 2. Scalability

More documents → larger indexes → slower or costlier search; more chunks in context → **token cost** and **latency**.

**Mitigations:** sharding, metadata filters (search only HR vs only engineering), smaller top-k, re-ranking, caching frequent queries.

---

## 3. Relevance and accuracy

Bad retrieval poisons the prompt: right-sounding answers, wrong facts.

**Mitigations:** better chunking, hybrid search, re-rankers, human eval sets, frameworks like **RAGAS** (see [`5_ragas_evaluation.md`](./5_ragas_evaluation.md)).

---

## 4. Bias and fairness

Training data, document corpus, and retrieval ranking can **favor** some topics or groups.

**Mitigations:** diverse sources, audit retrieved chunks, policy filters, monitoring in production.

---

## 5. Evolution and metrics

RAG is not “ship once.” You need **ongoing measurement**: retrieval quality, answer faithfulness, user feedback, regression when you change embed model or chunk size.

**Mitigations:** labeled Q&A sets, component metrics (retriever vs generator), A/B tests on prompts and top-k.

---

## 6. Managed knowledge bases (optional)

Cloud vendors offer managed RAG-style stacks so teams spend less time on ingest plumbing.

Example: **Amazon Bedrock Knowledge Bases** — connects **private data sources** to retrieval + generation for more relevant, customized responses (AWS-specific; same RAG ideas apply on other clouds).

Conceptually: you still have **sources → index → retrieve → generate**; the platform handles parts of ingestion and wiring.
