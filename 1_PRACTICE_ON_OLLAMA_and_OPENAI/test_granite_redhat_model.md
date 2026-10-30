# Understanding `test_granite_redhat_model.py`

This note explains **Red Hat Granite** via an OpenAI-compatible endpoint, and what each line of the script does.

This script shares the **same structure** as [`Test_OPENAI_LLM_with_openAI.py`](Test_OPENAI_LLM_with_openAI.py) and [`Test_ollama_with_OPENAI.py`](Test_ollama_with_OPENAI.py). The main difference is how the `OpenAI()` client is created: it points at Red Hat’s Granite API (`base_url` + Granite API key + Granite model name from `.env`).

Same `chat.completions.create(...)` call in all three — only the host (and auth) change:

| Script | `base_url` | Why |
|--------|------------|-----|
| [OpenAI cloud](Test_OPENAI_LLM_with_openAI.py) | not needed | default = OpenAI cloud (`https://api.openai.com/v1`) |
| [Ollama](Test_ollama_with_OPENAI.py) | `http://localhost:11434/v1` | local server, not OpenAI |
| **This file (Granite / RHDP)** | RHDP MaaS URL from `.env` | Red Hat host, not OpenAI |

Concept overviews (repo root): [OpenAI API vs ChatGPT](../OpenAI_API_vs_ChatGPT_subscription.md) · [Ollama install](../Ollama_install_linux.md)

Related practice notes:

- [`Test_OPENAI_LLM_with_openAI.md`](./Test_OPENAI_LLM_with_openAI.md) — cloud OpenAI  
- [`Test_ollama_with_OPENAI.md`](./Test_ollama_with_OPENAI.md) — local Ollama with the same client  

---

## Requirements

```bash
pip install openai python-dotenv
```

Put a `.env` in this directory or a parent directory. Example content:

```env
# Red Hat Demo Platform — granite-4-0-h-tiny
REDHAT_GRANITE_API_KEY="sk-_your_key_here"
REDHAT_GRANITE_BASE_URL=https://maas-rhdp.apps.maas.redhatworkshops.io/v1
REDHAT_GRANITE_MODEL=granite-4-0-h-tiny
```

---

## What is Red Hat Granite (in this script)?

[IBM Granite](https://www.ibm.com/granite) models are available through Red Hat–hosted, **OpenAI-compatible** HTTP APIs.

This practice script targets the **Red Hat Demo Platform** MaaS endpoint and model:

| Setting | Value |
|---------|--------|
| Platform | Red Hat Demo Platform (RHDP) MaaS |
| Model | `granite-4-0-h-tiny` |
| Base URL | `https://maas-rhdp.apps.maas.redhatworkshops.io/v1` |

That means:

- You still use the official `openai` Python package
- You do **not** call `api.openai.com`
- You pass your Granite **API key**, **base URL**, and **model name** from `.env`

See the `base_url` table at the top of this note for how this lines up with OpenAI cloud and Ollama.

---

## Full script

```python
from dotenv import load_dotenv
load_dotenv(override=True)

import os

granite_api_key = os.getenv("REDHAT_GRANITE_API_KEY")
granite_base_url = os.getenv("REDHAT_GRANITE_BASE_URL")
granite_model = os.getenv("REDHAT_GRANITE_MODEL")

if granite_api_key:
    print("Red Hat Granite API Key is set")
else:
    print("Red Hat Granite API Key not set")


from openai import OpenAI

# Create an OpenAI-compatible client for the Red Hat Granite endpoint
granite = OpenAI(
    api_key=granite_api_key,
    base_url=granite_base_url
)

messages = [
    {
        "role": "user",
        "content": "Who is IRON MAN ?"
    }
]

# Call the Granite model
response = granite.chat.completions.create(
    model=granite_model,
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

### Read Granite settings from the environment

```python
granite_api_key = os.getenv("REDHAT_GRANITE_API_KEY")
granite_base_url = os.getenv("REDHAT_GRANITE_BASE_URL")
granite_model = os.getenv("REDHAT_GRANITE_MODEL")
```

| Variable | Meaning |
|----------|---------|
| `REDHAT_GRANITE_API_KEY` | Secret that authenticates you to the Granite endpoint |
| `REDHAT_GRANITE_BASE_URL` | OpenAI-compatible API base (host + `/v1` path as provided by Red Hat) |
| `REDHAT_GRANITE_MODEL` | Which Granite model id to call |

If any are missing, `os.getenv` returns `None` and the later API call will fail.

```python
if granite_api_key:
    print("Red Hat Granite API Key is set")
else:
    print("Red Hat Granite API Key not set")
```

Prints whether the key was found — without printing the secret itself (safer than dumping the raw key).

The script still continues either way. The real request fails later if the key or URL is missing.

---

### Create the OpenAI client (pointed at Granite)

```python
from openai import OpenAI

granite = OpenAI(
    api_key=granite_api_key,
    base_url=granite_base_url
)
```

Creates an OpenAI client configured for Red Hat Granite — **this is the important structural difference** from default cloud OpenAI (`OpenAI()` with no args) and from Ollama (fixed localhost URL + dummy key).

| Argument | Meaning |
|----------|---------|
| `api_key=granite_api_key` | Your Red Hat Granite credential |
| `base_url=granite_base_url` | Send Chat Completions to the Granite host, not OpenAI cloud |

Same Python method (`chat.completions.create`) as the other two practice scripts.

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

Creates the chat input as a **list of message dictionaries** — same Chat Completions shape as OpenAI / Ollama.

- `role`: `"user"` → this message is from you  
- `content`: the text sent to the model  

This script uses only a single `"user"` message.

---

### Call the Chat Completions API

```python
response = granite.chat.completions.create(
    model=granite_model,
    messages=messages
)
```

This is the main request:

1. `granite.chat.completions.create(...)` → send a chat completion request  
2. `model=granite_model` → use the model name from `.env`  
3. `messages=messages` → send your prompt list  

The endpoint returns a **response object** (choices, usage, metadata), not just plain text.

---

### Print the model’s answer

```python
print(response.choices[0].message.content)
```

Walks into the response structure:

| Part | Meaning |
|------|---------|
| `response` | Full API result |
| `choices` | List of possible answers (usually length 1) |
| `choices[0]` | First (best/default) choice |
| `.message` | The assistant message object |
| `.content` | The actual text string to print |

So this line prints only the reply text (e.g. an explanation of Iron Man).

---

## What happens when you run it?

1. Load `.env` and read Granite key, base URL, and model
2. Print whether the API key is set
3. Create an OpenAI-compatible client pointed at the Granite endpoint
4. Send: *“Who is IRON MAN ?”* to the configured Granite model
5. Print the model’s text answer

No OpenAI cloud call. No local Ollama required for this script.

---

## How to run

```bash
python test_granite_redhat_model.py
```

`load_dotenv()` loads `.env` from the current working directory (or wherever you point it). Keep the file in this directory or a parent directory so those vars are available when you run.

---

## Quick troubleshooting

| Problem | Likely cause |
|---------|----------------|
| “API Key not set” | Missing `REDHAT_GRANITE_API_KEY` in `.env`, or `.env` not found from the directory you ran from |
| Auth / 401 errors | Wrong or expired Granite API key |
| Connection / DNS errors | Wrong `REDHAT_GRANITE_BASE_URL` |
| Model not found | Wrong `REDHAT_GRANITE_MODEL` for that endpoint |
