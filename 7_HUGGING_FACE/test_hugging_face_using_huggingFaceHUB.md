# `test_hugging_face_using_huggingFaceHUB.py` — explained

Walkthrough of [`test_hugging_face_using_huggingFaceHUB.py`](./test_hugging_face_using_huggingFaceHUB.py).

Related notes: [`what_is_huggingface.md`](./what_is_huggingface.md)

Sister script (OpenAI client style): [`test_hugging_face_using_OPENAI.py`](./test_hugging_face_using_OPENAI.py) · [`test_hugging_face_using_OPENAI.md`](./test_hugging_face_using_OPENAI.md)

---

## What this script does (one sentence)

Loads `HF_TOKEN` from `.env`, uses Hugging Face’s official `InferenceClient`, asks a chat model “What is the capital of France?”, and prints the answer.

---

## Full script

```python
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv(override=True)

client = InferenceClient(
    provider="together",
    api_key=os.environ["HF_TOKEN"],
)

completion = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
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
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
```

| Import | Why |
|--------|-----|
| `os` | Read env vars like `HF_TOKEN` |
| `InferenceClient` | Official Hugging Face inference client |
| `load_dotenv` | Load secrets from `.env` |

`huggingface_hub` is the official HF SDK for Hub + tokens + (now) inference.

### Load `.env`

```python
load_dotenv(override=True)
```

Loads your `.env`, including:

```env
HF_TOKEN="XXXXXXXXXXXXXXXXXX"
```

`override=True` replaces any existing env value with the `.env` value.

### Create the client

```python
client = InferenceClient(
    provider="together",
    api_key=os.environ["HF_TOKEN"],
)
```

| Piece | Meaning |
|-------|---------|
| `InferenceClient(...)` | High-level HF client for model calls |
| `provider="together"` | Route the call through **Together AI** backend |
| `api_key=...HF_TOKEN` | Auth with your Hugging Face token |

#### What does “route through Together AI backend” mean?

Your code talks to **Hugging Face**, but the model may actually **run on Together AI’s servers**.

```text
Your Python
    ↓  HF_TOKEN
Hugging Face (InferenceClient / router)
    ↓  provider="together"
Together AI machines run Qwen
    ↓
Answer comes back to you
```

| Piece | Role |
|-------|------|
| **Hugging Face** | Front door / catalog / token / routing |
| **Together AI** | One possible **compute provider** that hosts/runs models |
| `provider="together"` | “Please run this model on Together’s backend” |

Why this exists:

- Hugging Face lists many models  
- Not every model always runs on HF’s own free servers  
- Providers (Together, Fireworks, etc.) supply GPU hosting  
- HF can **route** your request to a provider  

So you still use `HF_TOKEN` and a Hub model name, but the GPU work may happen at Together.

If Together/routing isn’t set up for your account, the call can fail — then check HF settings / billing / try another provider or model.

#### What is the Qwen model here?

```python
model="Qwen/Qwen2.5-7B-Instruct"
```

**Qwen** (pronounce roughly like “Chwen”) is a family of open LLMs from **Alibaba** (Tongyi Qianwen).

| Piece in the name | Meaning |
|-------------------|---------|
| `Qwen/` | Organization / model family on the Hub |
| `Qwen2.5` | Version generation of the model line |
| `7B` | About **7 billion** parameters (size) |
| `Instruct` | Fine-tuned to follow chat instructions (not only raw text completion) |

So in this script:

- you are not calling GPT from OpenAI  
- you are calling an **open Qwen chat model** listed on Hugging Face  
- size `7B` is medium-small: capable for Q&A, lighter than huge 70B models  

Full Hub-style id: `Qwen/Qwen2.5-7B-Instruct`

⚠️ Note: for some setups you may need provider-linked billing / access. If auth fails, check HF token permissions and provider routing.

### Call the model

```python
completion = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
)
```

| Piece | Meaning |
|-------|---------|
| `chat.completions.create` | OpenAI-style chat request |
| `model=...` | Hub model id |
| `messages` | Chat turns (`user` / `assistant` / `system`) |

Here: one user question only.

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
python test_hugging_face_using_huggingFaceHUB.py
```

Needs:

- `HF_TOKEN` in `.env`  
- package: `huggingface_hub` (`pip install huggingface_hub`)  

---

## When to use this style

Use **`InferenceClient`** when you want the **official Hugging Face hub client**.

Use the OpenAI-client script when you want the **same OpenAI SDK shape** you already know, pointed at HF’s router.

---

## Why this script has no `:together` on the model name

Same model. Same Together. Different place to say “use Together.”

| Script | How Together is selected | Model string |
|--------|--------------------------|--------------|
| `InferenceClient` (this one) | `provider="together"` on the client | `Qwen/Qwen2.5-7B-Instruct` |
| OpenAI client | no `provider=` arg — put it in the model id | `Qwen/Qwen2.5-7B-Instruct:together` |

```text
InferenceClient:  provider="together"  +  model="Qwen/..."
OpenAI client:    model="Qwen/...:together"
```
