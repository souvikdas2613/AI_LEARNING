# Features of an LLM

Chapter notes for **Souvik’s** AI learning journey (folder `3_LLMs_and_TOKENS`).

**Characteristics** that make an LLM powerful — parameters, tokens, data, architecture — not a list of chat tasks.

Related: [`what_is_an_llm.md`](./what_is_an_llm.md) · [`what_are_tokens.md`](./what_are_tokens.md)

---

## Index

| # | Characteristic |
|---|----------------|
| 1 | [What “powerful” means](#1-what-powerful-means) |
| 2 | [Scale of training data](#2-scale-of-training-data) |
| 3 | [Parameters (weights)](#3-parameters-weights) |
| 4 | [Tokens (how it reads language)](#4-tokens-how-it-reads-language) |
| 5 | [Transformer / attention](#5-transformer--attention) |
| 6 | [Context window](#6-context-window) |
| 7 | [How it was tuned (base vs instruct vs chat)](#7-how-it-was-tuned-base-vs-instruct-vs-chat) |
| 8 | [Compute at train and at run time](#8-compute-at-train-and-at-run-time) |
| 9 | [What does *not* make it powerful by itself](#9-what-does-not-make-it-powerful-by-itself) |
| 10 | [One picture](#10-one-picture) |

---

## 1. What “powerful” means

A **powerful LLM** is not “it can chat.” Almost every LLM can chat.

Power here means:

- better **next-token** guesses on hard language  
- more **knowledge patterns** from training  
- can use **longer prompts** without falling apart  
- still usable (speed, cost, hardware)

Those come from **characteristics of the model**, not from a fancy UI.

---

## 2. Scale of training data

Called **large** because it was trained on **huge text** (and often more).

More (and better) data → more patterns: grammar, facts-as-text, code style, Q&A shape.

```text
tiny data  →  weak language model
internet-scale data  →  LLM-level fluency
```

Data quality matters too — junk in, junk patterns out.

---

## 3. Parameters (weights)

**Parameters ≈ weights** — the “levers” inside the network.

They control: given these input tokens, which **next token** is likely?

- Set during **training** (examples in → weights adjust)  
- Frozen (mostly) when you **use** the model (inference)

| Scale (rough) | Vibe |
|---------------|------|
| ~1–3 billion (`1.5b`) | Laptop / Ollama-friendly |
| tens of billions | Stronger, needs more GPU |
| 100B+ | Very capable, expensive to run |

**More parameters** can mean more capacity — **if** they were trained well. A huge poorly trained model is not automatically better than a smaller well-trained one.

When you see `qwen2.5:1.5b`, **`1.5b` = parameter scale**.

More detail: [`what_is_an_llm.md`](./what_is_an_llm.md) (Parameters section).

---

## 4. Tokens (how it reads language)

The model never sees “letters” as you do. It sees **tokens** (chunks: word, part-word, punctuation).

| Why this makes it powerful |
|----------------------------|
| Flexible vocab — names, code, new words as pieces |
| Billing and limits counted in **tokens**, not words |
| Same sentence can be **different token counts** on different models |

A better tokenizer + vocab that fits the data → the model “sees” language more efficiently.

Full notes: [`what_are_tokens.md`](./what_are_tokens.md)

```text
text → tokenizer → token ids → model (parameters) → next token
```

---

## 5. Transformer / attention

Most LLMs are **Transformers**.

**Self-attention** = each token can look at **other tokens** in the window, not only the last few words.

That is a core characteristic: **long-range context** in language (who “it” refers to, how a function relates to a call 20 lines up).

**LLM ≈ big Transformer + lots of data + lots of parameters, trained to predict tokens.**

---

## 6. Context window

How many **tokens** the model can consider at once (your prompt + its reply, depending on the product).

| Bigger window | Smaller window |
|---------------|----------------|
| Long docs, long chats | Forgetful / you must truncate |
| Costs more to fill | Cheaper short Q&A |

Powerful models often pair **capacity (parameters)** with a **usable window**. A 70B model with a tiny window still struggles on long documents.

---

## 7. How it was tuned (base vs instruct vs chat)

Same size, different **training stage** → different power *for you*:

| Characteristic | Effect |
|----------------|--------|
| **Base** | Completes text; not a polite assistant |
| **Instruction-tuned** | Follows “summarize / extract / translate” |
| **Chat / dialog-tuned** | Multi-turn Q&A |

A smaller **instruct** model can feel “smarter” in ChatGPT-style use than a bigger **raw base** model.

---

## 8. Compute at train and at run time

| When | Characteristic |
|------|----------------|
| **Training** | Needs enormous compute (you don’t do this for GPT-class models at home) |
| **Inference** | Needs GPU/RAM; quantization can shrink memory (see [`9_QUANTIZATION`](../9_QUANTIZATION/)) |

A model is only “powerful **in practice**” if you can **run** it (or afford the API).

---

## 9. What does *not* make it powerful by itself

| Myth | Reality |
|------|---------|
| Fancy product name | UI ≠ model quality |
| “I used OpenAI SDK” | SDK can point at HF / Ollama — not extra brain |
| More tokens in the prompt always | Can hit the window and add noise |
| Biggest parameter count only | Data, tuning, and architecture matter |

---

## 10. One picture

```text
                    what makes an LLM powerful
─────────────────────────────────────────────────────────────
  Data (huge, decent quality)
       +
  Parameters / weights (capacity)
       +
  Tokens + tokenizer (how language is chunked)
       +
  Transformer / attention (context across the sequence)
       +
  Context window (how much it can see at once)
       +
  Tuning (instruct / chat vs raw base)
       +
  Enough compute to train and to run
```

**Short memory aid**

> **Data + parameters + tokens + attention + window + tuning**  
> that’s the character of a powerful LLM — not “it has a chatbot screen.”
