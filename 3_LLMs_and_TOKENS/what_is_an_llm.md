# What Is an LLM?

Personal learning notes: what an LLM is, how you use one, then a map of **closed** vs **open-source** model families.

Also in this folder: [`what_are_tokens.md`](./what_are_tokens.md) — character → word → token (how LLMs read text).

> Snapshot era: ~2024–2025. Names and context windows change often; always check the vendor docs for current models (e.g. `gpt-4.1-nano`, Claude 4, Gemini 2.x, Llama 4).

---

## What is an LLM?

An **LLM** (**Large Language Model**) is a type of **AI program** that can **recognize and generate text** (and often related tasks: answer questions, summarize, translate, chat, recommend).

It is called **“large”** because it is trained on **huge sets of data** — often text gathered from the internet at enormous scale (many gigabytes to far more). From enough examples, the model learns patterns in human language (and other complex data) so it can interpret prompts and produce fluent replies.

**Under the hood (same idea as before):** it predicts the **next token** in a sequence. That simple skill powers chat, summarization, coding help, and more.

| Piece | Plain meaning |
|-------|----------------|
| **Large** | Huge training data + (usually) billions of parameters |
| **Language** | Understands / generates human language (and often code); some are multimodal |
| **Model** | Learned function: input tokens → next-token probabilities → generated reply |

**In practice:** you send a prompt (and often a system message); the model generates a continuation — answers, summaries, code — one token at a time.

### Where LLMs sit in the AI map

```
AI
 └── Machine learning / deep learning
      └── Foundation models
           └── Large language models (LLMs)
                └── Often used as generative AI (new text, etc.)
```

- LLMs are a **subset of deep learning**.
- LLMs are also often described as a **subset of foundation models** — general-purpose models pre-trained at scale, then reused or specialized.
- **Generative AI** is AI that can **produce new content** (text, images, audio, synthetic data). Many LLM apps (ChatGPT, Gemini chat) are generative AI products built on LLMs.

The largest and most capable LLMs today are often **GPTs** — **G**enerative **P**retrained **T**ransformers — used inside generative chatbots like **ChatGPT** or **Gemini**.

### Pre-trained vs fine-tuned

LLMs are typically **general-purpose language models** that are:

1. **Pre-trained** — learned language patterns from massive internet-scale (and other) text by predicting next tokens / similar objectives. After this you already have a strong “foundation” model you can prompt.
2. **Fine-tuned** (optional) — further trained on narrower data for a **specific purpose** (support bot style, domain jargon, safer replies, etc.).

Example vibe: models like **Gemini** (multimodal) or dialog-focused systems ingest very large multi-source data, build a foundation language model, then you use it by **asking a question** — typed or spoken into a prompt.

### Not the same as

| Term | Difference |
|------|------------|
| **ChatGPT / Claude.ai / Gemini app** | *Products* (chat UIs) built **on top of** LLMs |
| **OpenAI API / Ollama** | *Ways to call* an LLM from code |
| **Tokenizer** | Splits text into tokens before the model sees it — see [`what_are_tokens.md`](./what_are_tokens.md) |
| **Generative AI** | Broader umbrella (text *and* images/audio/…); LLMs are a major part of it |

Examples of LLMs: GPT-4 / `gpt-4.1-nano`, Claude, Gemini, Llama, Qwen, Mistral.

---

## LLMs and the Transformer

Most modern LLMs are built on the **Transformer** — a neural-network architecture that is especially good at **understanding context** in language.

- **Self-attention** lets the model look at relationships across a sequence (which words relate to which), not just the last few words.
- That is why Transformers usually grasp context better than older sequence models for language tasks.
- **GPT** in “Generative Pretrained Transformer” means the model family is Transformer-based.

You do not need the full math yet — remember: **LLM ≈ (usually) a big Transformer trained to predict tokens.**

---

## Parameters in an LLM

Very fundamental to an LLM: the number of **parameters** inside the model.

**Parameters are also called weights.**  
Generally they are synonymous. There is a detail that they are not *exactly* the same in some situations, but basically think of **weights and parameters as the same thing**.

**Model weights** are the **levers** within a model that control what kinds of outputs it generates when it is given some inputs. They determine how the model predicts the **next word** (next token) that will follow.

These weights are **set when you train** an LLM. The model sees lots and lots of examples and uses those examples to **adjust its weights** until it gets better and better at predicting the next token. (Tokens: see [`what_are_tokens.md`](./what_are_tokens.md).)

The way the model improves is by adjusting all of its weights. If you already know data science, this will feel familiar. If you are new to it, keep this intuition: **parameters/weights control the output** — training is the process of tuning those levers from examples.

Rough public scale for GPT generations:

| Model | Parameters (approx.) |
|-------|----------------------|
| GPT-2 | ~1.5 billion |
| GPT-3 | ~175 billion |
| GPT-4 | Not officially published (estimates vary; treat huge exact claims carefully) |

When you see **`qwen2.5:1.5b`** in Ollama, the **`1.5b`** is about parameter scale (1.5 billion) — small enough for a laptop.

---

## Types of LLMs (how they are tuned)

There are three common *kinds* of language models by **how they were trained to respond**. Each wants prompts a bit differently.

| Type | Trained to… | Prompt vibe | Example tasks |
|------|-------------|-------------|----------------|
| **Generic (base) language model** | Predict the **next word/token** from training-style text | Continuation / completion | “Once upon a time…” → keeps writing |
| **Instruction-tuned** | Follow an **instruction** in the input | Clear commands | Summarize X, translate X, classify sentiment of X, write a poem in style of X |
| **Dialog-tuned (chat)** | Produce the **next reply in a conversation** | Chat / Q&A turns | Chatbots; usually a special case of instruction-tuning framed as dialogue |

What you use daily (ChatGPT, Claude, your API `messages` with system + user) is usually **instruction- and/or dialog-tuned**, not a raw base model.

---

## Examples of LLMs (quick tour)

Names change fast; this is a **recognition list**, not a ranking.

### Closed / product-side (you call via UI or API)

| Name | Org | One-line note |
|------|-----|----------------|
| **GPT-3 / GPT-3.5 / GPT-4** family | OpenAI | Classic GPT line; ChatGPT is the *product* on top; APIs expose models like `gpt-4.1-nano` |
| **Claude** | Anthropic | Strong chat / assistant models (closed weights) |
| **Gemini** (earlier consumer name **Bard**) | Google | Multimodal chat + APIs; long-context variants |
| **PaLM 2** | Google | Earlier Google LLM line used inside Google products |
| **Command R+** | Cohere | Strong for RAG-style retrieval apps |
| **Grok** | xAI | Tied to X (Twitter) product |

Older / specialized names you may still see: **BERT** (encoder, great at understanding tasks), **T5** (text-to-text), **LaMDA** (dialogue-oriented), **Turing NLG** (Microsoft).

### Open-weight / open-source side (often run with Ollama)

| Name | Org | One-line note |
|------|-----|----------------|
| **Llama / LLaMA 3.x** | Meta | Flagship open-weight family |
| **Mistral / Mixtral** | Mistral | Fast dense + strong MoE open models |
| **Qwen** | Alibaba Cloud | Strong code & chat; good Ollama picks |
| **Gemma** | Google | Smaller open models |
| **Phi / Phi-3** | Microsoft | Small, capable open models |
| **BLOOM**, **GPT-J**, **Falcon**, **RoBERTa** | Various | Earlier open / research lines you may see in docs |

**Coding helper:** GitHub **Copilot** is LLM-powered assistance for **code**, not a general chat product like ChatGPT.

Full comparison tables (params, context, license) are below.

---

## Key definitions

### Closed models (proprietary / non-open-source)

**Closed models** are LLMs whose **weights are not publicly released**. You use them through a product or API (ChatGPT, Claude.ai, OpenAI API, Google AI Studio, etc.). You cannot download the full model and run it yourself.

| You can | You usually cannot |
|---------|-------------------|
| Call the model via API / chat UI | Download the raw weights |
| Pay per token or subscription | Fully inspect / retrain the base model locally |
| Use the vendor’s hosted fine-tunes (if offered) | Redistribute the model freely |

Examples from this chart: **GPT-4**, **Claude 3**, **Gemini**, **Command R+**, **Grok**.

### Frontier models

**Frontier models** are the **most capable, cutting-edge LLMs available at a given time** — the “state of the art” (SOTA) for reasoning, coding, long context, multimodal work, etc.

Important nuances:

- **Frontier ≠ always closed.** Most frontier models today are closed (GPT / Claude / Gemini flagships), but strong open releases (e.g. top Llama / Mixtral / Qwen variants) are often called the **open-source frontier**.
- **Frontier shifts over time.** Yesterday’s frontier becomes today’s mid-tier as newer models ship.
- **“Open-source frontier”** means the **best open-weight families** people actually pull and run locally — Llama, Mixtral, Qwen, Gemma, Phi — not every small research model ever published.

| Term | Short meaning |
|------|----------------|
| **Closed model** | Weights locked; access via API / product only |
| **Open-source / open-weight model** | Weights available to download and run (license still matters) |
| **Frontier model** | Current top-tier capability for its class (closed or open) |
| **Open-source frontier** | Leading open-weight model families right now |

---

## Three ways to use models

There are **three common ways** to talk to an LLM. Same idea of “ask a model / get text back” — different packaging.

```
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ Chat interfaces │   │   Cloud APIs    │   │ Direct inference│
│  (like ChatGPT) │   │ (code → cloud)  │   │ (run yourself)  │
└─────────────────┘   └─────────────────┘   └─────────────────┘
```

### 1. Chat interfaces

**What:** A website or app chat box — “like ChatGPT.”

**Examples:** ChatGPT, Claude.ai, Gemini, Perplexity, meta.ai.

**Best for:** Quick questions, brainstorming, learning prompts by hand.

**Tradeoff:** Easy, but hard to automate, scrape websites, or build apps on top. You are a human in the loop.

### 2. Cloud APIs

**What:** Your **code** calls a remote model over the internet (HTTP). The vendor hosts the GPU; you pay per use (or use free tiers).

**Includes:**

- **LLM APIs** — e.g. OpenAI API (`openai` Python package), Anthropic API, Google AI API  
- **Frameworks** — e.g. LangChain (wrappers, chains, tools on top of APIs)  
- **Managed AI cloud services** — Amazon Bedrock, Google Vertex AI, Azure ML (enterprise-style hosting of many models)

**Best for:** Apps, scripts, notebooks — what you do in `1_PRACTICE_ON_OLLAMA_and_OPENAI/` and `2_USER_PROMPT_SYSTEM_PROMPT/`.

**Tradeoff:** Needs API keys and (usually) money; data leaves your machine; model choice is whatever the cloud offers.

### 3. Direct inference

**What:** The model runs **on your machine** (or a server you control). You load weights and generate tokens yourself — no OpenAI bill for that call.

**Includes:**

- **Hugging Face Transformers** — load models in Python, full control, more setup / VRAM  
- **Ollama** — simple local runner; OpenAI-compatible API on `localhost` (what your Ollama practice script uses)

**Best for:** Privacy, zero per-token cloud cost, learning how open models feel, offline use.

**Tradeoff:** Needs disk + RAM/VRAM; smaller models than cloud frontier; you manage install / pulls / updates.

### Quick compare

| Way | Who runs the model? | Typical cost | Your practice |
|-----|---------------------|--------------|---------------|
| **Chat UI** | Vendor | Subscription / free tier | Manual chatting |
| **Cloud API** | Vendor | Pay per tokens | `Test_OPENAI_LLM_with_openAI.py`, website summarizer |
| **Direct inference** | You (local) | Electricity + hardware | `Test_ollama_with_OPENAI.py`, Ollama |

Same **messages** idea (system + user prompts) works across cloud APIs and Ollama’s OpenAI-compatible endpoint — that’s why one Python style can hit both.

---

## Who builds these LLMs?

A quick map of **company → model name → chat product** (so GPT vs ChatGPT, Claude the model vs Claude the app, etc. don’t get mixed up).

| Company | Model family | Chat / product you open in a browser |
|---------|--------------|--------------------------------------|
| **OpenAI** | GPT-4 family | ChatGPT |
| **Anthropic** | Claude | Claude |
| **Google** | Gemini | Gemini Advanced |
| **Cohere** | Command R+ | Command R+ |
| **Meta** | Llama | meta.ai |
| **Perplexity** | Perplexity | Perplexity (search) |

---

## Non-open-source LLMs (closed / proprietary)

| Model | Params | Tokens (context) | Architecture | Org | Release | License | MoE | Fine-tuning | Notes |
|-------|--------|------------------|--------------|-----|---------|---------|-----|-------------|-------|
| GPT-4 | Est. 500B–1.7T | 8K / 32K | Dense or MoE | OpenAI | Mar 2023 | Closed | Yes* | No | Top-tier, closed weights |
| GPT-4-turbo | Unknown | 128K | MoE (likely) | OpenAI | Nov 2023 | Closed | Yes | No | Used in ChatGPT Plus |
| GPT-3.5 | ~175–200B (est.) | 4K / 16K | Dense | OpenAI | 2022 | Closed | No | No | Default in free ChatGPT |
| Claude 3 Opus | Unknown | 200K+ | MoE (rumored) | Anthropic | Mar 2024 | Closed | Yes* | No | SOTA performance |
| Claude 3 Sonnet | Unknown | 200K+ | Unknown | Anthropic | Mar 2024 | Closed | ? | No | Default Claude on web |
| Claude 3 Haiku | Unknown | 200K+ | Unknown | Anthropic | Mar 2024 | Closed | ? | No | Lightweight variant |
| Gemini 1.5 Pro | Unknown | 1M | MoE (likely) | Google DeepMind | Feb 2024 | Closed | Yes | No | Very long context |
| Gemini 1.0 Ultra | Unknown | 32K | Transformer / MoE | Google DeepMind | Dec 2023 | Closed | Yes | No | Top-tier competitor to GPT-4 |
| Gemini 1.0 Pro | Unknown | 32K | Transformer | Google DeepMind | Dec 2023 | Closed | ? | No | API via Google AI Studio |
| Gemini Nano | Unknown | 4K–8K | Lightweight | Google DeepMind | 2024 | Closed | No | No | For Android / on-device |
| Command R+ | Unknown | 128K | Transformer | Cohere | 2024 | Closed | No | No | RAG optimized, proprietary |
| Grok (xAI) | Unknown | Unknown | Unknown | xAI | Late 2023–24 | Closed | ? | No | Integrated in X (Twitter) |
| Ernie 4.0 | Unknown | ~200K+ | Transformer | Baidu | 2023 | Closed | ? | No | Chinese LLM |
| PanGu-Σ | Unknown | 128K+ | Transformer | Huawei | 2023–2024 | Closed | ? | No | China's answer to GPT-4 |
| Jurassic-2 | Up to 178B | 8K | Transformer | AI21 Labs | 2023 | Closed | No | Yes (via API) | Fine-tuning via API |
| Mosaic MPT-30B | Unknown (est. 30B+) | 8K | Transformer | Databricks | 2023 | Closed | No | Yes (API) | Moved from open to cloud |
| Sage (Perplexity) | Unknown | 128K+ | Unknown | Perplexity AI | 2024–2025 | Closed | ? | No | Search-oriented contender |

\* = reported / rumored; closed models often do not publish exact architecture or parameter counts.

---

## Open-source frontier (families to know)

- **Llama** — Meta  
- **Mixtral** — Mistral  
- **Qwen** — Alibaba Cloud  
- **Gemma** — Google  
- **Phi** — Microsoft  

These are the families you typically pull with **Ollama** for local practice.

---

## Open-source LLMs comparison

| Model | Params | Tokens (context) | Architecture | Org | Release | License | MoE | Fine-tuning | Notes |
|-------|--------|------------------|--------------|-----|---------|---------|-----|-------------|-------|
| LLaMA 2 | 7B / 13B / 70B | 4K–32K | Transformer | Meta | Jul 2023 | Non-commercial | No | Yes (with approval) | High quality |
| LLaMA 3 | 8B / 70B | 8K–32K | Transformer | Meta | Apr 2024 | Open (custom) | No | Yes (more permissive) | Strong open LLM |
| Mistral 7B | 7B | 8K | Transformer | Mistral AI | Sep 2023 | Apache 2.0 | No | Yes | Fast, efficient |
| Mixtral 8x7B | 46.7B total (12.9B active) | 32K | MoE | Mistral AI | Dec 2023 | Apache 2.0 | Yes | Yes | Strong open MoE |
| Gemma | 2B / 7B | 8K | Transformer | Google DeepMind | Feb 2024 | Apache 2.0 | No | Yes | Small, efficient |
| Phi-3-mini | 3.8B | 128K | Transformer | Microsoft | Apr 2024 | MIT | No | Yes | Small, capable |
| Yi | 6B / 34B | 32K | Transformer | 01.AI (China) | Oct 2023 | Apache 2.0 | No | Yes | Strong multilingual |
| Qwen | 7B / 14B / 72B | 32K+ | Transformer | Alibaba | 2023–2024 | Apache 2.0 / Custom | No | Yes | Strong in code & chat |
| Falcon | 7B / 40B | 2K–4K | Transformer | TII (UAE) | Jun 2023 | Apache 2.0 | No | Yes | Fast inference |
| Orca 2 | 7B | 4K–8K | Transformer | Microsoft | Nov 2023 | OpenRAIL | No | Yes (restricted) | Reasoning-focused |
| Pythia | 70M–12B | 2K–4K | Transformer | EleutherAI | 2022–2023 | Apache 2.0 | No | Yes | Research model |
| OpenHermes | 7B (LLaMA-based) | 4K–8K | Transformer | Teknium / others | 2023 | OpenRAIL | No | Yes | Instruction-tuned |
| Mamba | ~2.8B | 65K | State Space Model | Princeton et al. | Early 2024 | MIT | No | Yes | Non-transformer |
| Command R+ | — | 128K | Transformer | Cohere | 2024 | Custom (commercial) | No | No | Optimized for RAG |
| TinyLLaMA | 1.1B | 2K–4K | Transformer | Community | 2023 | MIT | No | Yes | On-device / tiny |

---

## Column cheat sheet

| Column | Meaning |
|--------|---------|
| **Params** | Model size (billions of parameters). Bigger ≠ always better; affects VRAM and speed. |
| **Tokens** | Context window — how much text the model can see at once. |
| **Architecture** | Usually Transformer; MoE = Mixture of Experts (activate only some experts per token). |
| **License** | Closed = API-only weights. Open licenses (Apache 2.0, MIT, etc.) allow local use / fine-tunes (read the fine print). |
| **MoE** | Mixture of Experts — total params can be large while *active* params stay smaller (cheaper/faster inference). |
| **Fine-tuning** | Whether you can specialize the model on your data (locally or via API). |

---

## How this ties to your learning path

| Path | Examples from this chart | Where you practice |
|------|--------------------------|--------------------|
| **Closed cloud API** | GPT-4 family, Claude, Gemini | `1_PRACTICE_ON_OLLAMA_and_OPENAI/`, `2_USER_PROMPT_SYSTEM_PROMPT/` |
| **Local open weights** | Llama, Qwen, Mistral, Gemma, Phi | Ollama + `Test_ollama_with_OPENAI.py` |

For cheap cloud experiments you already use something like **`gpt-4.1-nano`** (newer than the GPT-4 rows in this chart). For free local runs, pick a small open model (e.g. **Qwen** / **Gemma** / **Phi**-class sizes that fit your machine).
