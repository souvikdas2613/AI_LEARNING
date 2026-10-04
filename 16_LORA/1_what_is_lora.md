# LoRA — Low-Rank Adaptation

Chapter notes (folder `16_LORA`).

**LoRA** (Low-Rank Adaptation) is a **parameter-efficient fine-tuning (PEFT)** method. Instead of updating all of a large model’s weights, LoRA inserts small trainable matrices into certain layers — usually the **attention** layers (`q_proj`, `k_proj`, `v_proj`, `o_proj`, and sometimes MLP linears).

That means:

- You **freeze** the base model (LLaMA, GPT, BERT, Mistral, etc.).
- You **train only** the LoRA adapters — tiny **rank-decomposed** matrices **A** and **B**.
- At **inference**, base weights and LoRA weights are **combined** → a fine-tuned behavior with far fewer trainable parameters than full fine-tuning.

This chapter follows [`15_MODEL_FINE_TUNING`](../15_MODEL_FINE_TUNING/1_fine_tuning_in_llm.md) (why fine-tune at all) and connects to [`9_QUANTIZATION`](../9_QUANTIZATION/what_is_quantization.md) (load big models in 4-bit → **QLoRA**).

---

## Why LoRA is useful

- **Fast training** — you might train millions of adapter parameters instead of billions in the full model.
- **Low memory** — practical to fine-tune many LLMs on a **single GPU** (especially with QLoRA).
- **Composable** — swap different LoRA adapter checkpoints on the **same** base model (e.g. one adapter for captioning, another for summarization).

---

## ◆ LoRA Formula

Instead of updating a full weight matrix $W \in \mathbb{R}^{d \times k}$, LoRA approximates the update as:

$$
W' = W + \Delta W, \quad \Delta W = AB
$$

where:

- $A \in \mathbb{R}^{d \times r},$
- $B \in \mathbb{R}^{r \times k},$

and $r \ll \min(d, k)$.

So the number of trainable parameters is drastically reduced.

---

## The problem LoRA solves

**Full fine-tuning** updates all parameters in the base model (often billions).

| Approach | What you train | Memory | Typical use |
|----------|----------------|--------|-------------|
| Full fine-tuning | Every weight in the model | Very high | You own the stack and have big GPUs |
| **LoRA** | Small adapter matrices on chosen layers | Much lower | Adapt open models on one GPU |
| Prompt / RAG only | No weight updates | Lowest | Knowledge or light behavior changes |

LoRA is about **behavior and style** on a task — same idea as fine-tuning in chapter 15 — but with far fewer trainable parameters.

---

## Idea in plain language (forward pass)

A transformer linear layer is a matrix multiply. With LoRA, the forward pass still uses frozen **W**, plus the adapter path:

```text
  h = W · x  +  (α/r) · B · A · x
      ↑              ↑
   frozen         trained (small)
```

At inference you can:

- **Merge** \(\Delta W\) into **W** once (`W' = W + ΔW`) for speed, or  
- Keep adapters separate and **hot-swap** different LoRA files for different tasks.

Higher **rank** `r` → more adapter capacity and more memory; lower `r` → smaller and cheaper.

---

## Key terms

| Term | Meaning |
|------|---------|
| **Rank (`r`)** | Size of the low-rank adapter; common values: 8, 16, 32, 64 |
| **`lora_alpha`** | Scaling factor (often `2 × r`); affects how strongly adapters influence the layer |
| **Target modules** | Which layers get adapters — often `q_proj`, `v_proj`, sometimes all linear layers in attention/MLP |
| **PEFT** | *Parameter-Efficient Fine-Tuning* — family of methods (LoRA is one). Hugging Face **`peft`** library implements LoRA and others |
| **Adapter weights** | The saved LoRA checkpoint (small `.safetensors` / adapter folder), not the full base model |

---

## LoRA vs full fine-tuning vs QLoRA

```text
Full fine-tuning     →  update every parameter (heavy)

LoRA                 →  freeze base model, train small adapters (lighter)

QLoRA                →  LoRA + quantized base model (4-bit load, adapters in higher precision)
```

**QLoRA** is the usual combo on a laptop or Colab GPU. Full walkthrough: [`2_what_is_qlora.md`](2_what_is_qlora.md). Quantization basics: [chapter 9](../9_QUANTIZATION/what_is_quantization.md).

---

## When LoRA is a good fit

LoRA works well when you want the model to:

- Follow a **consistent format** (JSON, bullet lists, ticket templates)
- Adopt a **tone or role** (support agent, reviewer)
- Improve on a **narrow task** (classification labels, extraction patterns)
- Learn from **hundreds to tens of thousands** of examples — not millions

LoRA is **not** a replacement for RAG when the answer depends on **fresh or private documents** you did not train on. See the RAG vs fine-tuning table in [fine-tuning notes](../15_MODEL_FINE_TUNING/1_fine_tuning_in_llm.md).

Often the best production pattern is still:

```text
RAG (current facts)  +  LoRA-tuned model (how to answer)
```

---

## Typical workflow (open models)

1. Pick a base model (e.g. on Hugging Face Hub).
2. Prepare data (same chat / instruction JSONL ideas as [`simple_finetune.ipynb`](../15_MODEL_FINE_TUNING/simple_finetune.ipynb)).
3. Load model — optionally **4-bit** for QLoRA.
4. Attach **LoRA** config (`peft` + `transformers` / `trl`).
5. Train for a few epochs; watch validation loss.
6. Save **adapter only**; load base + adapter for inference.

Tools people use: **Hugging Face PEFT**, **TRL** (`SFTTrainer`), **Unsloth** (faster LoRA), **Axolotl**, **LLaMA-Factory**.

---

## Hyperparameters (starting points)

General intro (parameters vs hyperparameters, `n_epochs`, `batch_size`): [`3_hyperparameters.md`](3_hyperparameters.md).

These LoRA-specific values are rules of thumb, not laws — always validate on your data.

| Setting | Starter idea |
|---------|----------------|
| `r` | 8 or 16 for small datasets; 32–64 if underfitting |
| `lora_alpha` | Often `16` when `r=8`, or `2 × r` |
| Learning rate | Often `1e-4` to `2e-4` for LoRA (higher than full-model FT) |
| Epochs | 1–3; stop if validation degrades |
| Batch size | As large as GPU allows; use gradient accumulation if needed |

---

## Quick recap

1. LoRA **freezes** the pre-trained model and trains **small** adapter matrices.  
2. It needs **much less** GPU memory than full fine-tuning.  
3. **QLoRA** = quantized base + LoRA — the practical path from chapter 9.  
4. Use LoRA for **behavior and format**; use **RAG** for **changing knowledge** at query time.  
5. Saved artifacts are usually **adapter weights**, reusable on top of the same base model.

---

## What’s next in this folder

- Notes: [`2_what_is_qlora.md`](2_what_is_qlora.md) — what the **Q** means, LoRA vs QLoRA, RAG + QLoRA  
- Notes: [`3_hyperparameters.md`](3_hyperparameters.md) — training controls vs learned weights  
- Later: hands-on notebook (e.g. Colab QLoRA on a small open model)
