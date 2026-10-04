# `llama.py` — simple Llama inference (no LoRA)

Companion to `[llama.py](llama.py)`. Runner: `[TEST_MODAL_LLAMA.py](TEST_MODAL_LLAMA.py)` · `[5_test_modal_llama_py.md](5_test_modal_llama_py.md)`.

**Training / LoRA / token datasets:** `[16_LORA](../16_LORA/)` — different step; this folder is **run the model once in the cloud**.

---

## Index


| #   | Topic                                                                                                                               |
| --- | ----------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [What is this for?](#1-what-is-this-for)                                                                                            |
| 2   | [Line by line (](#2-line-by-line-llamapy)`llama.py`[)](#2-line-by-line-llamapy)                                                     |
| 3   | [Why](#3-why-def-generate-and-imports-inside-it) `def generate` [and imports inside it?](#3-why-def-generate-and-imports-inside-it) |
| 4   | [Why tokenizer?](#4-why-tokenizer)                                                                                                  |
| 5   | [Why](#5-why-apply_chat_template) `apply_chat_template`[?](#5-why-apply_chat_template)                                              |
| 6   | [Why only decode](#6-why-only-decode-new-tokens) `outputs[0][input_len:]`[?](#6-why-only-decode-new-tokens)                         |
| 7   | [Why torch + transformers + accelerate?](#7-why-torch--transformers--accelerate)                                                    |
| 8   | [Why](#8-why-imagedebian_slimpip_install) `Image.debian_slim().pip_install(...)`[?](#8-why-imagedebian_slimpip_install)             |
| 9   | [Modal secret](#9-modal-secret-hf-secret) `hf-secret`                                                                               |
| 10  | [Base vs Instruct (your old output)](#10-base-vs-instruct-your-old-output)                                                          |
| 11  | [Run](#11-run)                                                                                                                      |


---



## 1. What is this for?

```text
TEST_MODAL_LLAMA.py  →  generate.remote("What is 2+2? ...")
                              ↓
                         Modal container
                              ↓
                         Llama-3.2-3B-Instruct
                              ↓
                         print Answer: (only the reply)
```

- **Not** fine-tuning, **not** LoRA, **not** QLoRA.  
- **Yes:** one **inference** call — question in, answer text out.  
- `[hello.py](hello.py)` proved Modal works; **this file** runs a **real Llama** the same way (`@app.function` + `.remote()`).


| File                                         | Role                                         |
| -------------------------------------------- | -------------------------------------------- |
| `[llama.py](llama.py)`                       | Defines `app` + `generate()`                 |
| `[TEST_MODAL_LLAMA.py](TEST_MODAL_LLAMA.py)` | **Main program** — calls `generate.remote()` |


---



## 2. Line by line (`llama.py`)



### `generate()` — four steps (read this first)

Modal only runs **this function** in the cloud. Everything inside is normal Hugging Face inference — not Modal magic.

```text
  your question (str)
        │
        ▼
  ┌─────────────────────────────────────┐
  │ 1. Load tokenizer + model (once     │  from_pretrained — big download first time
  │    per cold start)                  │
  └─────────────────────────────────────┘
        │
        ▼
  ┌─────────────────────────────────────┐
  │ 2. apply_chat_template → input_ids  │  "user: What is 2+2?" in Llama 3 format
  └─────────────────────────────────────┘
        │
        ▼
  ┌─────────────────────────────────────┐
  │ 3. model.generate(...)              │  model appends up to 32 answer tokens
  └─────────────────────────────────────┘
        │
        ▼
  ┌─────────────────────────────────────┐
  │ 4. decode only tokens AFTER prompt  │  [prompt_len:] drops the question from output
  └─────────────────────────────────────┘
        │
        ▼
  answer string back to TEST_MODAL_LLAMA.py
```


| Step | Code (roughly)                                              | You can skip worrying about…                                                                 |
| ---- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 1    | `AutoTokenizer` / `AutoModelForCausalLM` `.from_pretrained` | **How** weights load — library handles it; `HF_TOKEN` unlocks gated Hub model.               |
| 2    | `messages` + `apply_chat_template`                          | Special tokens — template adds what Instruct models expect. [§5](#5-why-apply_chat_template) |
| 3    | `model.generate`                                            | Sampling knobs — we use greedy (`do_sample=False`) for a short demo.                         |
| 4    | `new_token_ids[0][prompt_len:]` then `decode`               | Why not return full `generate` output — [§6](#6-why-only-decode-new-tokens).                 |


**Why it looks long:** steps 1–4 are the minimum for *any* local Llama script. Modal adds only the **wrapper** outside the function (`app`, `image`, `secrets`, `@app.function`). Imports sit **inside** `generate` so your laptop never loads 3B weights — [§3](#3-why-def-generate-and-imports-inside-it).

### File setup + each line


| Line(s) | Code                                                 | Explanation                                                                                  |
| ------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 5–6     | `import modal` / `from modal import Image`           | Modal SDK + **container image** recipe.                                                      |
| 8       | `app = modal.App("llama-inference")`                 | App name on [Modal dashboard](https://modal.com/apps). See `[2_hello_py.md](2_hello_py.md)`. |
| 9       | `image = Image.debian_slim().pip_install(...)`       | Cloud VM packages — [§8](#8-why-imagedebian_slimpip_install).                                |
| 10      | `secrets = [...]`                                    | `HF_TOKEN` in container — [§9](#9-modal-secret-hf-secret).                                   |
| 12      | `MODEL = "...-Instruct"`                             | Chat-tuned model (not base completion).                                                      |
| 15      | `@app.function(...)`                                 | “Run the function below on Modal.” No `gpu=` → CPU.                                          |
| 16      | `def generate(question: str) -> str:`                | What `generate.remote(question)` calls.                                                      |
| 17–18   | imports inside function                              | Torch/transformers run **in the container** only.                                            |
| 20–21   | `from_pretrained(MODEL)`                             | Step **1** — load tokenizer + model.                                                         |
| 23–28   | `messages` + `apply_chat_template` → `["input_ids"]` | Step **2** — question → token tensor.                                                        |
| 29      | `prompt_len = input_ids.shape[-1]`                   | Count prompt tokens for step **4** slice.                                                    |
| 31–33   | `generate` → `answer_ids` → `decode`                 | Steps **3** and **4** — new tokens, answer text only.                                        |


---



## 3. Why `def generate` and imports inside it?

```python
def generate(question: str) -> str:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
```



### Why `def generate(...)`?


| Piece           | Why                                                                     |
| --------------- | ----------------------------------------------------------------------- |
| `def generate`  | Only code Modal runs in the cloud when you call `generate.remote(...)`. |
| `question: str` | Text from `[TEST_MODAL_LLAMA.py](TEST_MODAL_LLAMA.py)`.                 |
| `-> str`        | Answer text back to your laptop.                                        |


Without this + `@app.function`, Modal has nothing to execute.

### Why imports **inside** the function?


| Reason                    | Explanation                                                                                |
| ------------------------- | ------------------------------------------------------------------------------------------ |
| Runs in the container     | Imports execute **on Modal’s VM**, where `image.pip_install` put `torch` / `transformers`. |
| Light local import        | `from llama import generate` on your PC does **not** load Llama or PyTorch locally.        |
| Same pattern as `hello()` | `[hello.py](hello.py)` uses `import requests` inside `hello()`.                            |


```text
Laptop: from llama import generate
Modal:  def generate(): import torch; load model; return answer
```

---



## 4. Why tokenizer?

Llama does not read strings — it reads **token ids**.


| Step          | What happens                                 |
| ------------- | -------------------------------------------- |
| Your question | `"What is 2+2? Reply with only the number."` |
| Tokenizer     | text → list of numbers                       |
| Llama         | predicts more numbers                        |
| Tokenizer     | numbers → text                               |


**Removed from this demo:** looping thousands of rows to count tokens for **training** (`[16_LORA](../16_LORA/prepare_sft_prompt_data.ipynb)`). That was **dataset prep**, not one inference call.

---



## 5. Why `apply_chat_template`?

**Instruct** models expect a **chat** layout (user / assistant roles), not a raw string like `2+2 = ?`.

`tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True)` builds the special tokens Llama 3 uses so the model knows: *user asked something → now I should answer as assistant*.

Without it, an instruct model can behave oddly or repeat text.

---



## 6. Why only decode new tokens?

Now:

```python
outputs = model.generate(inputs, ...)
return tokenizer.decode(outputs[0][input_len:], skip_special_tokens=True)
```


| Part           | Meaning                                                         |
| -------------- | --------------------------------------------------------------- |
| `outputs[0]`   | All token ids (question + answer)                               |
| `[input_len:]` | **Slice off** the question part                                 |
| `decode(...)`  | Only the **assistant reply** → cleaner `Answer: 4` style output |


---



## 7. Why torch + transformers + accelerate?

**Simple code** does not mean **no ML libraries**. Llama is a large neural network.


| Package        | Role                                                |
| -------------- | --------------------------------------------------- |
| `torch`        | Runs the math (CPU here; GPU if you add `gpu="T4"`) |
| `transformers` | Load Llama, tokenizer, `generate()`, chat template  |
| `accelerate`   | Often pulled in for loading helpers                 |


```text
question  →  transformers + tokenizer  →  torch  →  answer tokens  →  text
```

Compare `[hello.py](hello.py)`: only needs `requests` because it only calls ipinfo.

**Not doing here:** LoRA training, 4-bit QLoRA config, dataset histograms — that lives under `[16_LORA](../16_LORA/)`.

**Other players:** Ollama on your PC — same idea, different app.

---



## 8. Why `Image.debian_slim().pip_install(...)`?

When you `.remote()`, code runs on a **fresh** Linux VM — not your `conda` env.


| Piece                                                 | Meaning                                                 |
| ----------------------------------------------------- | ------------------------------------------------------- |
| `Image.debian_slim()`                                 | Small Debian base image                                 |
| `.pip_install("torch", "transformers", "accelerate")` | Bake dependencies into the image (reused on later runs) |


Without `image=image` on `@app.function` → `ImportError: No module named 'torch'`.

Installing inside `generate()` on every run would work but be **much slower** than baking the image once.

---



## 9. Modal secret `hf-secret`

**Not a file in this repo.** You create it on Modal:

1. [modal.com](https://modal.com) → **Secrets**
2. Name: `hf-secret` (must match line 10 in `llama.py`)
3. Key: `HF_TOKEN` · Value: `hf_...` from [Hugging Face tokens](https://huggingface.co/settings/tokens)
4. Accept **Llama 3.2** license on the model page on the Hub


| Credentials                             | Where            | For what                                |
| --------------------------------------- | ---------------- | --------------------------------------- |
| `MODAL_TOKEN_ID` / `MODAL_TOKEN_SECRET` | `.env` on laptop | Your script talks to **Modal**          |
| `HF_TOKEN` in `hf-secret`               | Modal dashboard  | **Container** downloads **gated** Llama |


---



## 10. Base vs Instruct (your old output)


| Setup                                       | Typical behavior                        |
| ------------------------------------------- | --------------------------------------- |
| **Base** model + raw `"2+2 = ? "`           | Often **repeats** prompt (what you saw) |
| **Instruct** + chat template + slice answer | **Question / Answer** printout          |


The **code change** was for clearer output; the **Modal pipe** (`.remote()`, `image`, secrets) is the same idea as before.

---



## 11. Run

```bash
cd AI_LEARNING/AI_LEARNING/17_MODAL
python TEST_MODAL_LLAMA.py
```

Edit `QUESTION` in `TEST_MODAL_LLAMA.py` to try other prompts.

First run: image build + model download can take a while on CPU.

If **Answer** repeats `2+2 = ?`, compare your `[llama.py](llama.py)` to this doc (Instruct + `[input_len:]` slice) — [§6](#6-why-only-decode-new-tokens).

---



## Quick recap

1. **Llama 3.2 3B Instruct** on Modal — one question, one answer string.
2. **Tokenizer + torch + transformers** — required to run Llama; not LoRA.
3. `image.pip_install` — libs on empty cloud VM.
4. `hf-secret` — `HF_TOKEN` for Hub.
5. **Chat template +** `[input_len:]` — readable answers, not repeated `2+2 = ?`.
6. **LoRA chapter** = training; this file = **inference only**.

