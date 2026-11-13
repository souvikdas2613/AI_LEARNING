# Understanding `test_enmaas_redhat_model.py`

This note explains **Red Hat ENMAAS** via an OpenAI-compatible endpoint, and what each line of the script does.

This script shares the **same structure** as [`Test_OPENAI_LLM_with_openAI.py`](Test_OPENAI_LLM_with_openAI.py), [`Test_ollama_with_OPENAI.py`](Test_ollama_with_OPENAI.py), and [`test_granite_redhat_model.py`](test_granite_redhat_model.py). The main difference is how the `OpenAI()` client is created: it points at Red Hat’s ENMAAS API (`base_url` + ENMAAS API key + model name from `.env`).

Same `chat.completions.create(...)` call in all four — only the host (and auth) change:

| Script | `base_url` | Why |
|--------|------------|-----|
| [OpenAI cloud](Test_OPENAI_LLM_with_openAI.py) | not needed | default = OpenAI cloud (`https://api.openai.com/v1`) |
| [Ollama](Test_ollama_with_OPENAI.py) | `http://localhost:11434/v1` | local server, not OpenAI |
| [Granite / RHDP](test_granite_redhat_model.py) | RHDP MaaS URL from `.env` | Red Hat host, not OpenAI |
| **This file (ENMAAS)** | ENMAAS URL from `.env` | Red Hat ENMAAS host, not OpenAI |

Concept overviews (repo root): [OpenAI API vs ChatGPT](../OpenAI_API_vs_ChatGPT_subscription.md) · [Ollama install](../Ollama_install_linux.md)

Related practice notes:

- [`Test_OPENAI_LLM_with_openAI.md`](./Test_OPENAI_LLM_with_openAI.md) — cloud OpenAI  
- [`Test_ollama_with_OPENAI.md`](./Test_ollama_with_OPENAI.md) — local Ollama with the same client  
- [`test_granite_redhat_model.md`](./test_granite_redhat_model.md) — Red Hat Granite / RHDP  

---

## Requirements

```bash
pip install openai python-dotenv
```

Put a `.env` in this directory or a parent directory. Example content:

```env
# Red Hat ENMAAS — DeepSeek Flash
REDHAT_ENMAAS_API_KEY="your_enmaas_key_here"
REDHAT_ENMAAS_BASE_URL=https://api.enmaas.devshift.net/v1
REDHAT_ENMAAS_MODEL=rits/deepseek-ai/DeepSeek-V4.1-Flash-1017
```

Equivalent curl (same endpoint the Python client calls):

```bash
curl https://api.enmaas.devshift.net/v1/chat/completions \
  -H "Authorization: Bearer $REDHAT_ENMAAS_API_KEY" \
  -H "content-type: application/json" \
  -d '{"model":"rits/deepseek-ai/DeepSeek-V4.1-Flash-1017","max_tokens":128,"messages":[{"role":"user","content":"Reply with exactly OK."}]}'
```

---

## What is Red Hat ENMAAS (in this script)?

ENMAAS exposes **OpenAI-compatible** HTTP APIs (Chat Completions under `/v1`).

This practice script targets:

| Setting | Value |
|---------|--------|
| Platform | Red Hat ENMAAS |
| Model | `rits/deepseek-ai/DeepSeek-V4.1-Flash-1017` |
| Base URL | `https://api.enmaas.devshift.net/v1` |

That means:

- You still use the official `openai` Python package
- You do **not** call `api.openai.com`
- You pass your ENMAAS **API key**, **base URL**, and **model name** from `.env`

`base_url` must end at `/v1` (no `/chat/completions`). The client appends that path itself.

---

## Full script

```python
from dotenv import load_dotenv
load_dotenv(override=True)

import os

enmaas_api_key = os.getenv("REDHAT_ENMAAS_API_KEY")
enmaas_base_url = os.getenv("REDHAT_ENMAAS_BASE_URL")
enmaas_model = os.getenv("REDHAT_ENMAAS_MODEL")

if enmaas_api_key:
    print("Red Hat ENMAAS API Key is set")
else:
    print("Red Hat ENMAAS API Key not set")


from openai import OpenAI

# Create an OpenAI-compatible client for the Red Hat ENMAAS endpoint
enmaas = OpenAI(
    api_key=enmaas_api_key,
    base_url=enmaas_base_url
)

messages = [
    {
        "role": "user",
        "content": "Who is IRON MAN ?"
    }
]

# Call the ENMAAS model
response = enmaas.chat.completions.create(
    model=enmaas_model,
    messages=messages
)

print(response.choices[0].message.content)
```

---

## Line-by-line explanation

### Load secrets from `.env`

```python
from dotenv import load_dotenv
load_dotenv(override=True)

import os
```

Loads variables from `.env` into the process environment, then imports `os` so you can read them with `os.getenv(...)`.

`override=True` means values in `.env` replace any same-named variables already set in the shell.

---

### Read ENMAAS settings from the environment

```python
enmaas_api_key = os.getenv("REDHAT_ENMAAS_API_KEY")
enmaas_base_url = os.getenv("REDHAT_ENMAAS_BASE_URL")
enmaas_model = os.getenv("REDHAT_ENMAAS_MODEL")
```

| Variable | Meaning |
|----------|---------|
| `REDHAT_ENMAAS_API_KEY` | Secret that authenticates you to ENMAAS |
| `REDHAT_ENMAAS_BASE_URL` | OpenAI-compatible API base (host + `/v1`) |
| `REDHAT_ENMAAS_MODEL` | Which ENMAAS model id to call |

If any are missing, `os.getenv` returns `None` and the later API call will fail.

```python
if enmaas_api_key:
    print("Red Hat ENMAAS API Key is set")
else:
    print("Red Hat ENMAAS API Key not set")
```

Prints whether the key was found — without printing the secret itself.

---

### Create the OpenAI client (pointed at ENMAAS)

```python
from openai import OpenAI

enmaas = OpenAI(
    api_key=enmaas_api_key,
    base_url=enmaas_base_url
)
```

Creates an OpenAI client configured for Red Hat ENMAAS — same pattern as Granite: custom `api_key` + `base_url`.

| Argument | Meaning |
|----------|---------|
| `api_key=enmaas_api_key` | Your ENMAAS credential |
| `base_url=enmaas_base_url` | Send Chat Completions to ENMAAS, not OpenAI cloud |

Same Python method (`chat.completions.create`) as the other practice scripts.

---

### Build the chat prompt

```python
messages = [
    {
        "role": "user",
        "content": "Who is IRON MAN ?"
    }
]
```

Creates the chat input as a **list of message dictionaries** — same Chat Completions shape as OpenAI / Ollama / Granite.

---

### Call the Chat Completions API

```python
response = enmaas.chat.completions.create(
    model=enmaas_model,
    messages=messages
)
```

This is the main request:

1. `enmaas.chat.completions.create(...)` → send a chat completion request  
2. `model=enmaas_model` → use the model name from `.env`  
3. `messages=messages` → send your prompt list  

---

### Print the model’s answer

```python
print(response.choices[0].message.content)
```

Prints only the reply text from the first choice.

---

## What happens when you run it?

1. Load `.env` and read ENMAAS key, base URL, and model
2. Print whether the API key is set
3. Create an OpenAI-compatible client pointed at the ENMAAS endpoint
4. Send: *“Who is IRON MAN ?”* to the configured ENMAAS model
5. Print the model’s text answer

No OpenAI cloud call. No local Ollama required for this script.

---

## How to run

```bash
python test_enmaas_redhat_model.py
```

`load_dotenv()` loads `.env` from the current working directory (or a parent). Keep the file in this directory or a parent directory so those vars are available when you run.

---

## Quick troubleshooting

| Problem | Likely cause |
|---------|----------------|
| “API Key not set” | Missing `REDHAT_ENMAAS_API_KEY` in `.env`, or `.env` not found from the directory you ran from |
| Auth / 401 errors | Wrong or expired ENMAAS API key |
| Connection / DNS errors | Wrong `REDHAT_ENMAAS_BASE_URL` |
| Model not found | Wrong `REDHAT_ENMAAS_MODEL` for that endpoint |
