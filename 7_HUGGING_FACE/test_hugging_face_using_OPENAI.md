# `test_hugging_face_using_OPENAI.py` — explained

Walkthrough of [`test_hugging_face_using_OPENAI.py`](./test_hugging_face_using_OPENAI.py).

Related notes: [`what_is_huggingface.md`](./what_is_huggingface.md)

Sister script (`InferenceClient` style): [`test_hugging_face_using_huggingFaceHUB.py`](./test_hugging_face_using_huggingFaceHUB.py) · [`test_hugging_face_using_huggingFaceHUB.md`](./test_hugging_face_using_huggingFaceHUB.md)

---

## What this script does (one sentence)

Loads `HF_TOKEN` from `.env`, uses the familiar **OpenAI Python client** pointed at Hugging Face’s router, asks “What is the capital of France?”, and prints the answer.

---

## Full script

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

MODEL = "Qwen/Qwen2.5-7B-Instruct:together"

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

completion = client.chat.completions.create(
    model = MODEL,
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
)

print(completion.choices[0].message.content)
```

---

## Bit by bit

### Imports

```python
import os
from openai import OpenAI
from dotenv import load_dotenv
```

| Import | Why |
|--------|-----|
| `os` | Read `HF_TOKEN` from environment |
| `OpenAI` | OpenAI-compatible Python client |
| `load_dotenv` | Load `.env` secrets |

This is the **same package** you used for OpenAI cloud — only `base_url` / model / key change.

### Load `.env`

```python
load_dotenv(override=True)
```

Your `.env` should include:

```env
HF_TOKEN="XXXXXXXXXXXXXXXXXX"
```

### Model name

```python
MODEL = "Qwen/Qwen2.5-7B-Instruct:together"
```

| Piece | Meaning |
|-------|---------|
| `Qwen/Qwen2.5-7B-Instruct` | Model on the Hub |
| `:together` | Provider routing hint (Together AI) |

#### What is Qwen?

**Qwen** is an open LLM family from **Alibaba**.  
`Qwen2.5-7B-Instruct` means: Qwen version 2.5, ~7 billion parameters, chat/instruct-tuned.

#### What does `:together` mean?

- Hugging Face receives your request  
- `:together` asks to run it on the **Together AI** backend  
- answer returns through HF to your Python  

```text
OpenAI SDK → HF router → Together runs Qwen → reply
```

⚠️ Depending on HF router setup, you may use the plain model id without `:together`. If one form fails, try the other.

---

### Key concept: why `:together` here, but not in the HUB script?

**Same model. Same Together. Different place to name the provider.**

| Script | How you select Together | Model string |
|--------|-------------------------|--------------|
| HUB (`InferenceClient`) | `provider="together"` on the client | `Qwen/Qwen2.5-7B-Instruct` |
| This one (`OpenAI`) | no `provider=` — put it in the model id | `Qwen/Qwen2.5-7B-Instruct:together` |

**HUB script** — provider is a separate argument, so the model name stays plain:

```python
client = InferenceClient(
    provider="together",   # ← Together chosen HERE
    api_key=os.environ["HF_TOKEN"],
)

model="Qwen/Qwen2.5-7B-Instruct"   # ← no :together needed
```

**This OpenAI script** — `OpenAI()` has no `provider=` argument, so HF’s router reads the provider from the model string:

```python
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)
# no provider= here

MODEL = "Qwen/Qwen2.5-7B-Instruct:together"  # ← Together chosen HERE
```

```text
HUB:      provider="together"  +  model="Qwen/..."
OpenAI:   model="Qwen/...:together"
```

Remember: `:together` is **routing**, not part of the model’s real name on the Hub.

### Key concept: this does **not** appear in OpenAI subscription usage

You are using the **OpenAI Python package**, but you are **not** calling OpenAI’s cloud.

| Piece in this script | Points to |
|----------------------|-----------|
| `base_url="https://router.huggingface.co/v1"` | Hugging Face (not `api.openai.com`) |
| `api_key=HF_TOKEN` | Your HF token (not `OPENAI_API_KEY`) |

So:

- **OpenAI usage / billing page** → does **not** show these calls  
- **Hugging Face** (and the routed provider, e.g. Together) → where usage lives  

You’ll see OpenAI subscription usage only when you call OpenAI cloud with `OPENAI_API_KEY` and the default OpenAI base URL.

```text
This script:   OpenAI SDK  →  HF router  →  Together   (HF bill / credits)
OpenAI cloud:  OpenAI SDK  →  api.openai.com           (OpenAI subscription)
```

### Create the client (HF router, not OpenAI cloud)

```python
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)
```

| Piece | Meaning |
|-------|---------|
| `base_url=...huggingface...` | Talk to **HF OpenAI-compatible router**, not `api.openai.com` |
| `api_key=HF_TOKEN` | Your Hugging Face token (not `OPENAI_API_KEY`) |

#### Why no Together API key here?

Even if the model runs on Together’s machines, **your Python is talking to Hugging Face**, not to Together directly.

```text
Your code
   ↓  uses HF_TOKEN
   ↓  base_url = router.huggingface.co
Hugging Face Router
   ↓  sees model "...:together"
Together AI runs the model
   ↓
Reply returns through Hugging Face
```

So:

| What you configure | Why |
|--------------------|-----|
| `base_url="https://router.huggingface.co/v1"` | Client endpoint is **Hugging Face** |
| `api_key=HF_TOKEN` | You authenticate to **HF**, not Together |
| `MODEL = "...:together"` | HF then **forwards** the job to Together |

You would need a **Together API key** only if you called Together’s own API directly (Together’s base URL + Together key).

This script uses the **HF router path**: one HF token, HF chooses/routes to the provider named in the model string.

This is the key difference from your OpenAI cloud test:

| Script | `base_url` | Key |
|--------|------------|-----|
| OpenAI cloud test | default OpenAI | `OPENAI_API_KEY` |
| This HF test | HF router | `HF_TOKEN` |

### Call the model

```python
completion = client.chat.completions.create(
    model = MODEL,
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
)
```

Same chat shape as OpenAI:

- `model` → which model  
- `messages` → conversation list  

### Print the reply

```python
print(completion.choices[0].message.content)
```

Expected vibe:

```text
The capital of France is Paris.
```

---

## How to run

```bash
python test_hugging_face_using_OPENAI.py
```

Needs:

- `HF_TOKEN` in `.env`  
- packages: `openai`, `python-dotenv`  

---

## When to use this style

Use this when you already know the OpenAI SDK and want Hugging Face models with **almost the same code**.

Use [`test_hugging_face_using_huggingFaceHUB.py`](./test_hugging_face_using_huggingFaceHUB.py) when you want the official `huggingface_hub.InferenceClient`.

---

## Side-by-side with the other HF test

| | `huggingFaceHUB` script | `OPENAI` script |
|---|-------------------------|-----------------|
| Client | `InferenceClient` | `OpenAI(...)` |
| Package | `huggingface_hub` | `openai` |
| Auth | `HF_TOKEN` | `HF_TOKEN` |
| How Together is selected | `provider="together"` | model suffix `:together` |
| Model string | `Qwen/Qwen2.5-7B-Instruct` | `Qwen/Qwen2.5-7B-Instruct:together` |
| Chat call | `client.chat.completions.create(...)` | same shape |
| Question | capital of France | capital of France |

(See **Key concept: why `:together` here, but not in the HUB script?** above for the full explanation.)
