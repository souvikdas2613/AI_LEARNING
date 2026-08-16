# Quantization

Chapter notes for **Souvik’s** AI learning journey (folder `9_QUANTIZATION`).

Related: [`7_HUGGING_FACE/what_is_huggingface.md`](../7_HUGGING_FACE/what_is_huggingface.md) — loading Hub models with Transformers.

---

## Index

| # | Topic |
|---|--------|
| 1 | [What is quantization?](#1-what-is-quantization) |
| 2 | [Why bother?](#2-why-bother) |
| 3 | [8-bit and 4-bit — what happens to accuracy?](#3-8-bit-and-4-bit--what-happens-to-accuracy) |
| 4 | [Bits and Bytes + Hugging Face](#4-bits-and-bytes--hugging-face) |
| 5 | [Config knobs (plain English)](#5-config-knobs-plain-english) |
| 6 | [Example config shape](#6-example-config-shape) |
| 7 | [What’s next — QLoRA](#7-whats-next--qlora) |
| — | Practice notebook: [`colab_quantization_explained.ipynb`](./colab_quantization_explained.ipynb) (Colab GPU — 4-bit load) |

---

## 1. What is quantization?

**Quantization** means: when you load a model into memory, you store its **weights with fewer bits** than the full training precision.

Usually model weights are **32-bit floating-point** numbers (`float32`).

Quantization loads them as something smaller, for example:

| Precision | Rough idea |
|-----------|------------|
| 32-bit (`float32`) | Full / default heavy |
| 16-bit (`float16` / `bfloat16`) | Half size-ish, common on GPU |
| **8-bit** | Much lighter |
| **4-bit** | Even lighter (half a byte per weight) |

```text
Same model idea
  32-bit weights  →  big RAM / VRAM
   8-bit weights  →  smaller
   4-bit weights  →  smallest of these
```

You are **not** changing the architecture (layers, attention, etc.).  
You are changing **how precisely each weight number is stored** when loaded.

---

## 2. Why bother?

Large models are heavy. Quantization helps you:

- **Fit** a bigger model into limited GPU / RAM  
- **Load** faster (less data to move)  
- Often **run** with better memory behavior  

Especially useful when:

- Colab free GPU is tight  
- Laptop VRAM is small  
- You want to try a 7B+ model without maxing memory  

---

## 3. 8-bit and 4-bit — what happens to accuracy?

Surprising part for many people:

- Dropping to **8 bits** usually does **not** hurt accuracy as much as you’d fear  
- Going to **4 bits** is still often **usable**, with some accuracy loss that many tasks can tolerate  

So the tradeoff is:

```text
fewer bits  →  less memory, faster-ish to load
            →  some quality risk (usually mild at 8-bit; more at 4-bit)
```

“Tolerable” depends on your task — always smoke-test the model after quantizing.

---

## 4. Bits and Bytes + Hugging Face

In practice (Hugging Face world), quantization is often done with:

| Piece | Role |
|-------|------|
| **`bitsandbytes`** | Library that does the low-bit loading math |
| **`transformers`** | Loads the Hub model and applies the BitsAndBytes config |

Flow:

```text
BitsAndBytesConfig(...)  →  tell Transformers how to quantize
AutoModel...from_pretrained(..., quantization_config=...)  →  load lighter weights
```

You create a **Bits and Bytes configuration object** that lists the quantization settings, then pass it when loading the model.

---

## 5. Config knobs (plain English)

| Setting | Meaning |
|---------|---------|
| `load_in_4bit=True` | Load weights in **4-bit** |
| `load_in_8bit=True` | Load weights in **8-bit** (use one style, not both at once) |
| `bnb_4bit_use_double_quant=True` | **Double quantization** — quantize again to save a bit more memory, usually tiny accuracy hit |
| `bnb_4bit_compute_dtype=torch.bfloat16` | Do the **math** in `bfloat16` for better GPU performance while weights stay 4-bit |

**Double quantization (simple):**  
Weights are compressed once, then that compressed form is compressed a little more → extra memory savings.

**Compute dtype vs storage:**  
Weights may be stored in 4-bit, but calculations can still run in a richer type like `bfloat16`.

---

## 6. Example config shape

Illustrative pattern (exact imports/model ids will match your day-4 / Colab code):

```python
import torch
from transformers import BitsAndBytesConfig

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)
```

Then that `quant_config` is passed into `from_pretrained(...)` as `quantization_config=quant_config`.

Needs:

- GPU runtime (typical for bitsandbytes 4-bit / 8-bit)  
- Packages: `transformers`, `bitsandbytes`, and a CUDA-capable PyTorch  

After loading, check size with:

```python
print(model.get_memory_footprint() / 1e6, "MB")
print(torch.cuda.memory_allocated() / 1e9, "GB allocated")
```

See the Colab notebook **section 3** for a full footprint + rough FP32 comparison.

---

## 7. What’s next — QLoRA

Later you’ll meet **QLoRA**: a **fine-tuning** method that uses **quantization** so you can adapt large models with much less memory.

```text
Quantization (here)  →  load big models lighter
QLoRA (later)        →  fine-tune while keeping them light
```

One-line memory aid:

> **Quantization = store weights with fewer bits so big models fit and move faster.**

---

## Quick recap

1. Default weights are often 32-bit floats  
2. Quantization loads 8-bit or 4-bit instead  
3. Accuracy drop is often smaller than people expect (especially 8-bit)  
4. Hugging Face uses **BitsAndBytesConfig** + Transformers  
5. Double quant + `bfloat16` compute are common 4-bit settings  
6. QLoRA builds on this idea for fine-tuning  
