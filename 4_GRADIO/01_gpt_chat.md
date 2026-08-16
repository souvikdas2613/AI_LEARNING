# `01_gpt_chat.py` — every step explained

Line-by-line walkthrough of [`01_gpt_chat.py`](./01_gpt_chat.py).

For the big-picture “what is Gradio?” notes, see [`what_is_gradio.md`](./what_is_gradio.md).

---

## What this script does (one sentence)

Loads your OpenAI key, defines a function that asks GPT a question, prints one test answer in the terminal, then opens a Gradio browser UI so you can type more questions.

---

## Big picture flow

```
.env  →  OpenAI client  →  message_gpt(prompt)
                                │
                    ┌───────────┴───────────┐
                    │                       │
              print() test            Gradio UI
           (terminal check)      (browser textboxes)
```

---

## Step 1 — Imports

```python
import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
```

| Import | Why we need it |
|--------|----------------|
| `os` | Read environment variables with `os.getenv(...)` |
| `load_dotenv` | Load key/values from a `.env` file into the environment |
| `OpenAI` | Official SDK class used to call OpenAI’s Chat Completions API |
| `gradio as gr` | Build the web UI (`gr.Interface(...).launch()`) |

Nothing runs yet here — Python only loads libraries into memory.

---

## Step 2 — Load secrets from `.env`

```python
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
```

### `load_dotenv(override=True)`

- Looks for a `.env` file (usually in the current working directory / project path)
- Reads lines like `OPENAI_API_KEY=...` and `MODEL_NAME=...`
- Puts them into process environment variables
- `override=True` means: if a variable already exists in the shell, **replace** it with the `.env` value

### `os.getenv("OPENAI_API_KEY")`

Reads the OpenAI secret key from the environment.  
This key proves to OpenAI that **you** are allowed to call the API (and get billed).

### `os.getenv("MODEL_NAME")`

Which model to call, e.g. `gpt-4.1-mini` or `gpt-4.1-nano`.  
Keeping it in `.env` means you can change models without editing code.

> Tip: keep `OPENAI_API_KEY` and `MODEL_NAME` in your `.env` so `load_dotenv()` can find them.

---

## Step 3 — Create the OpenAI client

```python
openai = OpenAI()
```

This builds a **client object** — a helper that knows how to talk to OpenAI.

Important bits:

- You are **not** calling the model yet
- With empty `OpenAI()`, the SDK automatically looks for `OPENAI_API_KEY` in the environment
- Later you use: `openai.chat.completions.create(...)`

Think of it as: **open a phone line**, not yet make the call.

---

## Step 4 — System message

```python
system_message = "You are a helpful assistant"
```

This is the **system prompt**.

| Role | Meaning |
|------|---------|
| `system` | Instructions about *who the model is* and *how it should behave* |
| `user` | The actual question / task from the human |
| `assistant` | The model’s reply (returned by the API) |

Here the system message is simple: be a helpful assistant.  
You can change it later (e.g. “reply in short bullet points” or “explain like I’m 5”).

---

## Step 5 — Define `message_gpt(prompt)`

```python
def message_gpt(prompt):
    """Send user prompt to the LLM and return the reply text."""
```

This is the **core function**.

- **Input:** `prompt` — a string (the user’s question)
- **Output:** a string (the model’s answer text)
- Gradio will call this function every time you click Submit in the UI

### Step 5a — Build the `messages` list

```python
messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": prompt},
]
```

OpenAI Chat Completions expects a **list of message dicts**.

Each dict has:

| Key | Meaning |
|-----|---------|
| `"role"` | Who is speaking: `"system"` or `"user"` (or later `"assistant"`) |
| `"content"` | The text for that role |

So this list means:

1. First tell the model: *You are a helpful assistant*
2. Then tell the model: *Here is the user’s question* (`prompt`)

Why multi-line format? Easier to read and edit than one long line.

### Step 5b — Call the model

```python
response = openai.chat.completions.create(
    model=MODEL_NAME,
    messages=messages,
)
```

This is the **actual API call**.

| Argument | Meaning |
|----------|---------|
| `model=MODEL_NAME` | Which GPT (from `.env`) |
| `messages=messages` | The conversation so far (system + user) |

What comes back (`response`) is a rich object with metadata.  
We usually only care about the text answer.

### Step 5c — Extract the reply text

```python
return response.choices[0].message.content
```

Break it down:

| Piece | Meaning |
|-------|---------|
| `response` | Full API response object |
| `.choices` | List of possible completions (usually length 1) |
| `[0]` | Take the first choice |
| `.message` | The assistant message object |
| `.content` | The actual text string |

So the function returns a plain string like `"Paris"`.

---

## Step 6 — Quick terminal test

```python
print(message_gpt("What is the capital of France?"))
```

Before Gradio starts, this:

1. Calls `message_gpt` once with a fixed question
2. Prints the answer in the terminal

Why keep it?

- Confirms API key + model work **before** opening the UI
- If this fails, the Gradio page will also fail — fix `.env` / network first

You can delete this line later if you only want the UI.

---

## Step 7 — Launch Gradio

```python
gr.Interface(
    fn=message_gpt,
    inputs="textbox",
    outputs="textbox",
    flagging_mode="never",
).launch()
```

This is the UI glue. Bit by bit — and **how Gradio knows where input goes and where output appears**.

### The big idea first

You already wrote a normal Python function:

```python
def message_gpt(prompt):   # ← ONE input argument
    ...
    return reply_text      # ← ONE return value
```

`gr.Interface` does **not** invent new input/output names.  
It **mirrors your function**:

| Your function | Gradio UI |
|---------------|-----------|
| Argument `prompt` | → becomes the **input** widget |
| `return ...` value | → becomes the **output** widget |

So:

```python
gr.Interface(
    fn=message_gpt,        # which function to call
    inputs="textbox",      # widget for the function ARGUMENT
    outputs="textbox",     # widget for the function RETURN value
    flagging_mode="never",
).launch()
```

### How do I know where the input is?

**Rule:**  
`inputs=` describes the widget(s) for the function’s **parameters**, in order.

Your function has **one** parameter: `prompt`.

So you give Gradio **one** input:

```python
inputs="textbox"
```

That creates **one text box** on the page.  
Whatever the user types there is passed as `prompt` into:

```python
message_gpt(prompt)
```

Example:

- User types: `Who is Iron Man?`
- Gradio calls: `message_gpt("Who is Iron Man?")`

You do **not** manually “put” the text into `prompt`. Gradio does that wiring for you.

### How do I know where the output is?

**Rule:**  
`outputs=` describes the widget(s) for the function’s **return value(s)**.

Your function returns **one** string:

```python
return response.choices[0].message.content
```

So you give Gradio **one** output:

```python
outputs="textbox"
```

That creates **another text box** (below / beside, depending on layout).  
Gradio puts the returned string into that box.

Example:

- Function returns: `"Iron Man is Tony Stark..."`
- That text appears in the **output** textbox

### What does `"textbox"` mean? Is it the default?

`"textbox"` is a **shortcut string** meaning: “use Gradio’s Textbox component.”

It is **not** automatic magic with zero config — you still must say `inputs=` and `outputs=`.  
But `"textbox"` is the **simplest / most common** choice for text in and text out.

| You write | Meaning |
|-----------|---------|
| `inputs="textbox"` | Input is a single-line/multi-line text box |
| `outputs="textbox"` | Output is shown as plain text in a text box |

Other common shortcuts later: `"text"`, `"number"`, `"image"`, etc.  
Or full objects like `gr.Textbox(label="Your message:", lines=7)`.

**Defaults around flagging / launch:**

| Setting | Default behavior | In our code |
|---------|------------------|-------------|
| `flagging_mode` | Flag button may appear | We set `"never"` to hide it |
| `.launch()` host | Local machine (`127.0.0.1`) | Default — fine for learning |
| `.launch()` port | Often `7860` | Default unless busy |
| Browser open | Does not always auto-open | Add `inbrowser=True` if you want |

So for beginners: **you must set `fn`, `inputs`, `outputs`**.  
Everything else can stay default at first.

### Picture of the page Gradio builds

```
┌─────────────────────────────────────┐
│  Input textbox   ← inputs="textbox" │
│  (user types here → becomes prompt) │
│                                     │
│           [ Submit ]                │
│                                     │
│  Output textbox  ← outputs="textbox"│
│  (shows return value from fn)       │
└─────────────────────────────────────┘
```

### Matching rule (memorize this)

```
inputs  ↔  function arguments (left to right)
outputs ↔  function return values
```

One argument + one return → one input widget + one output widget.  
That is why our call looks so small.

### If the function had 2 inputs later

```python
def add(a, b):
    return a + b

gr.Interface(fn=add, inputs=["number", "number"], outputs="number").launch()
```

Now:

- 1st number box → `a`
- 2nd number box → `b`
- result number box ← `return a + b`

Same rule: **order of `inputs` = order of arguments**.

### `fn=message_gpt`

“When the user clicks Submit, call this Python function.”

### `flagging_mode="never"`

Hides Gradio’s Flag button (used for marking bad demo outputs).  
Keeps the learning UI clean. Default is not `"never"`, so we set it explicitly.

### `.launch()`

Starts a local web server and prints a URL, usually:

```text
http://127.0.0.1:7860
```

Open that URL → type in the **input** box → Submit → see the answer in the **output** box.

---

## End-to-end: what happens when you click Submit

1. You type `Who is Iron Man?` in the Gradio **input** textbox (`inputs="textbox"`)
2. Gradio calls `message_gpt("Who is Iron Man?")`  ← that string becomes `prompt`
3. Function builds:

```python
[
  {"role": "system", "content": "You are a helpful assistant"},
  {"role": "user", "content": "Who is Iron Man?"},
]
```

4. OpenAI API runs the model named in `MODEL_NAME`
5. Function `return`s the reply string
6. Gradio puts that string into the **output** textbox (`outputs="textbox"`)

---

## How to run

```bash
python 01_gpt_chat.py
```

Stop with `Ctrl+C`.

---

## Common problems

| Problem | Likely cause |
|---------|----------------|
| `OpenAI API Key not set` / auth error | Missing or wrong `OPENAI_API_KEY` in `.env` |
| `MODEL_NAME` is `None` | Add `MODEL_NAME=...` to `.env` |
| Browser page empty / can’t connect | App not running, or wrong URL/port |
| Terminal works, Gradio fails | Same function — check traceback in the terminal where `.launch()` is running |

---

## Tiny experiments to try

1. Change `system_message` to `"Answer in one short sentence only"`
2. Change `outputs="textbox"` to a Markdown output later
3. Remove the `print(message_gpt(...))` line and use only the UI
4. Add `inbrowser=True` inside `.launch(...)` so the browser opens automatically
