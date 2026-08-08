# LLMs and Tokens — Practice Guide

This guide explains what **tokens** are, why they matter for LLMs, and how `PRACTICE_TOKENS.py` uses **tiktoken** to inspect them.

---

## What is a token?

Large Language Models (LLMs) do **not** read text character by character or word by word. They break text into smaller pieces called **tokens**.

A token can be:

- A whole word (`umbrella`)
- Part of a word (`S` + `ouv` + `ik` for “Souvik”)
- A space glued to a word (` my`, ` name`)
- Punctuation

The exact split depends on the **tokenizer** for the model you use (here: `gpt-4.1-nano` from `.env`).

---

## Why tokens matter

1. **Billing** — Providers charge by tokens (input + output).
2. **Context limits** — Models have a max context window; exceeding it fails or truncates.
3. **Prompt design** — Shorter prompts cost less and leave more room for the reply.
4. **Debugging** — Seeing tokens shows how the model actually “chunks” your text.

Rule of thumb (English, approximate):

> ~1 token ≈ 4 characters ≈ ¾ of a word  
> ~100 tokens ≈ 75 words

Always measure with tiktoken when accuracy matters.

---

## What is tiktoken?

**tiktoken** is OpenAI’s fast BPE (Byte Pair Encoding) tokenizer for Python. It can:

- Encode text → list of token IDs  
- Decode token IDs → text  
- Pick the correct encoding for a given model name  

Official package: [tiktoken on PyPI](https://pypi.org/project/tiktoken/)

---

## Install dependencies

```bash
pip install tiktoken python-dotenv
```

---

## Environment setup (`.env`)

Keep secrets in the AI_LEARNING repo root `.env` (gitignored), for example:

```env
OPENAI_API_KEY=sk-your-key-here
MODEL_NAME=gpt-4.1-nano
```

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | Checked at startup (this script does not call the API) |
| `MODEL_NAME` | Chooses the matching tokenizer via `tiktoken.encoding_for_model(...)` |

```python
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME')
```

---

## How `PRACTICE_TOKENS.py` works

1. Loads `.env` and prints whether key + model name were found.  
2. Builds the model’s tokenizer:

```python
encoding = tiktoken.encoding_for_model(MODEL_NAME)
```

3. **Example 1** — encodes `"Hi my name is Souvik"` and prints each ID ↔ text.  
4. **Example 2** — same for `"Hi my name is Souvik and I have an umbrella"`.

Core loop:

```python
tokens = encoding.encode("Hi my name is Souvik")
for token_id in tokens:
    token_text = encoding.decode([token_id])
    print(f"{token_id} = {token_text}")
```

---

## Run the script

```bash
python PRACTICE_TOKENS.py
```

---

## Example output (real run)

Captured with model `gpt-4.1-nano`.

### Startup checks

```text
API key found and looks good so far!


Model name found gpt-4.1-nano and looks good so far!
```

Your API key and `MODEL_NAME` loaded correctly from `.env`. The script only needs the model name for tokenization — it does not send requests to OpenAI for these examples.

---

### Example 1 — `"Hi my name is Souvik"`

**Input text:** `Hi my name is Souvik`

**Raw token IDs:**

```text
[12194, 922, 1308, 382, 336, 14851, 507]
```

**Each ID decoded:**

```text
12194 = Hi
922 =  my
1308 =  name
382 =  is
336 =  S
14851 = ouv
507 = ik
```

**What this shows**

| Observation | Meaning |
|-------------|---------|
| **7 tokens** for 5 “words” | Words ≠ tokens |
| Leading spaces (` my`, ` name`, ` is`) | Spaces are often glued onto the *next* word as one token |
| `Souvik` → `S` + `ouv` + `ik` | Uncommon / proper names often split into **subword** pieces |
| Large integers (e.g. `14851`) | Each piece maps to a fixed ID in the model’s vocabulary |

So the model does not see one neat “Souvik” token — it sees three chunks that it learned during training.

---

### Example 2 — `"Hi my name is Souvik and I have an umbrella"`

**Input text:** `Hi my name is Souvik and I have an umbrella`

**Raw token IDs:**

```text
[12194, 922, 1308, 382, 336, 14851, 507, 326, 357, 679, 448, 77378]
```

**Each ID decoded:**

```text
12194 = Hi
922 =  my
1308 =  name
382 =  is
336 =  S
14851 = ouv
507 = ik
326 =  and
357 =  I
679 =  have
448 =  an
77378 =  umbrella
```

**What this shows**

| Observation | Meaning |
|-------------|---------|
| First 7 IDs match Example 1 | Same prefix text → same tokens (tokenization is deterministic) |
| **12 tokens** total | Extra phrase added 5 more tokens |
| `umbrella` is **one** token (`77378`) | Common English words often stay whole (with a leading space) |
| Contrast with `Souvik` | Frequent words → fewer tokens; rare names → more tokens |

That last contrast is why token counting matters for cost: a rare name or technical string can use more tokens than a long common word.

---

### Side-by-side summary

| Sentence | Token count | Notable split |
|----------|-------------|----------------|
| `Hi my name is Souvik` | **7** | `Souvik` → `S` / `ouv` / `ik` |
| `... and I have an umbrella` | **12** | `umbrella` stays 1 token |

---

## Key API calls to remember

| Call | Meaning |
|------|---------|
| `tiktoken.encoding_for_model(name)` | Tokenizer for a named OpenAI model |
| `encoding.encode(text)` | Text → list of token IDs |
| `encoding.decode([id])` | One (or more) IDs → text |
| `len(encoding.encode(text))` | Token count for billing / limits |

Quick helper:

```python
def count_tokens(text: str, model: str) -> int:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))
```

---

## Context window

The **context window** is one of the most important properties of an LLM. It is the total number of tokens the model can examine at one time when generating the **next token**.

Next-token prediction is the core task of the model. The context window limits how many input tokens the model can consider to produce the next output token. That limit depends on model size (parameters) and architecture.

### How it shows up in practice

When you first call an LLM (e.g. OpenAI), the input is typically a **system prompt** + a **user prompt**. The model predicts the most likely next tokens from that input. Example: you pass website text and ask for a summary — the summary is the generated token sequence that follows.

In chat apps like ChatGPT, the model *appears* to remember the conversation. That is an illusion (see also `README_LLM_STATELESS_NO_MEMORY.md`). Each turn, the **entire conversation so far** — user inputs and model replies — is sent back as input. The model then predicts the next tokens from that full sequence.

So the context window covers everything up to the current point:

- Original system prompt  
- All user messages  
- All assistant replies  
- Plus room for the new output tokens being generated  

New tokens are appended at the end of this long sequence to continue the chat.

### Typical sizes (order of magnitude)

| Model family | Context window (approx.) | Rough word equivalent |
|--------------|--------------------------|------------------------|
| Gemini 1.5 Flash | **1,000,000** tokens | ~750,000 words |
| Claude series | **200,000** tokens | — |
| Many GPT models | **128,000** tokens | — |

Exact limits change by model version — always check the provider’s docs for the model you use.

### Key takeaways

- The context window includes **all** input prompts, system prompts, and generated output tokens in the conversation (whatever still fits).
- If history grows past the window, older turns must be dropped, summarized, or otherwise truncated — the model cannot “see” beyond the limit.
- API pricing is usually **per million tokens**, so short queries stay cheap; long chats and big documents cost more because they fill more of the window.
- Token counting (tiktoken) helps you stay under the limit and estimate cost before you call the API.

This ties directly to the “fake memory” pattern: resending full history works only while that history still fits inside the context window.

---

## Practice ideas

1. Encode your full name — see if it splits like `Souvik`.  
2. Compare `len(tokens)` for the same text under different models (if supported).  
3. Encode a long paragraph and print the count.  
4. Try emojis, URLs, code, or non-English text — splits often surprise you.  
5. Count tokens for a full chat `messages` list and compare to your model’s context window.

---

## Summary

- LLMs think in **tokens**, not words.  
- **tiktoken** is the standard way to inspect OpenAI-compatible tokenization.  
- Install: `pip install tiktoken`.  
- Real run above shows: proper names can split; common words like `umbrella` may stay one token; leading spaces often attach to the next word.  
- The **context window** caps how many tokens the model can see for next-token prediction — including the whole conversation you resend each turn.
