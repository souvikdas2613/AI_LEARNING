# What Is Gradio?

Personal learning notes: what Gradio is, why people use it with LLMs, and how a tiny UI is built.

Companion script in this folder: [`01_gpt_chat.py`](./01_gpt_chat.py) · line-by-line walkthrough: [`01_gpt_chat.md`](./01_gpt_chat.md)

Based on Udemy LLM Engineering **week2 / day2**.

---

## Course intro (why Gradio exists)

If you have experience with front-end development or have dabbled in it, you know that setting up a React app or similar involves a lot of **boilerplate code**. However, with models, we do not need to do that. We can build a user interface **super quickly**, and that is exactly what we will do today.

**Gradio** is actually part of **Hugging Face**. It was a startup acquired by Hugging Face a couple of years ago, so Gradio is now part of the Hugging Face family. Gradio lets you build and share delightful machine learning apps. I believe you will be delighted by it.

The key is the magical line:

```python
import gradio as gr
```

which is the common convention.

You write a function to perform a task. For example, the function `greet` takes a name and replies with `"Hello, name."` Then, you create a user interface based on that function by specifying **inputs** and **outputs**. You get a user interface built for you just like that.

```python
def greet(name):
    return "Hello, " + name

gr.Interface(fn=greet, inputs="textbox", outputs="textbox").launch()
```

That is exactly what we are going to do. We will create a UI for API calls to **GPT**, **Claude**, and **Gemini** so that you can see how to expose these models.

---

## What is Gradio?

**Gradio** is a Python library that turns a normal Python **function** into a **web user interface** (UI) with almost no frontend code.

You write:

```python
def shout(text):
    return text.upper()
```

Then Gradio can show a browser page with:

- an input box (type text)
- a button (Submit)
- an output box (see `HELLO`)

You do **not** write HTML, CSS, or JavaScript for the basic case. Gradio builds the page for you.

### Plain meaning

| Piece | Meaning |
|--------|---------|
| **Gradio** | Python package (`import gradio as gr`) — now part of Hugging Face |
| **UI** | What the user sees and clicks in the browser |
| **`gr.Interface`** | Connects your function to input/output widgets |
| **`.launch()`** | Starts a small local web server and opens the app |

---

## Why Gradio matters for LLM learning

When you call OpenAI from a script, the flow is:

```
terminal → python script → OpenAI API → print reply in terminal
```

That works for learning, but it is not how users chat with AI. Gradio upgrades the same idea to:

```
browser UI → your Python function → OpenAI API → reply shown in the UI
```

So you keep writing **Python functions**, but people interact with them like a mini ChatGPT.

**Mental model:**

```
┌──────────────────┐
│  Browser (UI)    │  ← Gradio builds this
│  textbox + btn   │
└────────┬─────────┘
         │ calls your function
         ▼
┌──────────────────┐
│  message_gpt()   │  ← your Python
└────────┬─────────┘
         │ API call
         ▼
┌──────────────────┐
│  OpenAI model    │
└──────────────────┘
```

---

## Core idea: wrap a function

Gradio does **not** replace OpenAI. It only wraps whatever function you give it.

```python
gr.Interface(
    fn=message_gpt,      # which Python function to run
    inputs="textbox",    # what the user types into
    outputs="textbox",   # where the return value is shown
    flagging_mode="never",
).launch()
```

When the user clicks Submit:

1. Gradio takes the textbox text
2. Calls `message_gpt(that_text)`
3. Puts the returned string into the output textbox

Same pattern works for non-AI functions too (`shout`, reverse string, word count, etc.).

---

## Important Gradio pieces

### 1. `import gradio as gr`

Common short alias. Almost every Gradio tutorial uses `gr`.

### 2. `gr.Interface(...)`

The simplest Gradio app builder.

| Argument | Role |
|----------|------|
| `fn=` | Your Python function |
| `inputs=` | Input widget(s). `"textbox"` is the simplest |
| `outputs=` | Output widget(s). `"textbox"` shows plain text |
| `flagging_mode="never"` | Hides the “Flag” button (used for collecting bad outputs) |

Later you can use richer widgets: `gr.Markdown`, dropdowns, images, audio, etc.

### 3. `.launch()`

Starts the app.

Typical local URL:

```text
http://127.0.0.1:7860
```

Open that in a browser. Stop the app with `Ctrl+C` in the terminal.

Useful options you will see in day2:

| Option | What it does |
|--------|----------------|
| `launch()` | Local only (this machine) |
| `launch(inbrowser=True)` | Also opens the browser automatically |
| `launch(share=True)` | Creates a temporary public Gradio link (tunnel) |
| `launch(auth=("user", "pass"))` | Simple password gate |

> Note: `share=True` can be blocked by antivirus / company networks. Skip it if it errors.

---

## Gradio vs other things (don’t mix them up)

| Thing | What it is |
|-------|------------|
| **Gradio** | Quick Python → web UI library |
| **OpenAI / Ollama** | The LLM you call from inside `fn` |
| **ChatGPT website** | A finished product UI (not your code) |
| **Streamlit / Dash** | Other Python UI tools (similar idea, different API) |
| **Hugging Face Spaces** | Place to host Gradio apps permanently |

Gradio is the **front door**. The LLM is the **brain** behind the door.

---

## Day2 learning path (simple → richer)

1. **Pure Python function** — `shout(text)` returns uppercase (no LLM)
2. **Gradio Interface** — same function, now in a browser
3. **Swap fn to GPT** — `message_gpt(prompt)` talks to OpenAI
4. **Better output** — Markdown instead of plain textbox
5. **Streaming** — show tokens as they arrive (`yield`)
6. **Chat UI** — multi-turn chat with history (`ChatInterface`)

This folder starts at steps 2–3 with [`01_gpt_chat.py`](./01_gpt_chat.py).

---

## How to run

```bash
conda activate my-proj
python 01_gpt_chat.py
```

Needs packages: `gradio`, `openai`, `python-dotenv`  
Needs `.env` with `OPENAI_API_KEY` and `MODEL_NAME`.

---

## What to read next

| File | Purpose |
|------|---------|
| [`01_gpt_chat.md`](./01_gpt_chat.md) | Every line of `01_gpt_chat.py` explained |
| [`01_gpt_chat.py`](./01_gpt_chat.py) | The actual script |

Also related from earlier folders:

- System vs user prompts — `2_USER_PROMPT_SYSTEM_PROMPT/`
- What an LLM is — `3_LLMs_and_TOKENS/what_is_an_llm.md`
