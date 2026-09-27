# LLM benchmarks (beyond GPQA)

Chapter notes for **Souvik’s** AI learning journey (folder `3_LLMs_and_TOKENS`).

**Benchmarks** are standardized tests for models — fixed questions, fixed scoring — so you can compare “how good is model A vs B **at task X**?” No single score means “best AI overall.”

Related: [`gpqa_benchmark.md`](./gpqa_benchmark.md) · [`what_is_an_llm.md`](./what_is_an_llm.md) · [`Features_of_LLM.md`](./Features_of_LLM.md)

---

## Index

| # | Section |
|---|---------|
| 1 | [In plain English](#1-in-plain-english) |
| 2 | [At-a-glance map](#2-at-a-glance-map) |
| 3 | [Knowledge and “general exams”](#3-knowledge-and-general-exams) |
| 4 | [Math](#4-math) |
| 5 | [Coding](#5-coding) |
| 6 | [Science (GPQA)](#6-science-gpqa) |
| 7 | [Reasoning and “AGI-ish” puzzles](#7-reasoning-and-agi-ish-puzzles) |
| 8 | [Instruction following and chat quality](#8-instruction-following-and-chat-quality) |
| 9 | [Long context](#9-long-context) |
| 10 | [Safety and harm](#10-safety-and-harm) |
| 11 | [Limitations of LLM benchmarks](#11-limitations-of-llm-benchmarks) |
| 12 | [Artificial Analysis (independent comparisons)](#12-artificial-analysis-independent-comparisons) |
| 13 | [Vellum LLM Leaderboard](#13-vellum-llm-leaderboard) |
| 14 | [Example snapshots: big models on leaderboards](#14-example-snapshots-big-models-on-leaderboards) |
| 15 | [How to read benchmark claims](#15-how-to-read-benchmark-claims) |
| 16 | [Interview one-liner](#16-interview-one-liner) |
| 17 | [References](#17-references) |

---

## 1. In plain English

Think of benchmarks like **different exam papers**:

1. One tests **memorized school subjects** (MMLU).
2. One tests **word problems** (GSM8K).
3. One tests **writing code that runs** (HumanEval, SWE-bench).
4. One tests **PhD-level science puzzles** ([GPQA](./gpqa_benchmark.md)).

A student who tops the history exam might fail the coding lab. Same for LLMs. Blog posts that shout one number (“92% on X!”) are only meaningful if you know **which exam** and **under what rules** (chain-of-thought, tools, time limit, etc.).

---

## 2. At-a-glance map

| Benchmark | Category | What it mainly tests | Difficulty vibe |
| --------- | -------- | -------------------- | --------------- |
| **MMLU** | Knowledge | ~57 subjects, multiple-choice (STEM, law, medicine, etc.) | Hard general exam |
| **MMLU-Pro** | Knowledge | Harder, fewer trickable MCQ variants | Tougher MMLU |
| **HellaSwag** | Commonsense | Finish a sentence / scenario sensibly | Everyday reasoning |
| **WinoGrande** | Commonsense | Pronoun / world knowledge resolution | Reading + common sense |
| **GSM8K** | Math | Grade-school math **word problems** | Arithmetic + steps |
| **MATH** | Math | Competition-style problems (algebra, geometry, …) | High school olympiad-ish |
| **AIME** | Math | USA Invitational — very hard short-answer math | Elite student math |
| **HumanEval** | Code | Write a Python function from a spec; unit tests pass | Intro coding interview |
| **MBPP** | Code | Mostly basic Python programming tasks | Similar to HumanEval |
| **SWE-bench** | Code / agents | Fix real GitHub issues in real repos | **Real** software job |
| **GPQA** | Science | Graduate-level bio / chem / physics MCQ | See [gpqa_benchmark.md](./gpqa_benchmark.md) |
| **ARC** (ARC-Easy / Challenge) | Reasoning | Science exam-style questions; Challenge = harder | Logic + science facts |
| **ARC-AGI** | Reasoning | Abstract pattern puzzles (anti-memorization goal) | “Fluid intelligence” stress test |
| **BBH** (BIG-Bench Hard) | Reasoning | Subset of hard tasks from BIG-Bench | Mixed reasoning |
| **Humanity’s Last Exam (HLE)** | Mixed | Very hard, broad expert questions (often with tools debate) | “Frontier stress test” |
| **MUSR** | Reasoning | Multi-step soft reasoning stories | Narrative logic |
| **IFEval** | Instruction following | Does output match explicit format rules? | “Do exactly what I said” |
| **MT-Bench** | Chat quality | Multi-turn questions; often judged by stronger models | Helpful chat |
| **LMArena / Chatbot Arena (LMSYS)** | Preference | Humans pick better reply in blind A/B chats → Elo-style rank | See [`lmarena_by_lmsys.md`](./lmarena_by_lmsys.md) |
| **TruthfulQA** | Factuality | Avoid popular **false** beliefs humans also get wrong | Honesty vs myths |
| **ToxiGen / safety suites** | Safety | Toxic or harmful generations | Refusal & harm |
| **Needle in a haystack** | Long context | Find a hidden fact in a long document | Memory span |
| **RULER** | Long context | Broader long-context retrieval & reasoning tasks | Long-document skills |

This is not every benchmark — new ones ship constantly — but these are the names you see most on **model cards** and in **interviews**.

---

## 3. Knowledge and “general exams”

### MMLU (Massive Multitask Language Understanding)

- **What:** Thousands of multiple-choice questions across many academic fields.
- **Layman:** “Did the model absorb a lot of textbook-style knowledge?”
- **Caveat:** MCQ format; scores inflated by clever prompting or training contamination rumors — still useful for **rough** comparison.

### MMLU-Pro

- Harder questions, designed to be less guessable than classic MMLU. Same idea: **broad knowledge**, tougher questions.

### TruthfulQA

- Tests whether the model repeats **common human misconceptions** (“viral myths”).
- **Layman:** “Will it confidently lie because the lie sounds popular?”

---

## 4. Math

### GSM8K (Grade School Math 8K)

- ~8k word problems needing **multi-step** arithmetic.
- **Layman:** Middle-school math story problems — not PhD math, but models must **chain steps** correctly.

### MATH

- Harder competition-style dataset (multiple areas). Step-by-step reasoning matters.

### AIME (American Invitational Mathematics Examination)

- Often reported on **frontier model cards** as a **prestige math** score.
- **Layman:** Math contest for top high school students — far above GSM8K.

---

## 5. Coding

### HumanEval

- Model writes a function; hidden **unit tests** decide pass/fail.
- **Layman:** LeetCode-style **single function** in a sandbox — not the whole codebase.

### MBPP (Mostly Basic Python Problems)

- Similar spirit to HumanEval — basic Python from description.

### SWE-bench (especially **Verified**)

- Model must produce a patch that fixes a real issue in an open-source repo.
- **Layman:** “Can you do an intern’s **real** ticket, not a toy puzzle?”
- Often run with an **agent** loop (read files, run tests, retry). Scores are **not** comparable to HumanEval percentages without reading the setup.

---

## 6. Science (GPQA)

Expert-level science Q&A — covered in depth in [`gpqa_benchmark.md`](./gpqa_benchmark.md) (Diamond subset, scores, leaderboards).

**One-line contrast:** MMLU has a **science section**; GPQA is **only** brutal science written by domain experts.

---

## 7. Reasoning and “AGI-ish” puzzles

### ARC (AI2 Reasoning Challenge)

- Science questions; **Challenge** split is the one quoted on cards.

### ARC-AGI / ARC-AGI-2

- Visual / abstract pattern tasks meant to resist memorization from training data.
- **Layman:** “IQ-test style” grids — tests whether the model **generalizes a rule**, not recalls a meme.

### BIG-Bench Hard (BBH)

- Hand-picked hard tasks from the huge BIG-Bench collection.

### Humanity’s Last Exam (HLE)

- Broad, very difficult questions across domains — newer **frontier bragging** benchmark.
- Scores are still low in absolute terms for many models; read **with tools / without tools** separately.

---

## 8. Instruction following and chat quality

### IFEval

- Verifiable constraints (“reply in JSON”, “use exactly N bullets”, …).
- **Layman:** “Follow the recipe on the label,” not “write a beautiful essay.”

### MT-Bench

- Multi-turn dialog scenarios; scoring often uses **judge models**.
- **Layman:** “Is it a good **assistant** over several back-and-forths?”

### LMArena / Chatbot Arena (LMSYS)

- **Elo-style** ranking from **blind pairwise** human preferences — not a fixed exam score.
- **Layman:** “Crowd votes which chatbot they like” — can differ from exam benchmarks.
- Full note: [`lmarena_by_lmsys.md`](./lmarena_by_lmsys.md).

---

## 9. Long context

### Needle in a haystack

- Hide a random sentence in a very long prompt; ask the model to retrieve it.
- **Layman:** “Did you actually read the whole novel, or only the last page?”

### RULER

- More varied long-context tests than a single needle string.

---

## 10. Safety and harm

Benchmarks vary by lab (ToxiGen, BBQ, red-team suites). They measure **refusal**, **bias**, and **harmful completions** — critical for products, rarely the headline number on a launch slide.

**Layman:** Exam scores say “how smart”; safety evals say “how safe when users are nasty or confused.”

---

## 11. Limitations of LLM benchmarks

Benchmarks are useful **rulers**, not proof of real-world mastery. Understanding their limits is a core **GenAI** concept — as important as knowing benchmark names.

| # | Limitation | Jump |
|---|------------|------|
| 1 | Benchmark contamination | [↓](#111-benchmark-contamination) |
| 2 | Overfitting to benchmarks | [↓](#112-overfitting-to-benchmarks) |
| 3 | Static questions vs dynamic reality | [↓](#113-static-questions-vs-dynamic-reality) |
| 4 | Multiple-choice advantage | [↓](#114-multiple-choice-advantage) |
| 5 | Poor measurement of hallucination | [↓](#115-poor-measurement-of-hallucination) |
| 6 | Reasoning ≠ benchmark score | [↓](#116-reasoning--benchmark-score) |
| 7 | Poor measurement of real-world usefulness | [↓](#117-poor-measurement-of-real-world-usefulness) |
| 8 | Scores are not always comparable | [↓](#118-scores-are-not-always-comparable) |
| 9 | Language and cultural bias | [↓](#119-language-and-cultural-bias) |
| 10 | Benchmark saturation | [↓](#1110-benchmark-saturation) |
| 11 | Benchmark performance ≠ real-world capability | [↓](#1111-the-biggest-distinction) |
| 12 | Static benchmark → agentic evaluation | [↓](#1112-where-evaluation-is-heading) |

### 11.1 Benchmark contamination

1. Test questions may have appeared in the model’s **training data**.
2. The model might **remember** an answer instead of **reasoning** to it.
3. This hurts most on **old, public** datasets that circulated widely on the web.

**Layman:** Studying the exact exam paper before the test inflates your score; it does not prove you learned the subject.

### 11.2 Overfitting to benchmarks

1. Once a benchmark becomes famous, teams can **tune** models and prompts for that test.
2. Scores can rise **without** the model getting equally better at messy, everyday work.

### 11.3 Static questions vs dynamic reality

1. Most benchmarks are **fixed** question sets.
2. Real usage changes constantly — new APIs, new incidents, new policies.
3. A model can ace a frozen test and still stumble on a **novel** problem.

### 11.4 Multiple-choice advantage

1. MMLU, GPQA, and many others are **multiple choice** (often four options).
2. Picking the right letter is **not** the same as deriving an answer from scratch, writing a design doc, or debugging a live system.

### 11.5 Poor measurement of hallucination

1. A model can score highly and still **confidently invent** facts when unsure.
2. Benchmarks rarely capture the full judgment: **answer vs “I don’t know.”**

### 11.6 Reasoning ≠ benchmark score

1. A **correct** final answer does not show **how** the model got there.
2. It might have memorized, pattern-matched, or used a shortcut you would not trust in production.

### 11.7 Poor measurement of real-world usefulness

GPQA might ask: *“Can the model solve this difficult chemistry question?”*

Your job might need: *“Can the model understand my Kubernetes cluster, read logs, find the root cause, propose a fix, write the YAML, validate it, and explain what changed?”*

Those are **different** skills. One high exam score does not guarantee the other.

### 11.8 Scores are not always comparable

1. Different **datasets**, **prompts**, **scoring scripts**, and **reasoning modes**.
2. **95% vs 90%** on two blogs is not automatically “5% better” — the tests may not be the same test.

### 11.9 Language and cultural bias

1. Many benchmarks are **English-first**, academic, and Western-curriculum flavored.
2. Performance can shift a lot by **language**, locale, and domain (legal, medical, local regulations).

### 11.10 Benchmark saturation

1. Older tests (e.g. parts of MMLU) became **too easy** for frontier models.
2. When everyone clusters at **~90–95%+**, the benchmark stops **separating** top models — you need harder or different evals.

### 11.11 The biggest distinction

> **Benchmark performance ≠ real-world capability.**

```text
                 LLM capability
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
   Knowledge       Reasoning      Execution
        │              │              │
       MMLU          GPQA          SWE-bench
       etc.          AIME          agents / tools
        │              │              │
        └──────────────┼──────────────┘
                       ↓
                 Real-world work
```

A model can be strong on GPQA but weak at **operating** software: unreliable tools, shaky long workflows, weak recovery from mistakes, or poor fit for **your** stack.

### 11.12 Where evaluation is heading

| Older default | Newer direction |
| ------------- | --------------- |
| Static benchmark: *“Answer this question.”* | **Dynamic / agentic** eval: *“Here is a real task — investigate, use tools, execute, fix errors, deliver an outcome.”* |

Examples of the shift: **SWE-bench** with agent loops, terminal benchmarks, multi-step sandboxes, and production-style red teaming — still imperfect, but closer to **work**, not just **quizzes**.

**Learning takeaway:** Use benchmarks to **compare models on defined skills**; do not treat leaderboard rank as “will succeed on my job tomorrow.”

---

## 12. Artificial Analysis (independent comparisons)

**[Artificial Analysis — Models](https://artificialanalysis.ai/models)** is a third-party site that compares hundreds of LLMs on **quality, speed, price, and context** using **its own** test runs — not vendor press-release numbers alone.

### 12.1 In plain English

1. Model makers publish cherry-picked benchmark slides.
2. Artificial Analysis re-runs evaluations under **one methodology** so you can compare models more fairly.
3. Think of it as a **consumer reports lab** for LLMs: same ruler, many products.

It does **not** replace your own testing for your job (Kubernetes, your data, your latency budget). It is a strong **starting point** when you ask: *“Which model is smart enough, fast enough, and cheap enough?”*

### 12.2 What you see on the Models page

Main hub: [artificialanalysis.ai/models](https://artificialanalysis.ai/models). Typical dimensions:

| Dimension | What it means (layman) |
| --------- | ---------------------- |
| **Intelligence** | Composite “how capable on hard tasks” score (see Intelligence Index below) |
| **Output speed** | Tokens per second — how fast text streams out |
| **Latency** | Time to **first token** (wait before the answer starts) |
| **Price** | Cost per million tokens (input / output / cache) |
| **Context window** | How much text you can stuff into one prompt |
| **Cost per task** | Dollars to complete one weighted “intelligence” task (ties quality to money) |

You can click a model for detail, filter by provider, and compare **open weights** vs **proprietary** models.

### 12.3 Artificial Analysis Intelligence Index

Instead of a single MMLU or GPQA number, the site publishes an **Intelligence Index** (versioned, e.g. v4.3.x) that **blends multiple evaluations** with fixed weights.

As of the site’s public description, the index can include evals such as:

1. **AA-Briefcase** — agentic “knowledge work” tasks  
2. **GDPval-AA** — realistic professional / work-style tasks  
3. **AutomationBench-AA** — agentic SaaS-style workflows  
4. **Terminal-Bench 4.0** — coding and terminal use  
5. **SciCode** — coding  
6. **Humanity’s Last Exam** — very hard broad reasoning  
7. **GDP.pdf** — professional document reasoning  
8. **CritPt** — physics-style reasoning  
9. **AA-Omniscience** — knowledge + **hallucination** behavior  
10. **AA-LCR** — long-context reasoning  

**Layman read:** This matches the trend in [§11.12](#1112-where-evaluation-is-heading) — less “one exam,” more **agents, tools, terminals, and real-ish work**.

The index **score is not a percentage** like GPQA; it is Artificial Analysis’s own scale. Always read their [methodology](https://artificialanalysis.ai/) / FAQs before treating “58 vs 54” as intuitive gaps.

### 12.4 Other useful corners of the site

1. **[Evaluations hub](https://artificialanalysis.ai/evaluations)** — per-benchmark pages (e.g. [GPQA Diamond](https://artificialanalysis.ai/evaluations/gpqa-diamond)) with independent scores.  
2. **Capability indexes** — slices for finance, legal, medical, engineering, etc.  
3. **Openness Index** — how open the weights and license are (not the same as “smarter”).  
4. **Leaderboards** — ranked views; good for orientation, still not a substitute for your use case.

### 12.5 How to use it without fooling yourself

1. Treat it as **independent replication**, not ground truth for your stack.  
2. Check whether the model row is **reasoning** vs **non-reasoning** (thinking time changes latency and cost).  
3. Pair **intelligence** with **price** and **speed** — a genius model you cannot afford or that is too slow fails in production.  
4. Cross-check one-off benchmarks (GPQA, SWE-bench) on the eval pages when that skill matters most.

**Interview line:** *“Artificial Analysis runs standardized, third-party evals and combines them into an Intelligence Index plus speed/price/context metrics — useful when vendor benchmark slides aren’t comparable.”*

---

## 13. Vellum LLM Leaderboard

**[Vellum — LLM Leaderboard](https://www.vellum.ai/llm-leaderboard)** is a **public dashboard** from [Vellum](https://www.vellum.ai/) (LLM app / eval tooling company). It aggregates **latest reported benchmark scores**, plus **speed, latency, and API pricing**, for many model versions.

### 13.1 In plain English

1. **Artificial Analysis** ( [§12](#12-artificial-analysis-independent-comparisons) ) emphasizes *running* many evals itself under one methodology.  
2. **Vellum’s leaderboard** is closer to a **single page of scoreboards**: “who is winning **which named test** right now?” plus a **model catalog** (context window, $/1M tokens, knowledge cutoff).  
3. Data is described as coming from **model providers and independently run evaluations** — still read the fine print; not every cell uses the same harness.

**Layman:** AA feels like one lab’s full report; Vellum feels like **sports highlights** across many competitions on one screen.

### 13.2 What’s on the page

Hub: [vellum.ai/llm-leaderboard](https://www.vellum.ai/llm-leaderboard). Typical blocks:

| Block | What you get |
| ----- | ------------ |
| **Featured benchmark** | Site picks a headline test (e.g. **Humanity’s Last Exam** as “Best Overall”) with top-5 models |
| **Top models per benchmark** | Separate mini-leaderboards per skill (examples below) |
| **Fastest models** | Throughput (tokens/sec) |
| **Lowest latency** | Time to first token (TTFT) |
| **Cheapest models** | Input / output price per 1M tokens |
| **All models table** | Provider, context, pricing, knowledge cutoff — handy for **product** choices |

Scores and ranks **change** as new models ship; use the live page, not a frozen copy in these notes.

### 13.3 Benchmark columns you’ll recognize

Vellum groups leaders by **task type** — good mapping to [§2](#2-at-a-glance-map) and [§11](#11-limitations-of-llm-benchmarks):

| Vellum label (examples) | Benchmark | Skill |
| ----------------------- | --------- | ----- |
| Best in Reasoning | **GPQA Diamond** | Expert science MCQ — see [`gpqa_benchmark.md`](./gpqa_benchmark.md) |
| Best Overall (featured) | **Humanity’s Last Exam (HLE)** | Very hard, broad frontier stress test |
| Best in Agentic Coding | **SWE-bench** | Real repo bug-fix / agentic coding |
| Best for Work Automations | **AutoBench** | Workflow / automation-style agent tasks |
| Best in Computer Use | **OSWorld** | GUI / desktop-style computer use |
| Best in Browsing | **BrowseComp** | Web browsing / research-style tasks |
| Best in Terminal Use | **Terminal-Bench** | Shell / terminal agent work |

Example snapshot (rankings move): GPQA Diamond leaders have included models in the **mid‑90%** range; HLE “best overall” leaders often sit around **~60–65%** because HLE is much harder in absolute terms — **do not compare those percentages across different benchmarks**.

### 13.4 When Vellum is especially useful

1. **Quick orientation** — “Who’s cited as top on GPQA vs SWE-bench **this month**?”  
2. **Ops planning** — compare **context window** and **$/1M tokens** beside scores.  
3. **Interview prep** — tie benchmark **names** to **real capabilities** (science vs coding vs computer use).

### 13.5 Caveats (read with [§11](#11-limitations-of-llm-benchmarks))

1. **Aggregator ≠ one methodology** — each benchmark may use different prompts, agent scaffolding, or provider-reported numbers.  
2. **Cross-site disagreement** — Vellum’s GPQA top-5 may not match [NeoSignal](https://neosignal.io/) or [Artificial Analysis GPQA Diamond](https://artificialanalysis.ai/evaluations/gpqa-diamond); that usually means **different eval setup**, not that one site is “wrong.”  
3. **Reasoning variants** — same family (e.g. “Opus” with different effort tiers) can appear as separate rows.  
4. **Product context** — Vellum sells LLM workflow tools; the leaderboard is **free marketing + education**, still worth using with healthy skepticism.

### 13.6 Artificial Analysis vs Vellum (one glance)

| | [Artificial Analysis](https://artificialanalysis.ai/models) | [Vellum Leaderboard](https://www.vellum.ai/llm-leaderboard) |
|---|-------------------------------------------------------------|-------------------------------------------------------------|
| **Strength** | Own Intelligence Index, deep methodology, cost-per-task | Many **named** benchmark winners + pricing table on one page |
| **Best for** | Fair cross-model **quality + speed + price** under AA’s harness | Fast **“who leads which benchmark?”** + catalog lookup |
| **Use together** | Yes — cross-check a headline score on both before you bet a production choice |

**Interview line:** *“Vellum’s LLM Leaderboard is a multi-benchmark scoreboard and model catalog; I pair it with independent runners like Artificial Analysis when I need comparable methodology.”*

---

## 14. Example snapshots: big models on leaderboards

The tables below are **real examples** of how frontier and familiar models show up on public boards. **Ranks change** when new models ship — use them to learn **shape and scale**, then open the live sites.

Sources: [Vellum LLM Leaderboard](https://www.vellum.ai/llm-leaderboard), [Artificial Analysis Models](https://artificialanalysis.ai/models), [Artificial Analysis Evaluations](https://artificialanalysis.ai/evaluations), [NeoSignal GPQA Diamond](https://neosignal.io/benchmarks/gpqa-diamond) (independent GPQA run). *Snapshot mindset: late 2025 – 2026 era.*

### 14.1 Vellum — one model family, different “sports”

On [Vellum](https://www.vellum.ai/llm-leaderboard), the **same provider** can lead one column and not another. Example top-5 blocks as published on the site:

**Featured: Humanity’s Last Exam (“Best Overall”)** — absolute scores stay **modest** (~65% for leaders) because HLE is brutally hard:

| Rank | Model | Score |
| ---: | ----- | ----: |
| 1 | Claude Fable 5.1 | 65% |
| 2 | Claude Mythos 5.1 | 65% |
| 3 | Claude Opus 5 | 64.7% |
| 4 | Claude Mythos 5 | 64.5% |
| 5 | Claude Opus 4.8 | 57.9% |

**GPQA Diamond (“Best in Reasoning”)** — leaders cluster **~94–96%** (different test, different scale — do not compare to HLE %):

| Rank | Model | Score |
| ---: | ----- | ----: |
| 1 | Claude Sonnet 5 | 96.2% |
| 2 | GPT-6 Astra | 96% |
| 3 | Claude 3 Opus | 95.4% |
| 4 | GPT-5.6 Sol | 94.6% |
| 5 | Gemini 3.1 Pro | 94.3% |

**SWE-bench (“Agentic Coding”)**:

| Rank | Model | Score |
| ---: | ----- | ----: |
| 1 | GPT-5.6 Sol | 96.2% |
| 2 | Claude Mythos 5 | 95.5% |
| 3 | Claude Fable 5 | 95% |
| 4 | GPT-5.6 Luna | 93% |
| 5 | Claude Opus 4.8 | 88.6% |

**AutoBench (“Work Automations”)** — scores look **low** (~30–49% for leaders); the task is hard and unlike GPQA:

| Rank | Model | Score |
| ---: | ----- | ----: |
| 1 | GLM-5.3-Flash | 48.8% |
| 2 | GPT-6 Astra | 41.4% |
| 3 | Claude Fable 5.1 | 31.4% |
| 4 | Claude Mythos 5.1 | 31.4% |
| 5 | Gemini 3.7 Flash | 30.4% |

**Layman read:** GPT-6 Astra can be **#2 on GPQA** and **#2 on AutoBench**, but AutoBench is still only ~41% — **always read the benchmark name**, not just the number.

**Vellum catalog row (pricing + context)** — how a “big” model looks outside scores:

| Model | Provider | Context | Input $/1M | Output $/1M |
| ----- | -------- | ------- | ---------: | ----------: |
| Claude Opus 5 | Anthropic | 128k | $5 | $25 |
| GPT-5.6 Sol | OpenAI | 128k | $5 | $30 |
| Gemini 3.1 Pro | Google | ~66k | $2 | $12 |
| GPT-4o | OpenAI | 4k* | $2.5 | $10 |
| DeepSeek V4 Pro | DeepSeek | 384k | $0.44 | $0.87 |

\*Vellum’s table lists some legacy rows with smaller context; always confirm on the provider docs.

### 14.2 Artificial Analysis — composite “Intelligence Index”

On [Artificial Analysis Models](https://artificialanalysis.ai/models), **Intelligence Index** blends ~10 evals (see [§12.3](#123-artificial-analysis-intelligence-index)). Scores are on AA’s **own scale** (not 0–100%).

**Top models (from site FAQ, Intelligence Index v4.3.x):**

| Rank | Model | Intelligence Index |
| ---: | ----- | -----------------: |
| 1 | Claude Opus 5.5 (max effort, fallback) | 58 |
| 2 | Claude Opus 5.5 (xhigh effort, fallback) | 56 |
| 3 | Claude Opus 5.5 (high effort, fallback) | 54 |
| 4 | Claude Fable 5.1 (max effort, fallback) | 53 |
| 5 | Claude Fable 5.1 (xhigh effort, fallback) | 53 |

**Best open-weights (same FAQ):**

| Rank | Model | Intelligence Index |
| ---: | ----- | -----------------: |
| 1 | MiMo-V2.6-Pro | 46 |
| 2 | GLM-5.3 (max) | 45 |
| 3 | Kimi K3 (max) | 44 |

**Layman read:** “Opus 5.5 max = 58” means **strong across AA’s blended agentic + reasoning battery**, not “58% on an exam.”

### 14.3 Artificial Analysis — single-eval pages ([evaluations hub](https://artificialanalysis.ai/evaluations))

The [evaluations](https://artificialanalysis.ai/evaluations) index lists **one leaderboard per test**. Examples of what you click through to:

| Evaluation page (AA) | Skill tested | Tie-in to these notes |
| -------------------- | ------------ | --------------------- |
| [GPQA Diamond](https://artificialanalysis.ai/evaluations/gpqa-diamond) | Expert science MCQ | [`gpqa_benchmark.md`](./gpqa_benchmark.md) |
| [Humanity’s Last Exam](https://artificialanalysis.ai/evaluations/humanitys-last-exam) | Frontier Q&A | [§2](#2-at-a-glance-map) HLE row |
| [Terminal-Bench 4.0](https://artificialanalysis.ai/evaluations/terminal-bench-4-0) | Terminal / agentic coding | [§13.3](#133-benchmark-columns-youll-recognize) |
| [SciCode](https://artificialanalysis.ai/evaluations/scicode) | Scientific coding | Coding + science |
| [AA-Omniscience](https://artificialanalysis.ai/evaluations/aa-omniscience) | Knowledge vs hallucination | [§11.5](#115-poor-measurement-of-hallucination) |
| [ITBench-AA](https://artificialanalysis.ai/evaluations/itbench-aa) | K8s incident root cause | Your Kubernetes example in [§11.7](#117-poor-measurement-of-real-world-usefulness) |

Each page shows **charts** (score vs cost, vs speed) for dozens of models — useful when you care about **one** skill.

### 14.4 Same benchmark, different site (GPQA Diamond)

GPQA is a good lesson: **leaderboards disagree** when methodology differs.

**Vellum** (top of “Best in Reasoning”) — see [§14.1](#141-vellum--one-model-family-different-sports): e.g. Claude Sonnet 5 **96.2%**, GPT-6 Astra **96%**.

**NeoSignal** (independent harness, different model list):

| Rank | Model | GPQA Diamond |
| ---: | ----- | -----------: |
| 1 | Gemini 3 Pro | 92.61% |
| 2 | GPT-5.2 | 91.40% |
| 3 | Grok 4 | 87.00% |
| 4 | Claude Opus 4.5 | 86.05% |
| 5 | Gemini 2.5 Pro | 85.29% |

**Neither is “wrong”** — different model variants, prompts, and eval code. For interviews: cite **source + benchmark + split**.

### 14.5 Familiar models — “where the old guard sits” (NeoSignal GPQA)

Helpful anchors when you hear **GPT-4o** or **Llama 405B** in older blog posts:

| Model | GPQA Diamond (NeoSignal) | Rough tier |
| ----- | -------------------------: | ---------- |
| GPT-4o | 49.21% | ~coin flip vs expert science |
| Llama 3.1 405B | 50.92% | similar |
| GPT-4.1 | 68.69% | clearly stronger |
| o1 | 76.77% | reasoning era jump |
| Claude Opus 4.5 | 86.05% | modern frontier band |
| Gemini 3 Pro | 92.61% | top of this table |

**Layman read:** GPQA went from “GPT-4 era ~40–50%” to “frontier ~90%+” in a few years — the benchmark stayed hard; models changed.

### 14.6 One fictional “day in the life” comparison

You are picking a model for **two** tasks:

1. **Hard science Q&A** → check [GPQA Diamond on AA](https://artificialanalysis.ai/evaluations/gpqa-diamond) or [Vellum GPQA column](https://www.vellum.ai/llm-leaderboard).  
2. **Fix real GitHub bugs** → check Vellum **SWE-bench** or AA **Terminal-Bench / SciCode** on [evaluations](https://artificialanalysis.ai/evaluations).  
3. **Budget** → Vellum **cheapest** table or AA **cost per Intelligence Index task** on [models](https://artificialanalysis.ai/models).

If model A wins (1) but loses (2), that is **normal** — matches the diagram in [§11.11](#1111-the-biggest-distinction).

---

## 15. How to read benchmark claims

1. **Which split?** (e.g. GPQA **Diamond** vs full GPQA.)
2. **Tools allowed?** (calculator, code execution, web search.)
3. **Reasoning mode?** (“thinking” models may use many internal tokens.)
4. **Who ran it?** Vendor slide vs [Artificial Analysis Models](https://artificialanalysis.ai/models), [Vellum LLM Leaderboard](https://www.vellum.ai/llm-leaderboard), [Epoch AI](https://epoch.ai/), [NeoSignal](https://neosignal.io/), etc.
5. **Pass@1 vs pass@k** — one attempt vs best of k samples.

---

## 16. Interview one-liner

1. **“LLM benchmarks are task-specific rulers: MMLU for broad knowledge, GSM8K/MATH/AIME for math, HumanEval/SWE-bench for code, GPQA for expert science, ARC-AGI and HLE for hard reasoning stress tests. No single score defines the best model.”**

2. **“Benchmarks can be contaminated, gamed, and saturated; high MCQ scores don’t prove reliable reasoning or real-world execution — that’s why agentic and task-based evals matter.”**

3. **“For third-party comparisons I look at Artificial Analysis: Intelligence Index plus speed, latency, price, and per-eval pages like GPQA Diamond — same methodology across vendors.”**

4. **“Vellum’s leaderboard is a handy multi-benchmark scoreboard (GPQA, SWE-bench, HLE, terminal/computer-use tests) plus pricing and context — I cross-check against independent evals when scores matter.”**

---

## 17. References

1. [GPQA paper](https://arxiv.org/abs/2311.12022) — see also [`gpqa_benchmark.md`](./gpqa_benchmark.md)
2. [MMLU paper](https://arxiv.org/abs/2009.03300)
3. [GSM8K](https://arxiv.org/abs/2110.14168)
4. [HumanEval](https://arxiv.org/abs/2107.03374)
5. [SWE-bench](https://www.swebench.com/)
6. [BIG-Bench](https://arxiv.org/abs/2206.04615)
7. [Artificial Analysis — Models comparison hub](https://artificialanalysis.ai/models)
8. [Artificial Analysis — Evaluations hub](https://artificialanalysis.ai/evaluations)
9. [Vellum — LLM Leaderboard](https://www.vellum.ai/llm-leaderboard)
10. [NeoSignal — GPQA Diamond](https://neosignal.io/benchmarks/gpqa-diamond)
