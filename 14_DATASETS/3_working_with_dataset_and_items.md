# `working_with_DATASET.py` + `items.py` — explained together

Chapter notes (folder `14_DATASETS`).

| File | Role |
|------|------|
| [`working_with_DATASET.py`](./working_with_DATASET.py) | Load Amazon Appliances data, explore rows, build a list of `Item`s |
| [`items.py`](./items.py) | `Item` class — clean one product and build a **training prompt** |

Related simpler script: [`amazon_appliances_dataset_simple.py`](./amazon_appliances_dataset_simple.py) + [`2_amazon_appliances_dataset_simple.md`](./2_amazon_appliances_dataset_simple.md)

---

## Big idea

```text
Hugging Face Amazon dataset (raw row)
              ↓
     working_with_DATASET.py
              ↓
         Item(datapoint, price)   ← items.py
              ↓
   cleaned text + training prompt
   "How much does this cost... Price is $123.00"
```

The simple script stops at: clean dicts + train/val/test lists.  
**This pair goes further:** each kept product becomes an `Item` ready for **price-prediction training**.

### Theory note — this is curation, not training

These two files are an example of **data curation** (prepare clean examples / prompts).  
They are **not** model training (no weight updates, no `trainer.train()`).

Theory: [`1_what_is_a_dataset.md`](./1_what_is_a_dataset.md) → section **“What is data curation?”**

```text
Collect → Curate → Train / Evaluate
              ↑
     working_with_DATASET.py + items.py
```

---

## How the two files connect

```python
from items import Item
...
item = Item(datapoint, price)
if item.include:
    items.append(item)
```

| Piece | Meaning |
|-------|---------|
| `from items import Item` | Import the class from `items.py` in the **same folder** |
| `Item(datapoint, price)` | Build one cleaned product object |
| `item.include` | `True` only if text is long enough / useful enough |
| `items.append(item)` | Keep that object for later use |

So:

- `working_with_DATASET.py` = **driver / main script**
- `items.py` = **helper class** that does the hard cleaning + prompt work

---

## Where `Item` / its functions are called

`items.py` only **defines** the class.  
All calls happen in [`working_with_DATASET.py`](./working_with_DATASET.py).

### 1. Import the class

```python
from items import Item
```

### 2. Create an `Item` (this triggers the cleaning chain)

```python
item = Item(datapoint, price)
if item.include:
    items.append(item)
```

That one constructor call runs this inside `items.py`:

```text
Item(datapoint, price)
        ↓
   __init__(data, price)
        ↓
   parse(data)
        ↓
   scrub(...) / scrub_details()
        ↓
   make_prompt(text)     ← only if text/tokens are good enough
        ↓
   include = True
```

You do **not** call `parse`, `scrub`, or `make_prompt` yourself from the main script.  
They run automatically when you write `Item(...)`.

### 3. Use the finished object later

```python
print(items[0])                 # calls __repr__
print(items[0].prompt)          # attribute set by make_prompt
print(items[0].test_prompt())   # method call — price digits removed
```

| Code in `working_with_DATASET.py` | What runs in `items.py` |
|-----------------------------------|-------------------------|
| `Item(datapoint, price)` | `__init__` → `parse` → scrub helpers → maybe `make_prompt` |
| `item.include` | flag set during `parse` |
| `print(items[0])` | `__repr__` |
| `items[0].prompt` | training string (already built) |
| `items[0].test_prompt()` | **explicit method call** for inference-style prompt |

**Summary:** from the main file you only write `Item(...)`, `.include`, `.prompt`, and `.test_prompt()`. Cleaning and prompt building happen inside the class.

---

# Part A — `working_with_DATASET.py`

## A1. Setup notes at the top

```python
##  pip install datasets==3.6.0
#   DATA SET Used from HUGGING FACE
#   https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023
```

| Note | Why |
|------|-----|
| `datasets==3.6.0` | Newer `datasets` may reject this Amazon loader script |
| Hub URLs | Where the data lives on Hugging Face |

Dataset page:  
https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023

---

## A2. Imports + login

```python
import os
from dotenv import load_dotenv
from huggingface_hub import login
from datasets import load_dataset, Dataset, DatasetDict
import matplotlib.pyplot as plt

from items import Item

load_dotenv(override=True)
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')
os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN', 'your-key-if-not-using-env')

hf_token = os.environ['HF_TOKEN']
login(hf_token)
```

| Piece | Meaning |
|-------|---------|
| `load_dotenv` | Read `.env` into environment |
| `login(hf_token)` | Authenticate with Hugging Face |
| `load_dataset` | Download / open Hub datasets |
| `Dataset`, `DatasetDict` | Imported but **not used yet** in this short script |
| `matplotlib.pyplot` | Imported but **not used yet** in this short script |
| `from items import Item` | Need `items.py` beside this file |
| `OPENAI_API_KEY` | Loaded here; **not used** in the rest of this file (for later steps) |

`.env` should contain at least:

```text
HF_TOKEN=hf_...
```

---

## A3. Load Appliances metadata

```python
dataset = load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023",
    "raw_meta_Appliances",
    split="full"
)
```

| Argument | Meaning |
|----------|---------|
| `"McAuley-Lab/Amazon-Reviews-2023"` | Dataset repo on HF |
| `"raw_meta_Appliances"` | Config = Appliances product metadata |
| `split="full"` | Full split |

Same idea as the simple script.  
Tip: if loading fails on script datasets, add `trust_remote_code=True` and use `datasets==3.6.0`.

---

## A4. Peek at one row

```python
print("DATASET LENGTH IS :     " + str(len(dataset)))

datapoint = dataset[2]

print(datapoint["title"])
print(datapoint["description"])
print(datapoint["features"])
print(datapoint["details"])
print(datapoint["price"])
```

| Piece | Meaning |
|-------|---------|
| `len(dataset)` | How many raw product rows |
| `dataset[2]` | 3rd row (0-based index) |
| `title` / `description` / `features` / `details` / `price` | Typical metadata fields |

This is exploration: “What does one Amazon product look like?”

---

## A5. Count how many rows have a price

```python
prices = 0
for datapoint in dataset:
    try:
        price = float(datapoint["price"])
        if price > 0:
            prices += 1
    except ValueError as e:
        pass

print(f"\nThere are {prices:,} with prices which is {prices/len(dataset)*100:,.1f}%")
```

| Piece | Meaning |
|-------|---------|
| `float(...)` | Price must be a real number |
| `price > 0` | Ignore zero / nonsense |
| `except ValueError` | Skip empty / non-numeric prices |
| `%` print | What fraction of the dataset is usable for price work |

Many rows have missing or junk prices — this measures that.

---

## A6. Build `Item` objects (the important loop)

```python
items = []
for datapoint in dataset:
    try:
        price = float(datapoint["price"])
        if price > 0:
            item = Item(datapoint, price)
            if item.include:
                items.append(item)
    except ValueError as e:
        pass

print(f"\nThere are {len(items):,} items")
```

Flow for each row:

```text
raw datapoint
    ↓
valid price > 0 ?
    ↓ yes
Item(datapoint, price)   # cleaning happens inside items.py
    ↓
item.include == True ?   # enough useful text / tokens
    ↓ yes
append to items list
```

So `items` is **smaller and cleaner** than `dataset`.  
Not every priced product becomes an `Item` — only those that pass `Item`’s quality checks.

---

## A7. Inspect the first Item and its prompts

```python
print(items[0])
print(items[0].prompt)
print(items[0].test_prompt())
```

| Call | What you see |
|------|----------------|
| `items[0]` | Short form via `__repr__`: `<Title = $price>` |
| `.prompt` | **Training** text including the answer price |
| `.test_prompt()` | Same text **without** the real price (model must predict) |

Example shape of training prompt:

```text
How much does this cost to the nearest dollar?

<cleaned title + description + features...>

Price is $149.00
```

Test prompt ends at:

```text
Price is $
```

so the model must complete the number.

---

# Part B — `items.py` (`Item` class)

## B1. Constants

```python
BASE_MODEL = "meta-llama/Meta-Llama-3.1-8B"

MIN_TOKENS = 150
MAX_TOKENS = 160

MIN_CHARS = 300
CEILING_CHARS = MAX_TOKENS * 7
```

| Constant | Meaning |
|----------|---------|
| `BASE_MODEL` | Tokenizer to count/cut text the way Llama 3.1 would |
| `MIN_TOKENS` | Too short → not enough signal → reject (`include=False`) |
| `MAX_TOKENS` | Truncate long products so prompts stay similar length |
| `MIN_CHARS` | Character gate before tokenization |
| `CEILING_CHARS` | Rough character cap before tokenization (`160 * 7`) |

### Is `BASE_MODEL` from Hugging Face?

Yes. That string is a **Hugging Face model id**:

```text
meta-llama/Meta-Llama-3.1-8B
    │              │
    │              └── model name
    └── organization on Hugging Face
```

Hub page:

**https://huggingface.co/meta-llama/Meta-Llama-3.1-8B**

In `items.py` it is used to load the **tokenizer** only:

```python
AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
```

So this script downloads/uses the Llama 3.1 **tokenizer** from HF to **count and truncate tokens**.  
It does **not** load/run the full 8B model for generation here.

Important notes:

| Point | Detail |
|-------|--------|
| Gated model | Meta Llama often requires accepting the license on the Hub page |
| Token | Need a valid `HF_TOKEN` (and Hub access approved) |
| First run | Tokenizer files download into the local HF cache |
| Purpose here | Match how Llama would tokenize the product text before training |

---

## B2. Class fields + tokenizer

```python
class Item:
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    PREFIX = "Price is $"
    QUESTION = "How much does this cost to the nearest dollar?"
    REMOVALS = [...]
```

| Piece | Meaning |
|-------|---------|
| `tokenizer` | Shared Hugging Face tokenizer for the class |
| `PREFIX` | Answer prefix used in prompts |
| `QUESTION` | Question asked in every prompt |
| `REMOVALS` | Noisy phrases to strip from `details` |

Instance fields (set per product):

| Field | Meaning |
|-------|---------|
| `title` | Product title |
| `price` | Numeric price |
| `details` | Raw details blob |
| `prompt` | Full training string |
| `include` | Keep this item? (`True`/`False`) |
| `token_count` | Tokens in the final prompt |

---

## B3. `__init__` — create one Item

```python
def __init__(self, data, price):
    self.title = data['title']
    self.price = price
    self.parse(data)
```

Saves title + price, then calls `parse()` to clean text and maybe set `include=True`.

---

## B4. Cleaning helpers

### `scrub_details()`

Removes boring boilerplate from details using `REMOVALS`  
(e.g. “Batteries Included?”, “Best Sellers”, …).

### `scrub(stuff)`

| Step | Meaning |
|------|---------|
| Regex cleanup | Collapse weird punctuation / whitespace |
| Drop long alphanumeric codes | Words length ≥ 7 that contain digits (often SKUs / model junk) |

Goal: keep **human-useful** product language, drop noise that leaks IDs.

---

## B5. `parse(data)` — decide include + build prompt

```text
join description
  + features
  + scrubbed details
        ↓
long enough in characters?  (MIN_CHARS)
        ↓
truncate chars → scrub title+contents
        ↓
tokenize
        ↓
enough tokens? (MIN_TOKENS)
        ↓
truncate to MAX_TOKENS → decode back to text
        ↓
make_prompt(text)
include = True
```

If any gate fails, `include` stays `False` and the main script skips that product.

---

## B6. `make_prompt(text)` — training example

```python
self.prompt = f"{self.QUESTION}\n\n{text}\n\n"
self.prompt += f"{self.PREFIX}{str(round(self.price))}.00"
```

Builds:

```text
How much does this cost to the nearest dollar?

<cleaned product text>

Price is $199.00
```

The model is trained to see the product text and learn to produce the price line.

`round(self.price)` → nearest dollar.

---

## B7. `test_prompt()` — inference-style prompt

```python
return self.prompt.split(self.PREFIX)[0] + self.PREFIX
```

Takes the training prompt and **cuts off the actual price digits**.

Training:

```text
...Price is $199.00
```

Test / ask the model:

```text
...Price is $
```

Same product context; answer hidden.

---

## B8. `__repr__`

```python
return f"<{self.title} = ${self.price}>"
```

So `print(items[0])` is readable.

---

# Side-by-side: simple script vs this pair

| Topic | `amazon_appliances_dataset_simple.py` | `working_with_DATASET.py` + `items.py` |
|-------|----------------------------------------|----------------------------------------|
| Load HF data | Yes | Yes |
| Filter by price | Yes (`$1–$1000`) | Yes (`price > 0`) + stricter text/token gates |
| Store as | plain dicts | `Item` objects |
| Build LLM prompt | No | Yes |
| Train/val/test split | Yes | Not in this file (next step) |
| Needs tokenizer / Llama id | No | Yes (`AutoTokenizer` + `BASE_MODEL`) |

Progression:

```text
1_what_is_a_dataset.md
        ↓
amazon_appliances_dataset_simple.py   ← load / clean / split idea
        ↓
working_with_DATASET.py + items.py    ← turn rows into training prompts
```

---

## How to run

From the `14_DATASETS` folder (so `items.py` imports cleanly):

```bash
cd 14_DATASETS
python working_with_DATASET.py
```

Needs:

- `datasets==3.6.0` (recommended for this Amazon dataset)
- `python-dotenv`, `huggingface_hub`, `transformers`
- `.env` with `HF_TOKEN=...`
- Network the first time (dataset + tokenizer download)

Note: loading the Llama tokenizer may require Hugging Face access to that model id (gated models need a token + license acceptance on the Hub).
