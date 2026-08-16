# What Is Gradio?

Personal learning notes: what Gradio is, why people use it with LLMs, and how a tiny UI is built.

Companion script in this folder: [`01_gpt_chat.py`](./01_gpt_chat.py) · line-by-line walkthrough: [`01_gpt_chat.md`](./01_gpt_chat.md)

---

## Why Gradio exists

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

---

## Launch options (good to know)

These are optional knobs on `.launch(...)` or `gr.Interface(...)`. You do **not** need them for the basic GPT chat app. Useful knowledge.

### Open browser automatically

```python
gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch(inbrowser=True)
```

| Piece | Meaning |
|-------|---------|
| `inbrowser=True` | Gradio opens a new browser tab/window for you |

Without it, Gradio still runs — you just copy/open the printed URL yourself.

### Public share link

```python
gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch(share=True)
```

| Piece | Meaning |
|-------|---------|
| `share=True` | Creates a temporary **public** Gradio URL (tunnel) so others can open your demo |

Notes:

- Cool for quick demos / sharing with someone else
- Uses HTTP tunneling (similar idea to ngrok)
- Some antivirus tools and company networks **block** this
- If it errors at work, just skip it and use local URL only
- More permanent hosting later: **Hugging Face Spaces**

### Authentication (simple username + password)

```python
gr.Interface(
    fn=shout,
    inputs="textbox",
    outputs="textbox",
    flagging_mode="never",
).launch(inbrowser=True, auth=("ed", "bananas"))
```

| Piece | Meaning |
|-------|---------|
| `auth=("ed", "bananas")` | Browser asks for userid + password before showing the app |
| `"ed"` | example username |
| `"bananas"` | example password |

What to remember:

- Gradio makes basic login **very easy**
- This is fine for a quick private demo
- For anything real, **do not hardcode passwords in code** — at minimum put them in `.env`
- This is a simple gate, not full production security

Example idea with `.env`:

```python
# concept only — read user/pass from environment instead of hardcoding
auth=(os.getenv("GRADIO_USER"), os.getenv("GRADIO_PASS"))
```

### Dark mode vs light mode

By default, Gradio follows **your computer / browser theme**:

- OS/browser in dark → Gradio often looks dark
- OS/browser in light → Gradio often looks light

That is why two people can run the same code and see different themes.

#### Forcing dark mode (optional)

Gradio **recommends against** forcing a theme, because theme should stay a **user preference** (especially for accessibility).  
But if you want to force dark mode anyway, here is the pattern:

```python
# Define this JS snippet, then pass js=force_dark_mode when creating the Interface

force_dark_mode = """
function refresh() {
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.href = url.href;
    }
}
"""

gr.Interface(
    fn=shout,
    inputs="textbox",
    outputs="textbox",
    flagging_mode="never",
    js=force_dark_mode,
).launch()
```

What this does (plain English):

1. Small JavaScript runs in the browser
2. Checks the page URL for `__theme=dark`
3. If missing, reloads the page with `__theme=dark`
4. Gradio then renders in dark mode

| Piece | Meaning |
|-------|---------|
| `js=force_dark_mode` | Extra browser JS attached to the Interface |
| `__theme=dark` | Gradio’s URL switch for dark theme |

**Learning takeaway:** default = follow user settings. Force dark only if you really want a fixed look for demos/screenshots.

### Quick cheat sheet

| Option | Where | What it does |
|--------|--------|----------------|
| `launch()` | `.launch()` | Local only |
| `inbrowser=True` | `.launch(...)` | Auto-open browser |
| `share=True` | `.launch(...)` | Temporary public link |
| `auth=("user", "pass")` | `.launch(...)` | Simple login gate |
| `js=force_dark_mode` | `gr.Interface(...)` | Force dark theme via URL |
| `flagging_mode="never"` | `gr.Interface(...)` | Hide Flag button |

---

## Custom widgets: `inputs=[...]` and `outputs=[...]`

So far the simple form is:

```python
inputs="textbox"
outputs="textbox"
```

That works. Next you can build a **nicer UI** by creating widgets yourself and passing them as **lists**:

```python
inputs=[message_input]
outputs=[message_output]
```

### Why lists?

| Style | When |
|-------|------|
| `inputs="textbox"` | One simple input, Gradio picks defaults |
| `inputs=[message_input]` | One input, but **you** control label / lines / hint |
| `inputs=[box1, box2]` | Two inputs → maps to two function arguments |

Same idea for `outputs`.

### Example 1 — Shout with custom textboxes

```python
message_input = gr.Textbox(
    label="Your message:",
    info="Enter a message to be shouted",
    lines=7,
)
message_output = gr.Textbox(label="Response:", lines=8)

view = gr.Interface(
    fn=shout,
    title="Shout",
    inputs=[message_input],
    outputs=[message_output],
    examples=["hello", "howdy"],
    flagging_mode="never",
)
view.launch()
```

| Piece | Meaning |
|-------|---------|
| `gr.Textbox(...)` | Create a text box widget object |
| `label=` | Title shown above the box |
| `info=` | Small help text under the label |
| `lines=` | How tall the box is |
| `inputs=[message_input]` | Use **this** widget as the input |
| `outputs=[message_output]` | Use **this** widget as the output |
| `title="Shout"` | App title at the top of the page |
| `examples=[...]` | Clickable sample prompts under the UI |
| `view = gr.Interface(...)` then `view.launch()` | Same as chaining `.launch()`, just stored in a variable |

### Example 2 — Same UI pattern, but `fn=message_gpt`

```python
message_input = gr.Textbox(
    label="Your message:",
    info="Enter a message for GPT-4.1-mini",
    lines=7,
)
message_output = gr.Textbox(label="Response:", lines=8)

view = gr.Interface(
    fn=message_gpt,
    title="GPT",
    inputs=[message_input],
    outputs=[message_output],
    examples=["hello", "howdy"],
    flagging_mode="never",
)
view.launch()
```

Only `fn` and title/info text changed. The input/output wiring is the same.

### Example 3 — Output as Markdown (nicer for LLM replies)

```python
system_message = "You are a helpful assistant that responds in markdown without code blocks"

message_input = gr.Textbox(
    label="Your message:",
    info="Enter a message for GPT-4.1-mini",
    lines=7,
)
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=message_gpt,
    title="GPT",
    inputs=[message_input],
    outputs=[message_output],
    examples=[
        "Explain the Transformer architecture to a layperson",
        "Explain the Transformer architecture to an aspiring AI engineer",
    ],
    flagging_mode="never",
)
view.launch()
```

| Output type | Looks like |
|-------------|------------|
| `gr.Textbox` | Plain text |
| `gr.Markdown` | Formatted markdown (headings, bold, lists) |

### Simple vs custom — side by side

```python
# Simple (our 01_gpt_chat.py style)
gr.Interface(fn=message_gpt, inputs="textbox", outputs="textbox", flagging_mode="never").launch()

# Custom widgets (richer style)
gr.Interface(
    fn=message_gpt,
    title="GPT",
    inputs=[message_input],
    outputs=[message_output],
    examples=["hello", "howdy"],
    flagging_mode="never",
).launch()
```

Same wiring rule as before:

```
inputs  ↔ function arguments
outputs ↔ function return value
```

You only gained control over labels, size, examples, and output format.

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

## `gr.Interface` vs `gr.ChatInterface`

These are the two Gradio UIs you use most in this folder.  
They are **not** the same.

### `gr.Interface` — simple form UI

Best for: **one input → one output** (like a form).

```python
gr.Interface(
    fn=message_gpt,
    inputs="textbox",
    outputs="textbox",
    flagging_mode="never",
).launch()
```

| Piece | Meaning |
|-------|---------|
| `fn=` | Your function (e.g. `message_gpt(prompt)`) |
| `inputs=` | Widget(s) for function **arguments** |
| `outputs=` | Widget(s) for function **return value** |

Looks like: type in a box → Submit → see answer in another box.  
**No chat memory** unless you build it yourself.

Used in: [`01_gpt_chat.py`](./01_gpt_chat.py)

### `gr.ChatInterface` — chat bubble UI

Best for: **multi-turn chat** (like ChatGPT).

```python
gr.ChatInterface(fn=chat).launch()
```

| Piece | Meaning |
|-------|---------|
| `fn=` | Your chat function, usually `chat(message, history)` |
| `message` | New text the user just typed (Gradio passes this) |
| `history` | Earlier turns already on screen (Gradio passes this) |

Looks like: chat bubbles, Send button, conversation grows.  
Gradio keeps **history** and passes it into your function each time.

Used in: [`gradio_chatbot.py`](./gradio_chatbot.py)

### Side by side

| | `gr.Interface` | `gr.ChatInterface` |
|---|----------------|---------------------|
| UI style | Form (textbox in / out) | Chat bubbles |
| Typical function | `fn(prompt)` | `fn(message, history)` |
| Memory | No (one shot) | Yes (Gradio sends history) |
| You set `inputs=` / `outputs=` | Yes | Usually no — chat UI is built-in |
| Good for | Single Q&A, demos | Real chatbot |

### Tiny mental model

```text
gr.Interface      →  form page
gr.ChatInterface  →  chat page
```

Same idea underneath: Gradio calls **your Python function**.  
Only the UI shape and arguments differ.

### Gradio 6 chatbot tip

On Gradio 6.x use:

```python
gr.ChatInterface(fn=chat).launch()
```

Do **not** pass `type="messages"` (removed in Gradio 6; older Gradio 5 examples sometimes still show it).

More detail on `message` / `history`: [`gradio_chatbot.md`](./gradio_chatbot.md)

---

## Learning path (simple → richer)

## How to run

```bash
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
