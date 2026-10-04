# QLoRA — Quantized Low-Rank Adaptation

Chapter notes (folder `16_LORA`). Read first: [`1_what_is_lora.md`](1_what_is_lora.md).

**QLoRA** = **Quantized Low-Rank Adaptation**.

It's a technique for **fine-tuning large language models much more cheaply in GPU memory**.

Quantization background: [`9_QUANTIZATION/what_is_quantization.md`](../9_QUANTIZATION/what_is_quantization.md). RAG vs fine-tuning: [`15_MODEL_FINE_TUNING/1_fine_tuning_in_llm.md`](../15_MODEL_FINE_TUNING/1_fine_tuning_in_llm.md).

---

## Start with LoRA

Normally, fine-tuning means changing a huge number of model parameters:

```text
Base LLM
  ↓
Millions/billions of parameters updated
  ↓
Fine-tuned LLM
```

That's expensive.

**LoRA** freezes the original model and adds small trainable matrices:

```text
                ┌── LoRA adapters ← TRAIN
                │
Input → Base LLM ───────────────→ Output
          ↑
        FROZEN
```

Instead of modifying billions of parameters, you're training a much smaller number of parameters.

---

## Then what does the "Q" mean?

**Quantization.**

Instead of keeping the base model's weights in something like FP16:

```text
16-bit weights
```

QLoRA loads the base model in **4-bit quantized form**:

```text
                 4-bit
                  ↓
Input → Quantized Base Model → Output
                  ↑
             LoRA adapters
             (trainable)
```

So:

> **QLoRA = 4-bit quantized frozen model + trainable LoRA adapters**

This dramatically reduces GPU memory requirements.

---

## Why is this useful?

Imagine you have a large model:

```text
70B parameters
```

Full fine-tuning can require enormous GPU memory.

With QLoRA:

```text
70B model
   ↓
4-bit quantization
   ↓
much smaller memory footprint
   ↓
LoRA adapters trained
```

You can potentially fine-tune models that would otherwise be impractical on a single GPU.

---

## LoRA vs QLoRA

|                       | LoRA               | QLoRA                              |
| --------------------- | ------------------ | ---------------------------------- |
| Base model            | Usually FP16/BF16  | **4-bit quantized**                |
| Base weights trained? | ❌                  | ❌                                  |
| Adapter trained?      | ✅                  | ✅                                  |
| GPU memory            | Lower              | **Even lower**                     |
| Fine-tuning cost      | Lower than full FT | **Very low compared with full FT** |
| Typical use           | LLM customization  | LLM customization with limited GPU |

---

## And this connects directly to your previous question

You asked:

> **"Why fine-tune when RAG can do it?"**

QLoRA doesn't change the answer.

**RAG**:

```text
Model + external knowledge
```

**QLoRA**:

```text
Model + learned specialized behavior
```

For example:

**RAG**

> "Answer using our latest 10,000 product documents."

**QLoRA**

> "Learn to classify support tickets according to our company's classification style."

And you can combine them:

```text
                    ┌── Vector DB
                    │
Question → RAG ─────┤
                    ↓
                QLoRA model
                    ↓
                  Answer
```

---

## For your learning path

Learn **LoRA → QLoRA** conceptually. It's one of the most important modern techniques for adapting open-source LLMs.

Unlike OpenAI self-serve fine-tuning being blocked for many orgs (`403 training_not_available` — see [`simple_finetune.ipynb`](../15_MODEL_FINE_TUNING/simple_finetune.ipynb)), **QLoRA is something you can experiment with yourself** using open-source models such as **Llama**, **Qwen**, or **Granite**, provided you have suitable GPU resources (local or Colab).

---

## Quick recap

1. **LoRA** — frozen base + trainable low-rank adapters.  
2. **QLoRA** — same adapters, but the base is loaded in **4-bit** so memory drops further.  
3. **RAG** adds knowledge at query time; **QLoRA** teaches **behavior** — often used together.  
4. Next: [`3_hyperparameters.md`](3_hyperparameters.md) — epochs, batch size, learning rate vs model weights.
