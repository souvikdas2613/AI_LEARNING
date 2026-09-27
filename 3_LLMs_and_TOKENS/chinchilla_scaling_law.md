# Chinchilla scaling law

Chapter notes for **Souvik’s** AI learning journey (folder `3_LLMs_and_TOKENS`).

**Chinchilla’s law** (more precisely, the **Chinchilla scaling law**) is a central idea for how LLMs should be sized and trained under a fixed compute budget.

Related: [`what_is_an_llm.md`](./what_is_an_llm.md) · [`Features_of_LLM.md`](./Features_of_LLM.md) · [`what_are_tokens.md`](./what_are_tokens.md)

---

## In plain English

Training an LLM is like **studying for an exam** with a **fixed number of study hours** (your compute budget).

You can spend those hours in two main ways:

1. **Buy a bigger brain** — more **parameters** (more “slots” in the model to store patterns).
2. **Read more books** — more **training tokens** (more text the model actually sees during training).

For years, many teams bet almost everything on (1): *“If we build a gigantic model, it will be smartest.”*

Chinchilla said: **with the same total study time, that is often the wrong trade.** A slightly smaller brain that has **read a lot more** can beat a huge brain that **barely opened the textbooks**.

So the law is not “small models win.” It is:

> **For a given training budget, don’t only grow the model — grow the training data too, in a balanced way.**

The famous **~20 tokens per parameter** rule is just the balance DeepMind measured in their experiments. Think of it as a **recipe ratio** (flour ↔ water), not a magic number that every bakery must use forever.

**Parameters** = how big / complex the model is (billions of adjustable numbers).  
**Tokens** = chunks of text the model trains on (words and pieces of words — see [`what_are_tokens.md`](./what_are_tokens.md)).

**Why you care after training:** A smaller model that learned well is often **cheaper and faster to run** every time someone uses it (inference), even if training cost was similar.

---

## The basic idea

The 2022 DeepMind paper [*Training Compute-Optimal Large Language Models*](https://arxiv.org/abs/2203.15556) found that, for a fixed training-compute budget, you should not just keep making the model bigger.

You need to balance:

**Model parameters ↔ Training data (tokens)**

The paper found that, roughly:

> **Training tokens ≈ 20 × number of model parameters**

**Layman read on the table below:** each row is “if you build *this* sized model, Chinchilla-style training means showing it about *this much* text — not a thin slice of the internet.”

| Model | Approx. parameters | Chinchilla-style training data |
| ----- | -----------------: | -----------------------------: |
| 1B    |          1 billion |                    ~20B tokens |
| 7B    |          7 billion |                   ~140B tokens |
| 13B   |         13 billion |                   ~260B tokens |
| 70B   |         70 billion |                   ~1.4T tokens |

The actual Chinchilla model was **70B parameters trained on about 1.3T tokens**, while Gopher had **280B parameters** but substantially less training data. Despite being 4× smaller, Chinchilla achieved better results at roughly the same training compute. See [Google DeepMind’s summary](https://deepmind.google/blog/an-empirical-analysis-of-compute-optimal-large-language-model-training/).

**Simple comparison:**

| | Gopher-style mistake | Chinchilla-style balance |
|---|----------------------|---------------------------|
| Model | Very large | Moderately large |
| Data | Not enough for that size | Much more text |
| Result | Like a huge empty warehouse | Like a smaller warehouse, well stocked |

---

## Why was this important?

Before Chinchilla, the industry was heavily focused on:

**“Make the model bigger → it becomes smarter.”**

That sounds intuitive — like assuming a bigger hard drive automatically means better software. It does not. The software (what the model **learned**) depends on **how much quality experience** it had.

Chinchilla showed that a huge model can be **undertrained**: lots of capacity, not enough examples to fill it properly. The model can memorize some patterns but generalize worse than a better-fed smaller one.

For example:

- **280B model + too little data** ❌ — expensive to run, still “hungry” for more learning  
- **70B model + much more data** ✅ — often smarter on benchmarks, cheaper per chat at run time  

That is the key insight: **smart is not the same as big.** Smart is **big enough for the amount of training you can afford**, with **enough data** to use that size well.

---

## One important modern caveat

Do not interpret **20 tokens per parameter** as a universal law for every modern LLM.

It is a **compute-optimal pretraining result from the Chinchilla setup** — the best split *they* found when the goal was “use this GPU budget well during training.” Real products also care about **speed, price per question, and hardware**, so teams sometimes train **longer on more tokens** than that ratio, or choose different sizes on purpose.

**Plain English:** Chinchilla answered “how should we spend our **training** dollars?” Later work also asks “how should we spend our **every-user-asks-a-question** dollars?” Those answers can differ.

See also [Scaling Inference-Efficient Language Models](https://openreview.net/pdf?id=wslytZ28Ms) on OpenReview.

For an interview, a clean phrasing:

> **“Chinchilla scaling says that, under a fixed training-compute budget, model size and training data should be scaled together. The original study found an approximate optimum of 20 training tokens per parameter.”**

---

## References

- [Training Compute-Optimal Large Language Models (arXiv)](https://arxiv.org/abs/2203.15556)
- [An empirical analysis of compute-optimal large language model training — Google DeepMind](https://deepmind.google/blog/an-empirical-analysis-of-compute-optimal-large-language-model-training/)
