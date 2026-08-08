# Tokens in an LLM

Related: [`what_is_an_llm.md`](./what_is_an_llm.md)

**Tokens** are the individual units that are passed into a model. Billing, context limits, and “how long can my prompt be?” are counted in **tokens**, not characters or words.

---

## Character-level tokenization

In the early days of building neural networks, one common approach was to train models **character by character**. The model would take a series of individual characters and be trained to predict the most likely **next character** given the preceding characters.

**Benefits:** The number of possible inputs was limited to letters in the alphabet and some symbols — a **manageable vocabulary size**. The model’s weights did not need to account for too many different input possibilities.

**Challenge:** The model had to understand how a sequence of characters forms a word, and all the intelligence related to the **meaning** behind a word had to be captured inside the weights. That was an **excessive expectation** from the model.

---

## Word-level tokenization

To address those challenges, the approach shifted to training neural networks on **individual words**. A vocabulary was built — a dictionary or index of all possible words. Each token corresponded to one of those words.

This allowed the model to treat each word as having a distinct meaning, rather than inferring meaning only from sequences of characters.

**Downside:** An **enormous vocabulary** — it needed to include all possible words, including names of places and people.

---

## The GPT breakthrough (token chunks)

Around the time of GPT, a breakthrough was a **middle ground** between character-level and word-level tokenization.

Instead of training on individual characters or entire words only, text was broken into **chunks of letters called tokens**. These chunks sometimes form **complete words** and sometimes **parts of words**.

The model takes a series of tokens as input and outputs tokens accordingly.

**Benefits:**

- Can handle names / proper nouns as **fragments** of tokens  
- Effective at **word stems** — the same beginning of a word as one token, then extra tokens for different endings  
- Rare or new words can be built from smaller pieces  

---

## Seeing tokenization (OpenAI tokenizer)

OpenAI provides a tool at [https://platform.openai.com/tokenizer](https://platform.openai.com/tokenizer) where you can paste text and see how it is split into tokens.

- For a sentence of **common words**, each word often maps to **one token**. The tokenizer may include the **space before a word** as part of the token — that is intentional.  
- For **less common or invented words**, the tokenizer breaks them into **multiple tokens**. Example vibe: *exquisitely* may become several tokens if it is not a single vocabulary entry.

### Rare words, compounds, invented words

- Compound words like *handcrafted* may split into pieces such as *hand* + *crafted* — meaningful parts.  
- Invented or unusual forms (e.g. *Musterers*-style words) may split into a root-like piece plus an ending.  
- Words like *witchcraft* may split into *witch* + *craft* — tokenization reflecting semantic components.

Exact splits depend on the specific tokenizer (GPT-2 vs newer GPT tokenizers differ).

### Numbers and special cases

Long numbers do **not** usually map to a single token. Digit sequences are broken into tokens (e.g. GPT-2 often grouped digits in chunks — other tokenizers may differ).

---

## Rules of thumb

| Rough rule | Meaning |
|------------|---------|
| **~4 characters ≈ 1 token** | Average for English |
| **1 token ≈ 0.75 words** | Normal English writing |
| **1,000 tokens ≈ 750 words** | Handy for estimating |

Example scale: the complete works of Shakespeare are about **900,000 words** ≈ about **1.2 million tokens**.

For exact counts, use a tokenizer tool — do not rely only on these averages.

---

## Context window

The **context window** is an extremely important LLM property: the **total number of tokens** the model can examine at one time when generating the **next token**.

Next-token prediction is the core task. The context window limits how many **input** tokens the model can consider to produce the next output token. That limit depends on the model (size / architecture / product tier).

### How it shows up when you call an API

When you call OpenAI (or similar), the input is typically a **system prompt** + **user prompt**. The model predicts the most likely next tokens based on that input — e.g. you pass website text and ask for a summary; the summary is the generated token sequence.

### Chat “memory” is an illusion

In apps like ChatGPT, the model *appears* to remember the conversation. What actually happens: **each turn**, the app sends back the **conversation so far** (system prompt + prior user messages + prior assistant replies) as input. The model then predicts the next tokens at the end of that long sequence.

So the context window must fit:

- original system prompt  
- all user prompts so far  
- all model responses so far  
- plus room for the **new** generated tokens  

### Rough context sizes (change by product/version)

| Model family (examples) | Context window (order of magnitude) |
|-------------------------|-------------------------------------|
| Gemini 1.5-class (e.g. Flash) | Up to ~**1M tokens** (~750K words by the thumb rule) |
| Claude-class | Often ~**200K tokens** |
| Many GPT API models | Often ~**128K tokens** (varies by model) |

**API cost** is usually priced **per million tokens** (input + output), so short queries stay cheap; long scraped pages + long chats burn more of the window and the budget.

Your website summarizer truncates scrape text to ~2,000 **characters** as a simple safety limit — the model’s real limit is still measured in **tokens** inside the context window.
