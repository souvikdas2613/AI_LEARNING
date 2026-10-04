# `TEST_MODAL_LLAMA.py` — line by line

Companion to [`TEST_MODAL_LLAMA.py`](TEST_MODAL_LLAMA.py). App definition: [`llama.py`](llama.py) · [`4_llama_py.md`](4_llama_py.md).

---

## Index

| # | Topic |
|---|--------|
| 1 | [What is this for?](#1-what-is-this-for) |
| 2 | [Which file is main?](#2-which-file-is-main) |
| 3 | [Line by line](#3-line-by-line) |
| 4 | [What you should see](#4-what-you-should-see) |
| 5 | [If something fails](#5-if-something-fails) |

---

## 1. What is this for?

**Run:** `python TEST_MODAL_LLAMA.py`

This is the **“Run” button** for the Llama demo:

1. Load Modal tokens from `.env`  
2. Call `generate.remote(QUESTION)` on Modal’s servers  
3. Print **Question** and **Answer** separately  

No LoRA, no training — same role as [`TEST_MODAL.py`](TEST_MODAL.py) for [`hello.py`](hello.py), but for **Llama inference**.

---

## 2. Which file is main?

| File | Role |
|------|------|
| [`llama.py`](llama.py) | **Defines** `app` + `generate()` (Modal + Llama) |
| **This file** | **Executes** `python TEST_MODAL_LLAMA.py` |

No `.local()` — do not load Llama 3B on your laptop in this demo.

```text
llama.py          →  recipe (what Modal runs)
TEST_MODAL_LLAMA  →  main (calls .remote())
```

---

## 3. Line by line

| Line | Code | Explanation |
|------|------|-------------|
| 1 | Docstring | Points to this markdown file. |
| 2 | `import modal` | Client library (`enable_output`, `app.run`). |
| 3–5 | `load_dotenv(override=True)` | Read `.env` (`MODAL_TOKEN_ID`, `MODAL_TOKEN_SECRET`). |
| 7 | `from llama import app, generate` | Import from same folder **`17_MODAL`**. |
| 9 | `QUESTION = "What is 2+2? ..."` | Change to any short question. |
| 11 | `modal.enable_output()` | Stream Modal build/run logs to the terminal. |
| 12 | `with app.run():` | Open a Modal session for this script. |
| 13 | `answer = generate.remote(QUESTION)` | **Blocking** — cloud runs [`llama.py`](llama.py) `generate()`; returns **answer only** (not full echoed prompt). |
| 15–16 | `print("Question:" / "Answer:")` | Easy-to-read output. |

**Not in this file:** `HF_TOKEN` prints, LoRA, manual tokenizer, GPU env vars.

---

## 4. What you should see

```text
✓ App completed. View run at https://modal.com/apps/...
Question: What is 2+2? Reply with only the number.
Answer: 4
```

- Answer may not always be exactly `4` — you are testing **Modal + Llama**, not a calculator.  
- If **Answer** still repeats `2+2 = ?`, you are not on the current [`llama.py`](llama.py) (needs **Instruct**, chat template, and `outputs[0][input_len:]` decode). See [§6 — Why only decode new tokens?](4_llama_py.md#6-why-only-decode-new-tokens).

---

## 5. If something fails

| Error | Check |
|-------|--------|
| `ModuleNotFoundError: modal` | `pip install modal` in active env |
| Modal auth | `MODAL_TOKEN_*` in `.env` |
| Hub / gated model | Modal secret **`hf-secret`** with **`HF_TOKEN`**; Llama license on Hub |
| Secret not found | Secret name must be exactly **`hf-secret`** |
| Slow / timeout | First run downloads 3B on **CPU**; wait or add `gpu="T4"` in `llama.py` (paid) |

Full background: [`4_llama_py.md`](4_llama_py.md).

---

## Quick recap

`.env` → `app.run()` → `generate.remote(QUESTION)` → print **Answer** only. Llama logic lives in **`llama.py`**.
