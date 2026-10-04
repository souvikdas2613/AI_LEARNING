"""
Simple Amazon Appliances dataset walkthrough.

Idea:
  1. Load one Hugging Face dataset config
  2. Look at a few rows
  3. Keep only rows with a usable price
  4. Split into train / validation / test
"""

import os
from dotenv import load_dotenv
from huggingface_hub import login
from datasets import load_dataset

load_dotenv(override=True)
login(os.environ["HF_TOKEN"])


# 1) Load Appliances product metadata from Hugging Face
# Details: 2_amazon_appliances_dataset_simple.md
dataset = load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023",  # dataset on Hugging Face
    "raw_meta_Appliances",              # config: Appliances product metadata
    split="full",                       # use the full split
    trust_remote_code=True,             # allow dataset's custom loader script
)

print(f"Total rows: {len(dataset):,}")
print("First row keys:", list(dataset[0].keys()))
print("Example title:", dataset[0].get("title"))
print("Example price:", dataset[0].get("price"))


# 2) Keep only rows with a valid price between $1 and $1000
clean = []
for row in dataset:
    try:
        price = float(row["price"])
    except (TypeError, ValueError):
        continue

    if 1.0 <= price <= 1000.0:
        clean.append(
            {
                "title": row.get("title"),
                "price": price,
                "description": row.get("description"),
            }
        )

print(f"Clean rows with price $1–$1000: {len(clean):,}")


# 3) Find the most expensive item in the clean list
most_expensive = max(clean, key=lambda x: x["price"])
print(f"Most expensive: {most_expensive['title']} = ${most_expensive['price']:,.2f}")


# 4) Simple train / validation / test split (80% / 10% / 10%)
n = len(clean)
train = clean[: int(n * 0.8)]
val = clean[int(n * 0.8) : int(n * 0.9)]
test = clean[int(n * 0.9) :]

print(f"train={len(train):,}  val={len(val):,}  test={len(test):,}")
print("Done.")
