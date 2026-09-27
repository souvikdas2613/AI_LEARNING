# GPQA benchmark

Chapter notes for **Souvik’s** AI learning journey (folder `3_LLMs_and_TOKENS`).

When people say an LLM is **“GPQA-level”** or has **strong GPQA scores**, they are talking about a specific **hard science Q&A benchmark** — not a model name or a training law.

Related: [`what_is_an_llm.md`](./what_is_an_llm.md) · [`Features_of_LLM.md`](./Features_of_LLM.md) · [`chinchilla_scaling_law.md`](./chinchilla_scaling_law.md) · [`llm_benchmarks.md`](./llm_benchmarks.md) (full benchmark map)

---

## In plain English

Most quiz apps check whether you **remember facts** (“Who wrote Hamlet?”). GPQA is closer to **“Can you think like a PhD student under time pressure?”**

Questions are in **biology, physics, chemistry**, and related science. They are written so that:

- A smart non-expert will often get them wrong.
- Even **domain experts** find many of them hard.
- **Googling the question** usually does not hand you the answer — that is what **“Google-Proof”** means in the name.

So a high GPQA score suggests the model can **reason through expert science problems**, not just repeat things it saw in training. It is one signal of **depth**, not the only measure of a good model.

**GPQA** = **Graduate-Level Google-Proof Q&A**.

---

## What GPQA measures

GPQA is a benchmark designed to test whether an LLM can answer **very difficult, expert-level questions** in areas such as:

- Biology
- Physics
- Chemistry
- Other scientific domains

The key distinction is that GPQA questions are intended to be difficult **even for people who have strong domain knowledge**, and they are designed so that simply searching Google is not enough.

---

## GPQA vs other LLM benchmarks

Benchmarks answer different questions. Comparing models on only one score is like judging an athlete on only one sport.

| Benchmark | What it mainly tests |
| --------- | -------------------- |
| MMLU | Broad academic / general knowledge (many subjects, mostly multiple-choice) |
| GSM8K | Grade-school **math word problems** (step-by-step arithmetic reasoning) |
| HumanEval | **Coding** — can the model write functions that pass tests? |
| **GPQA** | **Expert-level scientific reasoning** (hard science Q&A) |
| AIME | **Competition-level mathematics** (very hard math for top students) |
| SWE-bench | **Real-world software engineering** (fix issues in actual code repos) |

**Layman takeaway:** MMLU is “did you study many subjects?” GPQA is “can you handle **graduate-level science puzzles** where lookup tricks fail?”

For a longer list (math, code, reasoning, chat, long context, safety), see [`llm_benchmarks.md`](./llm_benchmarks.md).

---

## GPQA Diamond

There is a harder slice called **GPQA Diamond** — the **toughest subset**, with **198 questions**. When a blog post or model card highlights **GPQA Diamond**, they are pointing at the **strictest** part of the benchmark, not the full pool.

So when someone says:

> **“This LLM has strong GPQA performance”**

they generally mean it shows strong **deep reasoning and expert scientific problem-solving**, not merely a large memorized knowledge base.

---

## Who scores what on GPQA Diamond?

GPQA Diamond is **multiple choice (four options)**. Blind guessing is about **25%**. A score in the **30–40%** range once meant “frontier AI”; by **2025–2026**, top systems are often **above 85%** on published leaderboards — which shows how fast models improved, not that the benchmark got easier.

**Scores are not apples-to-apples unless the setup matches.** The same model can look different if the run uses chain-of-thought, many sampled answers (“majority vote”), extended **reasoning** modes, or a third-party harness with stricter answer formatting. Treat every number as **“X% under method Y.”**

### Human and paper anchors (why the benchmark is hard)

| Who / what | GPQA Diamond accuracy | Source |
| ---------- | --------------------: | ------ |
| Random guess (4 choices) | ~25% | Design of benchmark |
| Skilled non-experts (web allowed, ~30+ min) | ~34% | [GPQA paper](https://arxiv.org/abs/2311.12022) |
| Domain PhD experts | ~65% (up to ~74% after fixing expert mistakes) | GPQA paper |
| Strong **GPT-4-class** baseline (2023 paper) | ~39% | GPQA paper |
| PhD experts (OpenAI o1-era human eval, cited by Epoch) | ~70% | [Epoch AI — GPQA Diamond](https://epoch.ai/benchmarks/gpqa-diamond) |

**Layman read:** Experts beat smart Googlers by a lot; early GPT-4 was well below experts; today’s best models are **far above** early GPT-4 and, on many reports, **above single-expert accuracy** — but that still does not mean they are infallible on real research.

### Vendor-reported frontier scores (launch / blog comparisons)

These come from **model makers’** benchmark slides (often best reasoning tier). Useful for marketing comparisons; confirm with independent evals when you can.

| Model (as reported) | GPQA Diamond | Notes |
| ------------------- | -----------: | ----- |
| Gemini 3 Deep Think | 93.8% | Google frontier reasoning mode |
| GPT-5.2 Pro | 93.2% | OpenAI Dec 2025 release |
| GPT-5.2 Thinking | 92.4% | OpenAI Dec 2025 release |
| Gemini 3 Pro | 91.9% | Google Nov 2025 |
| Claude Opus 4.5 | ~87% | Anthropic Nov 2025 |

Compiled from [R&D World — GPT-5.2 vs Gemini 3 vs Claude Opus 4.5](https://www.rdworldonline.com/how-gpt-5-2-stacks-up-against-gemini-3-0-and-claude-opus-4-5/) (Dec 2025; vendor-reported).

### Anthropic model card snapshot (Claude 3 generation)

Official **Claude 3** family numbers on **GPQA (Diamond)**, from Anthropic’s model card addendum (prompting varies by row):

| Model | Reported accuracy |
| ----- | ----------------: |
| Claude 3.5 Sonnet | 59.4% (0-shot) · 67.2% (5-shot CoT) |
| Claude 3 Opus | 50.4% · 59.5% |
| Claude 3 Sonnet | 40.4% · 46.3% |
| GPT-4o (cited by Anthropic) | 53.6% |

[Claude 3.5 Sonnet Model Card Addendum (PDF)](https://www-cdn.anthropic.com/fed9cc193a14b84131812372d8d5857f8f304c52/Model_Card_Claude_3_Addendum.pdf)

### Independent leaderboard snapshot (NeoSignal)

[NeoSignal GPQA Diamond leaderboard](https://neosignal.io/benchmarks/gpqa-diamond) aggregates many models under **one** harness (helpful for relative ranking). Snapshot below — **check the live page** for updates.

**Top of the table (2025–2026 era):**

| Rank | Model | Score |
| ---: | ----- | ----: |
| 1 | Gemini 3 Pro | 92.6% |
| 2 | GPT-5.2 | 91.4% |
| 3 | Grok 4 | 87.0% |
| 4 | Claude Opus 4.5 | 86.1% |
| 5 | Gemini 2.5 Pro (Jun 2025) | 85.3% |
| 6 | Kimi K2 thinking | 84.2% |
| 7 | DeepSeek V3 | 83.4% |
| 8 | Claude Sonnet 4.5 | 82.3% |
| 9 | OpenAI o3 | 81.8% |
| 10 | Qwen3 235B | 80.1% |

**Mid-tier anchors (same leaderboard):**

| Model | Score |
| ----- | ----: |
| OpenAI o1 | 76.8% |
| GPT-4.1 | 68.7% |
| Llama 4 Maverick | 67.0% |
| Mistral Large | 59.5% |
| Llama 3.1 405B | 50.9% |
| GPT-4o | 49.2% |
| Claude 3 Opus | 47.2% |
| GPT-4 Turbo | 46.6% |
| GPT-4o mini | 37.7% |
| GPT-3.5 turbo | 28.0% |

Another independent source is [Artificial Analysis — GPQA Diamond](https://artificialanalysis.ai/evaluations/gpqa-diamond) (methodology on that site; scores move as new models ship).

**Quick pattern:** OpenAI, Google, Anthropic, xAI, DeepSeek, and Qwen **frontier** models cluster **high** on Diamond today; **older chat models** (GPT-4o, Llama 3.1 405B) sit **near ~50%** on the same aggregator — roughly “strong general model, not specialist scientist” territory.

---

## How this fits your LLM mental model

- **Training scale** (parameters, tokens, Chinchilla-style balance) affects *how capable the base model can become* — see [`chinchilla_scaling_law.md`](./chinchilla_scaling_law.md).
- **GPQA** is a *ruler* used **after** training (and often after extra tuning) to see how well the model does on one type of hard task.

A model can score well on easy trivia and still struggle on GPQA. The reverse is also possible in theory, but in practice teams brag about GPQA when they want to claim **serious science reasoning**, not just chat fluency.

If you see **“Chinchilla’s Law → GPQA level”** in a slide or post, that is usually shorthand for a chain like: *train more efficiently (data + size) → better capabilities → better benchmark numbers including GPQA.* The law does not define GPQA; it is about **how to spend training compute**.

---

## Interview one-liner

> **“GPQA is a graduate-level, Google-proof science Q&A benchmark. High scores suggest strong expert scientific reasoning, not just broad knowledge — GPQA Diamond is the hardest 198-question subset.”**

---

## References

- [GPQA: A Graduate-Level Google-Proof Q&A Benchmark (arXiv)](https://arxiv.org/abs/2311.12022)
- [GPQA Diamond — NeoSignal leaderboard](https://neosignal.io/benchmarks/gpqa-diamond)
- [GPQA Diamond — Artificial Analysis](https://artificialanalysis.ai/evaluations/gpqa-diamond)
- [GPQA Diamond — Epoch AI (methodology & human baselines)](https://epoch.ai/benchmarks/gpqa-diamond)
- [Claude 3.5 Sonnet Model Card Addendum (GPQA table)](https://www-cdn.anthropic.com/fed9cc193a14b84131812372d8d5857f8f304c52/Model_Card_Claude_3_Addendum.pdf)
- [GPT-5.2 vs Gemini 3 vs Claude Opus 4.5 — R&D World](https://www.rdworldonline.com/how-gpt-5-2-stacks-up-against-gemini-3-0-and-claude-opus-4-5/)

*Scores section last reviewed: September 2026 — leaderboards change frequently.*
