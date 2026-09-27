# `keyword_rag_gradio_chat.py` — every step explained

Walkthrough of [`keyword_rag_gradio_chat.py`](./keyword_rag_gradio_chat.py), in the **same order** as the file (top → bottom).

File header comment: `load markdown dict → match words in question → OpenAI chat`.

---

## What this script does (one sentence)

Loads **employee** markdown into a `knowledge` dict (key = last name), matches words in each user message to those keys, appends matched text to the system prompt, and returns OpenAI’s reply via **Gradio** `chat(message, history)`.

---

## How to run

From the folder that contains `keyword_rag_gradio_chat.py` and `knowledge-base/`:

```bash
pip install openai python-dotenv gradio
python3 keyword_rag_gradio_chat.py
```

### `.env`

| Key | Used in file |
|-----|----------------|
| `OPENAI_API_KEY` | `OpenAI()` |
| `MODEL_NAME` | `openai.chat.completions.create(model=MODEL_NAME, ...)` |

```env
OPENAI_API_KEY=your-key-here
MODEL_NAME=gpt-4.1-nano
```

---

## Execution order (what runs when)

1. Imports  
2. `os.chdir(...)`  
3. `load_dotenv`, read keys, print key/model, `openai = OpenAI()`  
4. Employee loop → fill `knowledge` and `employee_keys`  
5. Print `[RAG load] ...`  
6. Print `employee_keys`, then each `knowledge` key + file text (debug loop)  
7. Define `SYSTEM_PREFIX`  
8. Define `chat` (not called yet)  
9. `gr.ChatInterface(chat).launch(inbrowser=True)`  
10. Each Gradio message → `chat(message, history)` → prints `words`, retrieve logs, `retrieved_employee_data`, augment, OpenAI

---

## Step 1 — Imports

```python
import os
import glob
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
```

| Import | Role in this file |
|--------|-------------------|
| `os` | `chdir`, `getenv` |
| `glob` | `knowledge-base/employees/*` |
| `Path` | Filename → last-name key |
| `gradio` | Chat UI |
| `load_dotenv` | Load `.env` |
| `OpenAI` | Chat Completions API |

---

## Step 2 — `chdir`

```python
os.chdir(os.path.dirname(os.path.abspath(__file__)))
```

Sets the working directory to the folder that contains this `.py` file so `knowledge-base/employees/*` resolves correctly.

---

## Step 3 — Environment and client

```python
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

MODEL_NAME = os.getenv("MODEL_NAME")
if MODEL_NAME:
    print(f"Using model: {MODEL_NAME}")
else:
    print("MODEL_NAME not set in .env")
openai = OpenAI()
```

| Line | Meaning |
|------|---------|
| `openai_api_key` | Only used for the startup print (first 8 chars) |
| `MODEL_NAME` | From `.env`; used on every API call |
| `OpenAI()` | Client reads `OPENAI_API_KEY` from the environment |

---

## Step 4 — Build `knowledge` dict (employees only)

Comment in the file mentions products; **as written**, only the employee loop runs.

```python
# Load employee (key = last name) and product (key = filename) markdown into one dict.
knowledge = {}
employee_keys = set()

for filename in glob.glob("knowledge-base/employees/*"):
    key = Path(filename).stem.split(" ")[-1].lower()
    employee_keys.add(key)
    with open(filename, encoding="utf-8") as f:
        knowledge[key] = f.read()

print(f"[RAG load] {len(employee_keys)} employees + {len(knowledge) - len(employee_keys)} products in knowledge dict.")

print ("employee_keys:\n\n")
print (employee_keys)
print ("knowledge:\n\n")
for key, value in knowledge.items():
    print (key)
    print (value)
    print ("\n\n")
```

| Line | Meaning |
|------|---------|
| `key` | Last word of filename → lower, e.g. `Alex Chen.md` → `chen` |
| `employee_keys` | Set of employee keys (used in `chat` for retrieve logs) |
| `knowledge[key]` | Full markdown file text |
| `[RAG load]` print | Employee count = `len(employee_keys)`; product count = `len(knowledge) - len(employee_keys)` (0 with only the employee loop) |
| `print(employee_keys)` | Dumps every last-name key after load (debug) |
| `for key, value in knowledge.items()` | Prints each key, then full markdown, then blank lines (long startup output) |

---

## Step 5 — `SYSTEM_PREFIX`

```python
SYSTEM_PREFIX = """
You represent Insurellm, the Insurance Tech company.
You are an expert in answering questions about Insurellm; its employees and its products.
You are provided with additional context that might be relevant to the user's question.
Give brief, accurate answers. If you don't know the answer, say so.

Relevant context:
"""
```

Inside `chat`, retrieved text is appended: `system_message = SYSTEM_PREFIX + extra`.

---

## Step 6 — `chat(message, history)`

Full function as in the file (same line order):

```python
def chat(message, history):
    print(f"\n[Gradio] user: {message!r}")

    # Retrieve: any word in the message that matches a dict key
    words = "".join(ch for ch in message if ch.isalpha() or ch.isspace()).lower().split()

    print ("words:\n\n")
    print (words)
    print ("\n\n")

    for w in words:
        if w in knowledge and w in employee_keys:
            print(f"[RAG retrieve] employee file for last name '{w}'")
        elif w in knowledge:
            print(f"[RAG retrieve] product file for '{w}'")

    retrieved_employee_data = [knowledge[w] for w in words if w in knowledge]

    print ("retrieved_employee_data:\n\n")
    print (retrieved_employee_data)
    print ("\n\n")

    if retrieved_employee_data:
        extra = "The following additional context might be relevant in answering the user's question:\n\n"
        extra += "\n\n".join(retrieved_employee_data)
        print(f"[RAG augment] {len(retrieved_employee_data)} file(s), {sum(len(c) for c in retrieved_employee_data)} chars")
    else:
        extra = "There is no additional context relevant to the user's question."
        print("[RAG augment] nothing matched — no docs in prompt")

    system_message = SYSTEM_PREFIX + extra
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]

    print(f"[OpenAI] model={MODEL_NAME}")
    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages)
    return response.choices[0].message.content
```

### 6a — Build `words`

```python
words = "".join(ch for ch in message if ch.isalpha() or ch.isspace()).lower().split()
```

Keep letters and spaces only → lowercase → split on spaces. Debug: `print(words)`.

For `tell me about chen` → `['tell', 'me', 'about', 'chen']`. That is tokenizing only — not retrieval yet.

### 6b — Retrieve loop (logs only)

```python
for w in words:
    if w in knowledge and w in employee_keys:
        print(f"[RAG retrieve] employee file for last name '{w}'")
    elif w in knowledge:
        print(f"[RAG retrieve] product file for '{w}'")
```

Walks each word and asks: **is `w` a key in `knowledge`?**

| Word | In `knowledge`? | In `employee_keys`? | Loop action |
|------|-----------------|---------------------|-------------|
| `tell` | No | — | No print |
| `me` | No | — | No print |
| `about` | No | — | No print |
| `chen` | Yes (`Alex Chen.md`) | Yes | Print employee retrieve line |

- `w in knowledge` — word is a lookup key (loaded markdown exists).  
- `w in employee_keys` — key came from `employees/` (first `if`).  
- `elif w in knowledge` — product keys (unused until you add a products loop).

This loop **does not** copy text into the prompt; it only **logs** which keys matched.

### 6c — Build `retrieved_employee_data` (actual retrieval)

```python
retrieved_employee_data = [knowledge[w] for w in words if w in knowledge]
```

#### What is `retrieved_employee_data`?

`retrieved_employee_data` is a **Python list of strings**. Each string is **one whole employee (or product) markdown file** whose **dictionary key** appeared as a word in the user’s message.

| Piece | Meaning |
|-------|---------|
| **Type** | `list` — e.g. `['# HR Record\n\n# Alex Chen\n...', ...]` |
| **One list item** | Entire file text for one matched key (this demo does not split files into smaller pieces) |
| **RAG term “chunk”** | In advanced RAG, context is often many small chunks; here **one employee file = one list element** in `retrieved_employee_data` |

#### How the line works

For each `w` in `words` **in order**:

1. If `w` is a key in `knowledge`, append `knowledge[w]` to the list.  
2. If `w` is not a key, skip it.

So `retrieved_employee_data` is **not** the words — it is the **file contents** behind those words.

**Example:** `tell me about chen`

```text
words  →  ['tell', 'me', 'about', 'chen']
retrieved_employee_data →  [ knowledge['chen'] ]     # one element: full Alex Chen.md (~2547 chars)
```

**Example:** `Who is lancaster and what is carllm?` (if both keys exist in `knowledge`)

```text
retrieved_employee_data →  [ knowledge['lancaster'], knowledge['carllm'] ]   # two elements
```

If the user says `chen` twice in one message, the list comprehension can append **the same text twice** (two list entries) — rare in practice.

#### `retrieved_employee_data` vs the retrieve `for` loop (6b)

| | Retrieve `for` loop | `retrieved_employee_data` line |
|---|---------------------|---------------|
| **Purpose** | Debug prints | **Data** for the model |
| **Output** | Lines in the terminal | List of strings in memory |
| **Used in API?** | No | Yes — becomes part of `extra` |

#### What happens to `retrieved_employee_data` next (6d)

```python
extra += "\n\n".join(retrieved_employee_data)
```

All list items are glued into **one big string** with blank lines between files. That string is appended after `SYSTEM_PREFIX` → the model reads it as **retrieved context**.

Debug `print(retrieved_employee_data)` in the terminal shows a list whose elements start like `['# HR Record\n\n# Alex Chen\n...']` — hard to read because each element is the **full** markdown file.

### 6d — Augment (`extra`)

If `retrieved_employee_data` is non-empty, join them into `extra` and log file count + character count. If empty, `extra` says there is no additional context.

### 6e — OpenAI

`system_message = SYSTEM_PREFIX + extra`, build `messages` with `history`, call API, `return` assistant text to Gradio.

---

## Step 7 — Launch Gradio

```python
gr.ChatInterface(chat).launch(inbrowser=True)
```

Gradio 6+: `gr.ChatInterface(chat)` only (no `type="messages"`).

---

## Sample run — input: `tell me about chen`

After startup prints (`[RAG load]`, `employee_keys`, knowledge debug loop), open the Gradio URL and send:

```text
tell me about chen
```

**Console (excerpt — `retrieved_employee_data` print is one very long string; omitted here):**

```text
[Gradio] user: 'tell me about chen'

words:

['tell', 'me', 'about', 'chen']


[RAG retrieve] employee file for last name 'chen'

retrieved_employee_data:

['# HR Record\n\n# Alex Chen\n\n## Summary\n- **Date of Birth:** ...']

[RAG augment] 1 file(s), 2547 chars
[OpenAI] model=gpt-4.1-nano
```

**Gradio assistant reply (example — wording can vary per API call):**

```text
Alex Chen is a Senior Backend Software Engineer at Insurellm, based in San Francisco. He joined the company as a Junior Backend Developer in April 2020 and was promoted over time due to his exemplary performance. He has contributed significantly to scaling backend services, reducing downtime, and improving system security. Alex's responsibilities include developing APIs, leading major architecture overhauls, and supporting cloud infrastructure transitions. He is actively involved in professional development and diversity initiatives within the company.
```

The answer comes from **Alex Chen’s markdown** in the system prompt (RAG), not from the model guessing.

---

## Terminal output cheat sheet

| When | Print |
|------|--------|
| Startup | API key hint, `Using model: ...`, `[RAG load]`, `employee_keys`, knowledge key/value loop |
| Each message | `[Gradio]`, `words`, `[RAG retrieve]` (per matching key), `retrieved_employee_data`, `[RAG augment]`, `[OpenAI]` |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `unexpected keyword argument 'type'` | Use `gr.ChatInterface(chat)` (Gradio 6+) |
| No `[RAG retrieve]` | No word matches a key — use employee **last name** (e.g. `chen`) |
| `MODEL_NAME not set` | Set `MODEL_NAME` in `.env` |
| Missing files | `knowledge-base/employees/` next to the script |
| Huge `retrieved_employee_data` in terminal | Expected — full markdown; use for learning/debug only |
