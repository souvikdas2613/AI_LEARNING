# `amazon_appliances_dataset_simple.py` — explained

Chapter notes (folder `14_DATASETS`).

Script: [`amazon_appliances_dataset_simple.py`](./amazon_appliances_dataset_simple.py)  
Related theory: [`1_what_is_a_dataset.md`](./1_what_is_a_dataset.md)

---

## What this file does (one sentence)

It **loads** Amazon Appliances product metadata from Hugging Face, **filters** rows with a usable price, finds the **most expensive** item, then makes a simple **train / validation / test** split.

```text
Hugging Face dataset
        ↓
load Appliances metadata
        ↓
keep rows with price $1–$1000
        ↓
train (80%) / val (10%) / test (10%)
```

---

## Step 1 — Imports + Hugging Face login

```python
import os
from dotenv import load_dotenv
from huggingface_hub import login
from datasets import load_dataset

load_dotenv(override=True)
login(os.environ["HF_TOKEN"])
```

| Line / piece | Meaning |
|--------------|---------|
| `os` | Read environment variables (like `HF_TOKEN`) |
| `load_dotenv` | Load a `.env` file into the environment |
| `login` | Authenticate with Hugging Face Hub |
| `load_dataset` | Download / open a dataset from Hugging Face |
| `load_dotenv(override=True)` | Read `.env`; overwrite existing env vars if present |
| `login(os.environ["HF_TOKEN"])` | Log in using your token |

Put this in a `.env` file (same folder or parent, depending where you run from):

```text
HF_TOKEN=hf_...
```

---

## Step 2 — Load the dataset

```python
dataset = load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023",  # dataset on Hugging Face
    "raw_meta_Appliances",              # config: Appliances product metadata
    split="full",                       # use the full split
    trust_remote_code=True,             # allow dataset's custom loader script
)
```

Plain English:

> Load the full Appliances product-metadata subset from that Hugging Face dataset into the variable `dataset`.

---

### What is the actual Hugging Face URL?

The first argument is **not** a full URL. It is a **Hub dataset id**:

```text
McAuley-Lab / Amazon-Reviews-2023
     │                 │
     │                 └── dataset name
     └── organization / user on Hugging Face
```

That maps to this web page:

**https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023**

So in your head:

```text
Code string:
  "McAuley-Lab/Amazon-Reviews-2023"

Browser URL:
  https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023
```

`load_dataset(...)` talks to the Hugging Face Hub, finds that dataset repo, downloads the needed files (first time), and builds a Python `dataset` object.

Category / config files for raw product metadata live under paths like:

**https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/tree/main/raw/meta_categories**

You are not downloading “the whole Amazon internet.”  
You are asking for **one named configuration** inside that repo.

---

### Argument-by-argument

| Argument | Meaning |
|----------|---------|
| `"McAuley-Lab/Amazon-Reviews-2023"` | Dataset repo id → Hub URL above |
| `"raw_meta_Appliances"` | **Config / subset** = Appliances **product metadata** |
| `split="full"` | Load the split named `full` (this dataset’s naming) |
| `trust_remote_code=True` | Allow the repo’s custom Python loader script to run |

Important distinction:

```text
"Amazon-Reviews-2023"     → whole dataset repo on HF
"raw_meta_Appliances"     → one configuration / subset inside it
split="full"              → which slice of that config to load
```

Conceptually:

```text
https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023
                │
                ├── raw_meta_Appliances   ← YOU LOAD THIS
                ├── raw_meta_Electronics
                ├── raw_meta_Books
                └── ...
                         │
                         └── split = full
                                  ├── product row 0
                                  ├── product row 1
                                  └── ...
```

**`raw_meta`** ≈ product metadata (title, price, description, features, …)  
**not** “only customer review text.”

---

### Does this `load_dataset(...)` call use `HF_TOKEN`?

Short answer:

| Piece in the script | Uses token? |
|---------------------|-------------|
| `login(os.environ["HF_TOKEN"])` earlier | **Yes** — explicitly logs you into Hugging Face |
| `load_dataset(...)` itself | **Often works without a token** for this **public** dataset, but after `login(...)` your session is authenticated |

More detail:

1. **This Amazon dataset is public** on Hugging Face.  
   Many people can download public datasets **without** logging in.

2. **Your script still logs in first:**

   ```python
   load_dotenv(override=True)
   login(os.environ["HF_TOKEN"])
   ```

   So when `load_dataset(...)` runs, Hugging Face libraries may use that logged-in identity / cached token.

3. **`load_dataset(...)` does not take `token=` in this line.**  
   You are not writing `load_dataset(..., token=hf_token)`.  
   Auth happens earlier via `login(...)`, or via env var `HF_TOKEN` that Hugging Face libs often auto-detect.

4. **When is a token actually required?**
   - private or gated datasets / models  
   - higher rate limits / authenticated Hub access  
   - pushing datasets back to the Hub  
   - some orgs require login even for public downloads

5. **So for this exact public Appliances load:**
   - Token is **not strictly required by the dataset being private**
   - Your script **does use the token** because you call `login(HF_TOKEN)` before loading
   - If you deleted the login lines, `load_dataset(...)` would often still work for this public dataset (network permitting)

```text
.env  →  HF_TOKEN
           ↓
     login(HF_TOKEN)     ← uses token explicitly
           ↓
     load_dataset(...)   ← downloads public Appliances meta
                           (auth optional for this public set,
                            but already logged in if login ran)
```

---

### What happens on your machine after the call?

First run:

```text
Hub URL / files  →  download  →  local HF cache  →  Python `dataset`
```

Later runs:

```text
local HF cache  →  Python `dataset`   (much faster; no full re-download)
```

Typical cache location (Linux):

```text
~/.cache/huggingface/datasets/
```

So `load_dataset` is not “streaming forever from the browser page.”  
It **uses the Hub as the source**, then works from a **local cache**.

---

### `trust_remote_code=True` — why?

Some older Hub datasets include a Python script (for example `Amazon-Reviews-2023.py`) that tells `datasets` **how** to read the files.

`trust_remote_code=True` means:

> “I allow that dataset repo’s loader code to run on my machine.”

Only do this for repos you trust.

If you see *Dataset scripts are no longer supported*, pin:

```bash
pip install datasets==3.6.0
```

Then restart the kernel / shell and try again.

---

## Step 3 — Peek at the data

```python
print(f"Total rows: {len(dataset):,}")
print("First row keys:", list(dataset[0].keys()))
print("Example title:", dataset[0].get("title"))
print("Example price:", dataset[0].get("price"))
```

| Line / piece | Meaning |
|--------------|---------|
| `len(dataset)` | How many product rows |
| `:,` | Thousands separator in the print (`1,234,567`) |
| `dataset[0]` | First row |
| `.keys()` | Field names in that row (`title`, `price`, …) |
| `.get("title")` | Read `title` safely (returns `None` if missing) |

This is your first “what does this dataset look like?” check.

---

## Step 4 — Keep only rows with a good price

```python
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
```

| Line / piece | Meaning |
|--------------|---------|
| `clean = []` | Empty list for kept examples |
| `for row in dataset` | Walk every product |
| `float(row["price"])` | Convert price text → number |
| `except ...: continue` | Skip rows with missing / junk prices |
| `1.0 <= price <= 1000.0` | Keep only prices in this range |
| `clean.append({...})` | Store a small dict: title, price, description |

Why filter?

- Many rows have empty or invalid prices  
- Extreme prices can distort learning  
- You only keep fields you care about

This is **data curation** in a few lines.

---

## Step 5 — Most expensive item

```python
most_expensive = max(clean, key=lambda x: x["price"])
print(f"Most expensive: {most_expensive['title']} = ${most_expensive['price']:,.2f}")
```

### What this line is asking

> “Look through every dict in `clean`, and return the **whole dict** whose `price` is the largest.”

`clean` looks conceptually like:

```text
clean = [
  {"title": "Blender A", "price": 49.99,  "description": [...]},
  {"title": "Oven B",    "price": 899.00, "description": [...]},
  {"title": "Fan C",     "price": 25.00,  "description": [...]},
]
```

After this line, `most_expensive` would be the **Oven B** dict (highest price), not just the number `899.00`.

---

### Break the line into pieces

```python
most_expensive = max(clean, key=lambda x: x["price"])
```

| Piece | Meaning |
|-------|---------|
| `max(...)` | Built-in Python function: “give me the biggest thing” |
| `clean` | The list to search |
| `key=...` | “Don’t compare whole dicts — compare using **this value** from each item” |
| `lambda x: x["price"]` | Tiny function: take item `x`, return its price |
| `most_expensive = ...` | Store the winning **dict** (the full product row) |

Without `key`, Python would try to compare dicts directly, which is not what you want here.  
With `key=lambda x: x["price"]`, Python compares **numbers** (the prices).

---

### What is `lambda`?

`lambda` means: **a small one-line function with no `def` name**.

These two are the same idea:

```python
# short form used in the script
key=lambda x: x["price"]

# longer equivalent
def get_price(x):
    return x["price"]

most_expensive = max(clean, key=get_price)
```

Read `lambda x: x["price"]` as:

```text
for each item x in clean:
    use x["price"] as the score for comparison
```

---

### What `max` does step by step

```text
start with first item as current winner
look at next item
if next item's price > winner's price → new winner
...
return the winner dict
```

Example:

```text
Blender A  price=49.99   → current winner
Oven B     price=899.00  → bigger → new winner
Fan C      price=25.00   → smaller → keep Oven B

result = Oven B dict
```

---

### Why not only get the max price number?

You *could* write:

```python
max_price = max(item["price"] for item in clean)
```

That gives only:

```text
899.00
```

But this line:

```python
most_expensive = max(clean, key=lambda x: x["price"])
```

gives the **full product**:

```text
{
  "title": "Oven B",
  "price": 899.00,
  "description": [...]
}
```

So you can print both title and price:

```python
print(f"Most expensive: {most_expensive['title']} = ${most_expensive['price']:,.2f}")
```

| Print piece | Meaning |
|-------------|---------|
| `most_expensive['title']` | Product name from the winning dict |
| `most_expensive['price']` | Price from that same dict |
| `:,.2f` | Format as money-like number: commas + 2 decimals (`899` → `899.00`) |

---

### Same idea with a plain loop (for learning)

```python
most_expensive = clean[0]
for item in clean:
    if item["price"] > most_expensive["price"]:
        most_expensive = item
```

`max(..., key=...)` is just the short, Pythonic version of that loop.

Simple exploration goal: “What’s the top of this cleaned set?”

---

## Step 6 — Train / validation / test split

```python
n = len(clean)
train = clean[: int(n * 0.8)]
val = clean[int(n * 0.8) : int(n * 0.9)]
test = clean[int(n * 0.9) :]
```

### Why do we need this?

If you give **all** products to the model for training, you cannot honestly answer:

> “How well does it work on products it has **never** seen?”

The model might only **memorize** the training examples (prices + titles it already saw).  
That looks great on the same data — and fails on new Amazon products.

So we **cut the cleaned list into 3 jobs**:

| Split | Share in this script | Job |
|-------|----------------------|-----|
| `train` | 80% | Teach the model patterns |
| `val` | 10% | Check while building / tuning (try ideas, pick better settings) |
| `test` | 10% | Final exam — touch as little as possible until the end |

```text
clean examples
     │
     ├── 80% → train        "study these"
     ├── 10% → validation   "practice quiz while learning"
     └── 10% → test         "final exam (unseen)"
```

Real-world analogy:

```text
train  = textbooks you study
val    = practice tests while preparing
test   = the real exam you take once
```

Without this split, your accuracy number can be **fake-high** because the model already saw those examples.

This is the same idea as in [`1_what_is_a_dataset.md`](./1_what_is_a_dataset.md).

---

### What each line does

| Piece | Meaning |
|-------|---------|
| `n = len(clean)` | How many clean products we have |
| `train = clean[: int(n * 0.8)]` | From start up to 80% |
| `val = clean[int(n * 0.8) : int(n * 0.9)]` | From 80% up to 90% |
| `test = clean[int(n * 0.9) :]` | From 90% to the end |

Example if `n = 1000`:

```text
train = clean[0 : 800]      # 800 items
val   = clean[800 : 900]    # 100 items
test  = clean[900 : 1000]   # 100 items
```

`int(...)` turns `1000 * 0.8` → `800` (list indexes must be whole numbers).

---

### Important limitation (kept simple on purpose)

This split is **sequential** (first 80%, next 10%, last 10%).  
It does **not** shuffle first.

In real projects you usually:

```text
shuffle clean  →  then split train / val / test
```

so one category does not dominate only the end of the list.

In **this script**, we only prepare the three lists and print their sizes.  
We do not train a model yet — but the split is the standard next step before ML.

---

## Final prints

```python
print(f"train={len(train):,}  val={len(val):,}  test={len(test):,}")
print("Done.")
```

Shows how big each split is, then exits cleanly.

---

## Map: script steps → dataset ideas

| Script step | Dataset concept |
|-------------|-----------------|
| `load_dataset(...)` | Getting a real dataset |
| Filter price `$1–$1000` | Cleaning / curation |
| Peek at `dataset[0]` | Exploring rows / columns |
| `train` / `val` / `test` | Proper ML splits |

---

## How to run

```bash
python amazon_appliances_dataset_simple.py
```

Needs:

- `datasets` (for this Amazon script, `datasets==3.6.0` is safest)
- `python-dotenv`
- `huggingface_hub`
- `HF_TOKEN` in `.env`
