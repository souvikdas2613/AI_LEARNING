# `preprocess_product_with_llm_simple.py` — explained

Chapter notes (folder `14_DATASETS`).

Script: [`preprocess_product_with_llm_simple.py`](./preprocess_product_with_llm_simple.py)

Simplified from Udemy week6 **Day 2** (data pre-processing / rewriting).  
No batch jobs, no JSONL files, no Hub push — just **one product, one LLM call**.

---

## What this file does

```text
Curated product text (from Hugging Face)
              ↓
LLM rewrite with a fixed format
              ↓
Clean Title / Category / Brand / Description / Details
```

This is **pre-processing**, not training.

| Stage | This script? |
|-------|----------------|
| Curation (Day 1 style) | Already done in the Hub dataset we load |
| Pre-processing / rewrite (Day 2) | **Yes** |
| Model training (Day 3+) | No |

---

## Why rewrite with an LLM?

Raw Amazon text is messy and inconsistent.  
An LLM can normalize each product into the **same structure**, which makes later ML easier.

---

## Step by step

### 1. Load a few products

```python
ds = load_dataset("ed-donner/items_raw_lite", split="train")
row = ds[0]
product_text = row["full"]
```

Hub page: https://huggingface.co/datasets/ed-donner/items_raw_lite

### 2. System prompt

Tells the model exactly which fields to return (`Title`, `Category`, `Brand`, …).

### 3. One `completion(...)` call

Uses `litellm` so you can switch models easily:

| Model string | Needs |
|--------------|--------|
| `ollama/llama3.2` | Local Ollama running |
| `groq/openai/gpt-oss-20b` | `GROQ_API_KEY` |

### 4. Print before / after

See the messy input vs the clean structured output.

---

## How to run

```bash
# if using Ollama:
ollama serve
ollama pull llama3.2

cd 14_DATASETS
python preprocess_product_with_llm_simple.py
```

Needs: `HF_TOKEN` in `.env`, `datasets`, `litellm`, `python-dotenv`, `huggingface_hub`.

---

## vs full week6 day2 notebook

| Full notebook | This simple script |
|---------------|--------------------|
| Thousands of items | 1 item |
| Groq batch API + JSONL | Single `completion` call |
| `Batch` helper class | None |
| Push rewritten dataset to Hub | Just print result |

Read the full notebook later when you want production-scale rewriting.
