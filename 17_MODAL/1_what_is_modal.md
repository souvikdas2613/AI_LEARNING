# What is Modal?

Chapter notes (folder `17_MODAL`).

**Modal** ([modal.com](https://modal.com)) is a platform for running **Python in the cloud** without managing your own servers. You write normal Python, decorate functions, and Modal runs them on **containers** in Modal’s infrastructure — often with **GPUs** when you need them.

For LLM work, Modal is useful when your laptop is too slow or low on memory, but you still want code in a repo/notebook that **calls** cloud compute on demand.

Related in this repo: [`16_LORA`](16_LORA/) (fine-tuning concepts) · [`8_GOOGLE_COLAB`](../8_GOOGLE_COLAB/what_is_google_colab.md) (another way to get GPUs).

---

## The problem Modal solves

| Approach | You manage | Good for |
|----------|------------|----------|
| **Local** | GPU drivers, CUDA, disk, RAM | Small models, quick tests |
| **Colab** | Notebook session, timeouts | Interactive experiments |
| **Modal** | Mostly **code + account**; Modal runs containers | **Deployed** functions, agents, batch jobs, GPU inference |

Think of Modal as: **“run this Python function in the cloud, with this image and this GPU.”**

---

## Core ideas (mental model)

```text
Your laptop / notebook
        │
        │  import modal, define app
        ▼
   modal.App  +  @app.function(...)
        │
        │  .remote()  →  runs on Modal’s container (maybe GPU)
        │  .local()   →  runs on your machine (debug)
        ▼
   Result comes back to your script
```

| Term | Meaning |
|------|---------|
| **`modal.App("name")`** | **Dashboard / project name** on Modal — not the same as your `def` function name |
| **`app`** | Python variable holding the `App`; **`@app.function`** registers the next function on it |
| **`@app.function(...)`** | **Required** to register a function with Modal (image, GPU, secrets) so `.remote()` works — see [`2_hello_py.md`](2_hello_py.md#why-appfunction-decorator-is-needed) |
| **`.remote()`** | Execute on Modal’s infrastructure |
| **`.local()`** | Execute in your current process (same code path, no cloud) |
| **Image** | OS + packages baked into the container (like a Dockerfile) |
| **Secret** | Named key/value store on Modal (e.g. `HF_TOKEN`) — not in git |
| **Region** | Optional, e.g. `region="eu"` — may affect latency and billing |

Example pattern (simplified):

```python
import modal

app = modal.App("example")

@app.function()
def hello():
    return "Hello from Modal"

# In a notebook or script:
with app.run():
    print(hello.local())   # your machine
    print(hello.remote())  # Modal cloud
```

**`App("example")` vs `def hello()`:** the string in `App(...)` is only for Modal’s UI. The decorator uses the variable **`app`**. Details: [`2_hello_py.md` — App name vs function name](2_hello_py.md#app-name-vs-function-name-not-the-same-thing).

---

## Install and fix `ModuleNotFoundError: No module named 'modal'`

The Python package is **`modal`**. It is **not** included in every conda env by default.

Use the **same environment** as your notebook kernel (e.g. `my-proj`):

```bash
conda activate my-proj
pip install "modal>=1.1.4"
```

Verify:

```bash
python -c "import modal; print(modal.__version__)"
```

In Cursor/VS Code: pick the kernel that matches that env, then **restart the kernel** after installing.

---

## Authentication (API tokens)

Modal needs to know **who you are** before it runs `.remote()` workloads.

1. Sign up at [modal.com](https://modal.com).
2. **Settings → API Tokens → New Token**.
3. Either run the CLI (course repos often use `uv run modal token set ...`) **or** put tokens in `.env`:

```bash
MODAL_TOKEN_ID=ak-...
MODAL_TOKEN_SECRET=as-...
```

4. In Python: `load_dotenv(override=True)` before calling Modal.

CLI alternative:

```bash
modal token set --token-id ak-... --token-secret as-...
```

If auth fails, check that the token file or env vars are visible to the **same** user/env that runs the notebook.

---

## Hugging Face on Modal (secrets)

Downloading **gated** models inside a Modal container needs `HF_TOKEN` **on Modal**, not only on your laptop.

Typical setup:

| Modal secret **name** | Key inside secret | Value |
|----------------------|-------------------|--------|
| `huggingface-secret` | `HF_TOKEN` | `hf_...` |

Your Modal function references that secret by name so the container sees `HF_TOKEN` at runtime. Create it in the Modal dashboard under **Secrets**.

---

## How is Modal different from Google Colab?

Colab basics: [`8_GOOGLE_COLAB/what_is_google_colab.md`](../8_GOOGLE_COLAB/what_is_google_colab.md).

Both give you **cloud compute** (often GPUs) for AI. The **experience and purpose** are different.

### One-sentence each

| | In one line |
|---|-------------|
| **Colab** | A **notebook in the browser** — you live inside cells on Google’s VM until the session ends. |
| **Modal** | **Python functions in your repo** — your laptop (or CI) **calls** short-lived containers when you run `.remote()`. |

### Analogy

**Colab** = you **sit at Google’s desk**: open a notebook, run cells, everything happens on that one cloud machine while the runtime is connected.

**Modal** = you **phone a workshop**: your script says “run `predict_price()` on a GPU,” Modal spins up a container, returns the result, container goes away. You are not required to work inside a notebook on their UI.

### Side-by-side

| Question | Google Colab | Modal |
|----------|--------------|--------|
| **Where do you write code?** | Mostly in the Colab web UI (`.ipynb`) | `.py` files, local IDE, notebooks that *call* Modal |
| **Where does GPU code run?** | On the **Colab runtime** attached to that notebook | On **Modal containers** triggered by decorated functions |
| **How do you “start” GPU work?** | Runtime → Change runtime type → GPU → run cells | `with app.run(): fn.remote()` (or deploy an app) |
| **Session lifetime** | Disconnect / idle → **runtime dies**; reinstall packages unless you saved | Each job is a **fresh container**; image defines packages |
| **Sharing** | Share notebook link; others run your cells | Share **code**; they use their Modal account + your app name |
| **Best for learning** | Pipelines, plots, step-by-step labs | **Agents**, APIs, “call cloud from my project” |
| **Typical cost** | Free tier + Colab Pro limits | Pay per compute time (see Modal pricing) |
| **Secrets** | Colab secrets / `userdata` / paste in cell (careful) | Modal **Secrets** dashboard, injected into containers |

### Same task, two workflows

**Fine-tune or try a model in a lab (interactive):**

```text
Colab: open notebook → pip install → load model on GPU → train/eval in cells
```

**Run a specialist model from an agent on your laptop:**

```text
Modal: agents/specialist.py defines @app.function(gpu=...) 
       → notebook on WSL calls specialist.predict.remote(description)
       → GPU work happens on Modal, answer returns to you
```

Week-style **capstone agent stacks** often use Modal so the **orchestrator** can stay light while **heavy steps** run in the cloud on demand.

### When to prefer which

| Prefer **Colab** when… | Prefer **Modal** when… |
|------------------------|-------------------------|
| You want zero local GPU setup | You want GPU from **local** code or a multi-file project |
| You are learning in **one notebook** | You are building **functions/services** agents call |
| You need quick plots and “run all cells” | You need **repeatable** deploys and secrets for production-like flows |
| Free tier is enough for the experiment | You accept metered cloud billing for on-demand GPUs |

Many people use **both**: Colab for experiments, Modal (or similar) when the project outgrows a single notebook session.

### Modal vs Colab vs local (summary table)

| | Local | Colab | Modal |
|---|--------|--------|--------|
| Setup | Hardest (GPU drivers) | Easy tab in browser | Account + `pip install modal` |
| Long-running agents | Limited by your hardware | Session limits | Designed for **serverless** jobs |
| “Call GPU from my code” | You already have GPU | Notebook must stay connected | `.remote()` from any machine |
| Cost | Hardware you own | Free tier + limits | Pay per use |

---

## Practice in this folder

| File | Notes |
|------|--------|
| [`hello.py`](hello.py) | Minimal Modal app (container + `hello()`) |
| [`2_hello_py.md`](2_hello_py.md) | Line-by-line explanation of `hello.py` |
| [`TEST_MODAL.py`](TEST_MODAL.py) | Run `hello.local()` and `hello.remote()` |
| [`3_test_modal_py.md`](3_test_modal_py.md) | Line-by-line explanation of `TEST_MODAL.py` |
| [`llama.py`](llama.py) | **Llama 3.2 3B Instruct** — one Q&A on Modal (CPU default, no LoRA) |
| [`4_llama_py.md`](4_llama_py.md) | `llama.py` explained (tokenizer, torch, image, `hf-secret`) |
| [`TEST_MODAL_LLAMA.py`](TEST_MODAL_LLAMA.py) | One question → `generate.remote()` → print **Answer:** only |
| [`5_test_modal_llama_py.md`](5_test_modal_llama_py.md) | `TEST_MODAL_LLAMA.py` line by line |

## Typical workflow for a learner

1. Install `modal` in your env.
2. Set Modal tokens (CLI or `.env`).
3. Run [`TEST_MODAL.py`](TEST_MODAL.py) — `.local()` then `.remote()` ([`3_test_modal_py.md`](3_test_modal_py.md)).
4. Run [`TEST_MODAL_LLAMA.py`](TEST_MODAL_LLAMA.py) — simple Llama inference ([`4_llama_py.md`](4_llama_py.md), [`5_test_modal_llama_py.md`](5_test_modal_llama_py.md)); optional `gpu="T4"` on `@app.function` if you need speed.
5. Store **HF_TOKEN** as Modal **Secret** `hf-secret` for gated models (not in git).

---

## Quick recap

1. **Modal** = run Python functions in the cloud via `modal.App` and `@app.function`.  
2. **`pip install modal`** fixes the missing-module error; match notebook kernel to that env.  
3. **Tokens** authenticate your account; **Secrets** inject `HF_TOKEN` etc. into containers.  
4. **`.remote()`** = cloud; **`.local()`** = debug on your machine.  
5. Use Modal when you need **scalable GPU jobs** without owning a big GPU box.

---

## Official docs

- [Modal docs](https://modal.com/docs)  
- [GPU guide](https://modal.com/docs/guide/gpu)  
- [Secrets](https://modal.com/docs/guide/secrets)  
- [Region selection](https://modal.com/docs/guide/region-selection)
