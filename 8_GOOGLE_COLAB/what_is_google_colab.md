# What Is Google Colab?

Chapter notes for **Souvik’s** AI learning journey (folder `8_GOOGLE_COLAB`).

Website: [https://colab.research.google.com/](https://colab.research.google.com/)

---

## Index

| # | Topic |
|---|--------|
| 1 | [What is Google Colab?](#1-what-is-google-colab) |
| 2 | [Why use Colab for AI / ML?](#2-why-use-colab-for-ai--ml) |
| 3 | [What you need to start](#3-what-you-need-to-start) |
| 4 | [Free tier — what you get and what you don’t](#4-free-tier--what-you-get-and-what-you-dont) |
| 5 | [How to check usage / resources](#5-how-to-check-usage--resources) |
| 6 | [What you can realistically use on free tier](#6-what-you-can-realistically-use-on-free-tier) |
| 7 | [Runtime and GPU](#7-runtime-and-gpu) |
| 8 | [Notebooks — how Colab feels](#8-notebooks--how-colab-feels) |
| — | [Where does pip install put packages?](#where-does-pip-install-put-packages-in-colab) |
| 9 | [Secrets and API tokens](#9-secrets-and-api-tokens) |
| 10 | [Colab vs your local laptop](#10-colab-vs-your-local-laptop) |
| 11 | [Colab + Hugging Face](#11-colab--hugging-face) |
| 12 | [Good habits](#12-good-habits) |
| — | Practice notebook: [`colab_openai_and_hf.ipynb`](./colab_openai_and_hf.ipynb) (OpenAI + HF **API** in one notebook) |

---

## 1. What is Google Colab?

**Google Colaboratory** (Colab) is a free (and optionally paid) cloud notebook environment from Google.

It runs in your browser and gives you:

- a **Jupyter-style notebook** (code cells + markdown cells)  
- a machine in the cloud (CPU, and often **GPU**)  
- easy install of Python packages  
- access from almost any computer with a Google account  

You write Python in cells → press Run → it executes on Google’s servers, not only on your weak laptop CPU.

Many people describe it as:

> **Jupyter Notebook in the cloud, with free GPUs.**

---

## 2. Why use Colab for AI / ML?

Local laptops often struggle with:

- large Hugging Face models  
- GPU-heavy inference  
- slow downloads / limited RAM  

Colab helps because:

| Need | How Colab helps |
|------|------------------|
| GPU | Free/paid access to GPUs (e.g. T4) for model demos |
| Setup | No local CUDA install drama for beginners |
| Sharing | Share a notebook link with others |
| Experiments | Try `transformers` pipelines quickly |
| Learning | Great for Hugging Face / model labs |

For **Souvik’s** path: Colab is especially useful when practicing **Hugging Face pipelines** and heavier models.

---

## 3. What you need to start

1. A **Google account**  
2. Open [https://colab.research.google.com/](https://colab.research.google.com/)  
3. Create a new notebook (`File → New notebook`)  
4. Start coding in cells  

That’s enough for the free tier.

---

## 4. Free tier — what you get and what you don’t

Important truth from Google’s own FAQ:

> Colab resources are **not guaranteed** and **not unlimited**.  
> Usage limits **fluctuate**. Google **does not publish exact quotas** because they change over time.

So free tier is excellent for **learning**, not for guaranteed production GPUs.

### What you typically GET on free tier

| You get | Notes |
|---------|--------|
| Notebooks in the browser | Jupyter-style cells, no local setup |
| CPU runtime | Always the default / fallback |
| GPU access (often **NVIDIA T4**) | When available — not guaranteed |
| Python + `pip install` | Install `transformers`, etc. in a cell |
| Google Drive mount | Save notebooks/files to Drive |
| Sharing notebooks | Share links with others |
| Session length | Often up to about **12 hours** max (depends on usage/availability) |
| Enough power for learning | Pipelines, small/medium model demos, experiments |

### What you typically do NOT get (or cannot rely on)

| You don’t get / can’t rely on | Why it matters |
|-------------------------------|----------------|
| Guaranteed GPU every time | Peak hours → “no GPU available” |
| Guaranteed GPU type | Usually T4 when lucky; can vary |
| Fixed published GPU-hour quota | Limits are dynamic / unpublished |
| Long idle sessions | Idle ~90 minutes often disconnects |
| Permanent disk on the VM | Runtime files vanish when session ends |
| Top GPUs (A100 etc.) | Those are paid / limited priority |
| Unlimited background jobs | Free tier is for interactive notebook use |
| Production SLA | Fine for study; not for always-on apps |

### Free vs paid (simple)

| | **Free** | **Pro / Pro+ / pay-as-you-go** |
|---|----------|--------------------------------|
| Cost | ₹0 | Paid compute units / subscription |
| GPU | Restricted, shared | Higher priority / more options |
| Sessions | Shorter / stricter | Longer / more flexible |
| Best for | Learning, demos | Heavier / more reliable work |

Paid is nice. **Not required** for most of **Souvik’s** learning path.

---

## 5. How to check usage / resources

Google does not show a perfect “you have X GPU hours left this week” meter for free users the way some clouds do.  
You check **current session resources** and **whether GPU is actually attached**.

### A) Check RAM / disk for this session (UI)

1. Open your Colab notebook  
2. Look near the top-right for **RAM / Disk** indicators (resource view)  
3. Click it to see memory and disk usage of the current runtime  

If usage is high, restart runtime or free memory.

### B) Confirm you actually have a GPU

In a code cell:

```python
!nvidia-smi
```

- If you see a GPU table (often **Tesla T4**) → GPU is attached  
- If it errors / no NVIDIA device → you are on CPU only  

Also:

```python
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU")
```

### C) Change / request GPU

1. `Runtime → Change runtime type`  
2. Hardware accelerator → **GPU** (T4 if listed)  
3. Save → reconnect runtime  

If Colab says GPU is unavailable: wait, try later, or continue on CPU for lighter tasks.

### D) If you use paid Colab

Paid plans show **compute unit** balance in account / settings style pages.  
Free tier is mostly “use it until limited / disconnected,” not a fixed dashboard of remaining hours.

### E) Practical “am I hitting limits?” signals

| Signal | Likely meaning |
|--------|----------------|
| Can’t select GPU | Quota busy / exhausted for now |
| Runtime disconnects quickly | Idle timeout or usage limit |
| Very slow jobs on “GPU” runtime | GPU not really utilized / fell back |
| `nvidia-smi` fails | No GPU on this session |

---

## 6. What you can realistically use on free tier

### Good fit (free tier friendly)

- Hugging Face `pipeline` demos (sentiment, summarization, small generation)  
- Small / medium models, especially quantized ones  
- Learning notebooks, tutorials, experiments  
- Whisper / transcription demos (depending on model size)  
- Image demos that fit in ~T4 memory  
- Prototyping code before moving to local/Ollama/OpenAI  

### Risky / often too heavy on free tier alone

- Huge LLMs at full precision  
- Long multi-hour training runs every day  
- Always-on APIs / production bots  
- Expecting the same GPU every morning at peak time  

### Simple strategy for learners

1. Do light work on **CPU** when possible  
2. Switch to **GPU** only when needed  
3. Save outputs to **Drive** often  
4. If GPU denied → pause and retry later, or use smaller model / local Ollama / OpenAI API  

---

## 7. Runtime and GPU

A **runtime** is the cloud machine attached to your notebook.

Common actions:

- `Runtime → Change runtime type`  
- Pick **CPU** or **GPU** (e.g. **T4**)  
- `Runtime → Run all` to run every cell  

For many Hugging Face demos, a free/low-cost **T4 GPU** is enough and results look great.

Important:

- Free GPUs are **shared** — sometimes busy  
- Runtime can **disconnect** if idle too long (~90 minutes is a common experience)  
- Max session often around **12 hours**, then you reconnect (new machine)  
- Files in the runtime can be lost when the session ends (unless saved to Drive)

---

## 8. Notebooks — how Colab feels

Colab notebooks are like Jupyter:

| Cell type | Purpose |
|-----------|---------|
| **Code** | Python that runs when you click ▶ |
| **Text / Markdown** | Notes and explanations |

Useful ideas:

- run cells one by one while learning  
- `!pip install package` in a cell to install libraries  
- print outputs appear under the cell  

Example cell:

```python
print("Hello from Colab!")
```

Install example:

```python
!pip install transformers
```

### Where does `pip install` put packages in Colab?

Packages install into the **current runtime’s Python environment** — the temporary cloud VM Google gave your notebook.

So:

```python
!pip install transformers
```

goes into that session’s site-packages on the **Colab machine**.

| Question | Answer |
|----------|--------|
| On my PC / WSL? | No |
| In Google Drive? | No (not by default) |
| On this Colab runtime? | Yes |
| Survives forever? | No — new/reset runtime → usually reinstall |

**Mental model:** Colab is a rental computer. `pip install` puts packages on that rental computer until the rental ends.

That’s why after **Runtime → Disconnect / factory reset**, you often need to run `!pip install ...` again.

---

## 9. Secrets and API tokens

When calling Hugging Face / OpenAI from Colab, do **not** hardcode keys in the notebook.

### What are Colab Secrets?

**Colab Secrets** are a place inside Google Colab to store private values like:

- `HF_TOKEN`  
- `OPENAI_API_KEY`  
- other API keys  

Your notebook can read them in code, but the secret values are **not printed in the notebook file** you share.

### How is this similar to `.env`?

| | **Local `.env`** | **Colab Secrets** |
|---|------------------|-------------------|
| Purpose | Keep secrets out of code | Keep secrets out of notebook code |
| Example keys | `OPENAI_API_KEY=...` | Name: `OPENAI_API_KEY`, Value: `...` |
| Used by | `load_dotenv()` + `os.getenv(...)` | Colab userdata / secrets API + `os.environ` |
| Should you commit to GitHub? | No (gitignore) | N/A — not in your repo |
| Idea | Same: store secrets separately from code | Same idea, different place |

**Same goal:** code asks for a key by name; the real value lives somewhere safer than the notebook text.

Local:

```python
from dotenv import load_dotenv
import os
load_dotenv()
key = os.getenv("HF_TOKEN")
```

Colab (typical pattern):

```python
from google.colab import userdata
import os

os.environ["HF_TOKEN"] = userdata.get("HF_TOKEN")
```

(Exact helper can vary slightly; idea is: read secret by name, then use it.)

### Where do I see Secrets? (not in Google Drive)

**Colab Secrets are NOT stored as a file in Google Drive.**

You will not find them by opening Drive folders like `My Drive/...`.

They live in **Colab’s Secrets panel**, tied to your Google account + Colab, separate from Drive files.

#### How to open Secrets in Colab

1. Open any Colab notebook  
2. Look at the **left sidebar**  
3. Click the **key / Secrets** icon (secrets manager)  
4. Add a secret:
   - Name: `HF_TOKEN`  
   - Value: your token  
5. Enable notebook access if Colab asks  

That’s where you “see” and edit them — inside Colab UI, not Drive.

### What *is* in Google Drive then?

| In Drive | Not in Drive |
|----------|--------------|
| Your `.ipynb` notebooks (if saved to Drive) | Colab Secrets values |
| Datasets / files you upload or save | API keys stored as Secrets |
| Exported outputs you copy to Drive | The Secrets manager itself |

So:

- **Notebook file** → can live in Drive  
- **Secret values** → Colab Secrets panel (account-side), not a Drive folder  

### Good rules

1. Prefer **Colab Secrets** for keys in Colab  
2. Prefer **`.env`** for keys on your laptop  
3. Never paste keys into notebook cells and then share the notebook  
4. Never commit `.env` or notebooks containing pasted keys to GitHub  

Same habit, two homes:

```text
Laptop  →  .env
Colab   →  Secrets panel (not Google Drive)
```

---

## 10. Colab vs your local laptop

| | **Local laptop** | **Google Colab** |
|---|------------------|------------------|
| Where code runs | Your machine | Google cloud |
| GPU | Only if you have one | Often available (free/paid) |
| Setup | Conda / venv / drivers | Browser + Google account |
| Files | Stay on disk | Temporary unless saved to Drive |
| `pip install` | Into your local env | Into the temporary Colab runtime |
| Best for | Everyday scripts, Gradio apps, Ollama | Heavy model / GPU experiments |

Both are useful:

- local → your Gradio apps, Ollama, daily practice  
- Colab → GPU notebooks, Hugging Face pipelines, quick experiments  

### Is Colab like OpenAI cloud?

Similar idea (**something in the cloud**), but **not the same**.

| | **OpenAI cloud** | **Google Colab** |
|---|------------------|------------------|
| What it is | Hosted **AI models** (GPT) you call by API | Hosted **computer + notebook** to run *your* code |
| You mainly get | Answers from OpenAI’s models | CPU/GPU machine in the browser |
| Example | `openai.chat.completions.create(...)` | Run a Hugging Face `pipeline` on a T4 GPU |

- **OpenAI cloud** = rent their **brain** (model API)  
- **Colab** = rent a **laptop/GPU in the cloud** to run notebooks yourself  

You can use both together: a Colab notebook that calls the OpenAI API.

---

## 11. Colab + Hugging Face

Typical learning flow:

1. Open Colab  
2. Set GPU runtime (T4)  
3. `pip install transformers` (and friends)  
4. Add `HF_TOKEN` as a secret if needed  
5. Run a `pipeline(...)` or download a Hub model  

This pairs with your chapter:

[`7_HUGGING_FACE/what_is_huggingface.md`](../7_HUGGING_FACE/what_is_huggingface.md)

---

## 12. Good habits

- Save important notebooks to **Google Drive**  
- Re-run install cells after a new runtime  
- Prefer **Secrets** for tokens  
- Disconnect / shut down runtime when done (polite on free tier)  
- Don’t rely on Colab as permanent storage  

---

## One-line takeaway

**Google Colab is a cloud Jupyter notebook with easy GPUs — perfect for trying Hugging Face models without fighting local hardware first.**
