"""
Simple Day-2 idea: rewrite a messy product description with an LLM.

Flow:
  1. Load a few curated products from Hugging Face
  2. Take one product's text
  3. Ask an LLM to rewrite it into a clean standard format
  4. Print before / after

This is pre-processing (rewriting), not model training.
"""

import os
from dotenv import load_dotenv
from huggingface_hub import login
from datasets import load_dataset
from litellm import completion

load_dotenv(override=True)
login(os.environ["HF_TOKEN"])


# --- 1) Load a small ready-made dataset (already curated earlier in the course) ---
# Hub: https://huggingface.co/datasets/ed-donner/items_raw_lite
ds = load_dataset("ed-donner/items_raw_lite", split="train")
print(f"Loaded train rows: {len(ds):,}")

# Use the first product that has a 'full' text field
row = ds[0]
product_text = row["full"]
price = row["price"]
title = row["title"]

print("\n=== BEFORE (raw-ish product text) ===")
print(f"Title: {title}")
print(f"Price: ${price}")
print(product_text[:800], "..." if len(product_text) > 800 else "")


# --- 2) Standard rewrite instructions ---
SYSTEM_PROMPT = """Create a concise description of a product. Respond only in this format. Do not include part numbers.
Title: Rewritten short precise title
Category: eg Electronics
Brand: Brand name
Description: 1 sentence description
Details: 1 sentence on features"""


# --- 3) Call an LLM once (Ollama local = free; change MODEL if you prefer Groq/OpenAI) ---
# Examples:
#   MODEL = "ollama/llama3.2"                 # local, needs Ollama running
#   MODEL = "groq/openai/gpt-oss-20b"         # needs GROQ_API_KEY
MODEL = "ollama/llama3.2"

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": product_text},
]

print(f"\nCalling model: {MODEL}")
kwargs = {"messages": messages, "model": MODEL}
if MODEL.startswith("ollama/"):
    kwargs["api_base"] = "http://localhost:11434"

response = completion(**kwargs)

summary = response.choices[0].message.content

print("\n=== AFTER (LLM rewritten) ===")
print(summary)

# Optional usage stats (may be None for some local setups)
usage = getattr(response, "usage", None)
if usage:
    print(f"\nInput tokens: {usage.prompt_tokens}")
    print(f"Output tokens: {usage.completion_tokens}")

print("\nDone. Idea: messy product text → clean structured summary for later ML.")
