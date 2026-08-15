# Gradio Chatbot — `chat(message, history)` explained

Detailed notes for [`gradio_chatbot.py`](./gradio_chatbot.py)  
For basic Gradio (`gr.Interface`), see [`what_is_gradio.md`](./what_is_gradio.md) and [`01_gpt_chat.md`](./01_gpt_chat.md).

---

## Big idea first

`01_gpt_chat.py` uses `gr.Interface` — **one question → one answer**.  
No memory of earlier turns.

`gradio_chatbot.py` uses `gr.ChatInterface` — a **real chat window**.  
Past turns are kept and sent again so the model can remember the conversation.

| App | Gradio class | Memory? |
|-----|--------------|---------|
| `01_gpt_chat.py` | `gr.Interface` | No |
| `gradio_chatbot.py` | `gr.ChatInterface` | Yes (via `history`) |

---

## The launch line

```python
gr.ChatInterface(fn=chat).launch()
```

### Gradio 6 note (important)

Your env has **Gradio 6.x**. In Gradio 6:

- `type="messages"` was **removed**
- messages format is already the **default**

So use:

```python
gr.ChatInterface(fn=chat).launch()
```

Not:

```python
gr.ChatInterface(fn=chat, type="messages").launch()  # TypeError on Gradio 6
```

(Older Gradio 5 examples sometimes show `type="messages"`. Same idea — just drop that argument on Gradio 6.)

### What this does **not** mean

You are **not** calling `chat(...)` yourself here.  
You are **not** passing `message` or `history` yourself.

You only tell Gradio:

> “Here is my function `chat`. When the user clicks Send, **you** call it.”

### What actually happens

1. `.launch()` starts the chat UI in the browser  
2. User types text and clicks **Send**  
3. **Gradio** calls your function behind the scenes:

```python
chat(message="What is Python?", history=[...])
```

4. Your function returns a reply string  
5. Gradio shows that reply in the chat window  
6. Gradio updates history for the next turn

### Who fills the arguments?

| Argument | Who fills it? | Meaning |
|----------|---------------|---------|
| `message` | **Gradio** | New text the user just typed |
| `history` | **Gradio** | Earlier chat turns already on screen |

Think of it like a button callback: you define the function; Gradio presses it and passes the arguments.

### What about history format? (`type="messages"` on Gradio 5)

On Gradio 5, people wrote `type="messages"` to get OpenAI-style history:

```python
[
  {"role": "user", "content": "Hi"},
  {"role": "assistant", "content": "Hello!"},
]
```

On **Gradio 6**, that format is already default — no `type=` needed.  
History still uses `role` + `content` (sometimes `content` is a plain string, sometimes a small list of text parts).

---

## Is `history` a default variable?

**No** — not a Python default like `history=[]` in the function definition.

It is the **2nd argument Gradio always passes** into your chat function.

```python
def chat(message, history):
```

You can rename the parameters:

```python
def chat(msg, past):
```

Gradio still passes:

1. new message first  
2. history second  

The name `history` is just the clear/usual name.

---

## What `chat(message, history)` does (step by step)

Current code idea (simplified):

```python
def get_text(content):
    """Gradio 6 may give content as a string OR a list of parts. Return plain text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                parts.append(part.get("text", ""))
            elif isinstance(part, str):
                parts.append(part)
        return "".join(parts)
    return str(content)


def chat(message, history):
    messages = [{"role": "system", "content": system_message}]

    for turn in history:
        messages.append(
            {"role": turn["role"], "content": get_text(turn["content"])}
        )

    messages.append({"role": "user", "content": message})

    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages)
    return response.choices[0].message.content
```

### Why `get_text(...)`?

On Gradio 6, `history` content can look like either:

```python
# simple string
"HI"

# OR list of parts
[{"type": "text", "text": "HI"}]
```

OpenAI wants plain text strings.  
`get_text(...)` converts both forms into a normal string like `"HI"`.

### Step 1 — start with system message

```python
messages = [{"role": "system", "content": system_message}]
```

Tells the model how to behave (“You are a helpful assistant”).

### Step 2 — add past turns from `history`

```python
for turn in history:
    messages.append(
        {"role": turn["role"], "content": get_text(turn["content"])}
    )
```

Each past turn is a dict with at least:

- `"role"` → `"user"` or `"assistant"`
- `"content"` → text (string or Gradio parts list)

We copy role + plain-text content into `messages`.

### Step 3 — add the new user message

```python
messages.append({"role": "user", "content": message})
```

The brand-new question goes at the end.

### Step 4 — call OpenAI and return the text

```python
response = openai.chat.completions.create(model=MODEL_NAME, messages=messages)
return response.choices[0].message.content
```

Same idea as `01_gpt_chat.py` — but now `messages` includes **memory**.

---

## First Send — `history` is empty

On the **first** message, Gradio usually passes:

```python
history = []
```

### Does the `for` loop run with `turn = NULL`?

**No.**

An empty list means the loop body is **skipped completely**.  
There is no `turn`. Nothing like `NULL` / `None`.

```python
for turn in history:   # history = []  →  runs zero times
    messages.append(...)
```

### First Send — final `messages`

```text
messages = [
  {"role": "system", "content": "You are a helpful assistant"},
  {"role": "user", "content": "Hi"},          ← only the new message
]
```

Empty list ≠ `turn = NULL`.  
Empty list = **loop skipped**.

---

## Second Send — `history` has past turns

After the first reply is shown, Gradio keeps those turns.

Example second question: `"What can you do?"`

Now Gradio might pass:

```python
message = "What can you do?"
history = [
  {"role": "user", "content": "Hi"},
  {"role": "assistant", "content": "Hello! How can I help?"},
]
```

### Loop runs twice

1. append the old user `"Hi"`  
2. append the old assistant `"Hello! How can I help?"`  
3. then append the new user message

### Second Send — final `messages`

```text
messages = [
  {"role": "system", "content": "You are a helpful assistant"},
  {"role": "user", "content": "Hi"},
  {"role": "assistant", "content": "Hello! How can I help?"},
  {"role": "user", "content": "What can you do?"},
]
```

That is why the model can remember earlier chat — you resend the past every time.

---

## Picture of the flow

```
Browser Chat UI
      │
      │  user clicks Send
      ▼
Gradio calls:  chat(message, history)
      │
      ▼
Build messages =
   [system] + history turns + [new user message]
      │
      ▼
OpenAI API
      │
      ▼
return reply text
      │
      ▼
Gradio shows reply + updates history
```

---

## Simple vs hard style (same meaning)

Compact one-liner style (Gradio 5 era):

```python
messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
```

Clearer learning style (what we use on Gradio 6):

```python
messages = [{"role": "system", "content": system_message}]
for turn in history:
    messages.append(
        {"role": turn["role"], "content": get_text(turn["content"])}
    )
messages.append({"role": "user", "content": message})
```

Same idea — the loop version is easier to read, and `get_text` keeps content safe for OpenAI.

---

## Full walkthrough example: you type `HI` → LLM says `HELLO`

This is the most important mental model.

### What `messages = [...]` means

`messages` is a **Python list**.  
Each item in the list is a **dict** with:

- `"role"` → who is speaking (`system` / `user` / `assistant`)
- `"content"` → the text

Example of **one** item (the system message):

```python
{"role": "system", "content": "You are a helpful assistant"}
```

So when code does:

```python
messages = [{"role": "system", "content": "You are a helpful assistant"}]
```

it means:

> `messages` is a list that currently has **exactly 1 dict** inside it — the system prompt.

It does **not** mean a special variable named `system`.  
It means the full dict above.

---

### Turn 1 — you type `HI`

#### Step A — Gradio calls your function

```python
chat(message="HI", history=[])
```

- `message` = `"HI"` (what you typed)
- `history` = `[]` (nothing earlier yet)

#### Step B — build `messages` inside `chat`

```python
messages = [{"role": "system", "content": "You are a helpful assistant"}]
```

Right now `messages` looks like this:

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
]
# list length = 1
```

#### Step C — the `for` loop

```python
for turn in history:   # history is []
    ...
```

Loop runs **0 times**. Nothing is appended.

`messages` is still unchanged:

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
]
# list length still = 1
```

#### Step D — add the new user message

```python
messages.append({"role": "user", "content": "HI"})
```

Now `messages` has **2** dicts:

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "HI"},
]
# list length = 2
```

#### Step E — call the LLM **once**

```python
response = openai.chat.completions.create(model=MODEL_NAME, messages=messages)
return response.choices[0].message.content
```

You hand OpenAI the **whole** `messages` list in **one** API call.

Suppose the model replies: `"HELLO"`

#### Step F — Gradio shows it

Chat window now looks like:

```text
You:  HI
Bot:  HELLO
```

Gradio also **stores** these turns in its own history for next time:

```python
history = [
    {"role": "user", "content": "HI"},
    {"role": "assistant", "content": "HELLO"},
]
```

---

### Turn 2 — you type `How are you?`

#### Step A — Gradio calls your function again

```python
chat(
    message="How are you?",
    history=[
        {"role": "user", "content": "HI"},
        {"role": "assistant", "content": "HELLO"},
    ],
)
```

Notice: Gradio passes the old `HI` / `HELLO` for you. You did not pass them manually.

#### Step B — start with system again

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
]
# list length = 1 again (fresh list each Send)
```

Every Send builds `messages` from scratch. Old turns come back only because Gradio passes them in `history`.

#### Step C — `for` loop now runs **twice** (list building only)

| Loop time | `turn` value | What gets appended |
|-----------|--------------|--------------------|
| 1st | `{"role": "user", "content": "HI"}` | old user message |
| 2nd | `{"role": "assistant", "content": "HELLO"}` | old bot reply |

After the loop:

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "HI"},
    {"role": "assistant", "content": "HELLO"},
]
# list length = 3
```

Still **no LLM call yet**. The loop only copied old chat into the list.

#### Step D — add the new message

```python
messages.append({"role": "user", "content": "How are you?"})
```

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "HI"},
    {"role": "assistant", "content": "HELLO"},
    {"role": "user", "content": "How are you?"},
]
# list length = 4
```

#### Step E — call the LLM **once** again

One API call with this full list.  
The model can “remember” you said HI earlier because those turns are inside `messages`.

---

### Critical point (don’t miss this)

| What | Calls LLM? |
|------|------------|
| `for turn in history:` | **No** — only builds a Python list |
| `messages.append(...)` | **No** — only adds to the list |
| `openai.chat.completions.create(...)` | **Yes** — **one** call per Send click |

So for your example:

- Click Send on `HI` → **1** LLM call → gets `HELLO`
- Click Send on next question → **1** more LLM call (with old turns included)

The loop does **not** send each history item to the LLM separately.

### Tiny analogy

1. Write old chat lines on a notepad (`for` loop)  
2. Write the new question at the bottom (`append`)  
3. Give the **whole notepad** to the teacher once (`create`)

---

## Real terminal output (from a real run)

These prints come from the `print(...)` lines in `gradio_chatbot.py`.  
Your LLM reply text can change slightly each run — the **structure** of `messages` stays the same.

### Turn 1 — typed `HI`, history empty

What Gradio effectively does:

```python
chat(message="HI", history=[])
```

What the terminal printed:

```text
initial messages:
 [{'role': 'system', 'content': 'You are a helpful assistant'}]

final messages:
 [{'role': 'system', 'content': 'You are a helpful assistant'}, {'role': 'user', 'content': 'HI'}]
```

Then the LLM replied (example):

```text
Hello! How can I assist you today?
```

Read it like this:

| Print | Meaning |
|-------|---------|
| `initial messages` | Only system so far — loop has not added anything yet |
| `final messages` | System + new user `HI` — ready for **one** LLM call |
| No old user/assistant turns | Because `history=[]` on first Send |

Pretty form of that final list:

```python
[
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "HI"},
]
```

---

### Turn 2 — typed `How are you?`, history has past turns

After Turn 1, Gradio keeps history like:

```python
[
    {"role": "user", "content": "HI"},
    {"role": "assistant", "content": "Hello! How can I assist you today?"},
]
```

Then Gradio calls:

```python
chat(message="How are you?", history=[...those 2 turns...])
```

What the terminal printed:

```text
initial messages:
 [{'role': 'system', 'content': 'You are a helpful assistant'}]

final messages:
 [{'role': 'system', 'content': 'You are a helpful assistant'}, {'role': 'user', 'content': 'HI'}, {'role': 'assistant', 'content': 'Hello! How can I assist you today?'}, {'role': 'user', 'content': 'How are you?'}]
```

Then the LLM replied (example):

```text
I'm just a helpful AI, so I don't have feelings, but I'm here and ready to assist you! How can I help you today?
```

Pretty form of that final list:

```python
[
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "HI"},
    {"role": "assistant", "content": "Hello! How can I assist you today?"},
    {"role": "user", "content": "How are you?"},
]
```

Notice:

1. `initial` is **always** only system (fresh list each Send)  
2. `final` includes old `HI` + old assistant reply + new question  
3. Still **one** LLM call — the loop only packed history into the list

---

### Bonus — Gradio 6 may pass content as a parts list

Sometimes history looks like this (not a plain string):

```python
[
    {"role": "user", "content": [{"type": "text", "text": "HI"}]},
    {"role": "assistant", "content": [{"type": "text", "text": "HELLO"}]},
]
```

`get_text(...)` converts that to plain `"HI"` / `"HELLO"`.  
After conversion, final messages printed as:

```text
final messages:
 [{'role': 'system', 'content': 'You are a helpful assistant'}, {'role': 'user', 'content': 'HI'}, {'role': 'assistant', 'content': 'HELLO'}, {'role': 'user', 'content': 'How are you?'}]
```

So OpenAI still receives normal strings.

---

## How to run

```bash
python gradio_chatbot.py
```

Open the local URL Gradio prints (usually `http://127.0.0.1:7860`).  
Stop with `Ctrl+C`.

---

## Quick memory checklist

| Question | Answer |
|----------|--------|
| Do I pass `history` in `.launch()`? | No — Gradio passes it when calling `chat` |
| Is `history` a Python default arg? | No — it’s the 2nd argument Gradio always supplies |
| First message: what is `history`? | Usually `[]` |
| First message: what about the `for` loop? | Skipped entirely (no `turn`) |
| Why keep history? | So the LLM gets past turns and can “remember” |
| Launch line on Gradio 6? | `gr.ChatInterface(fn=chat).launch()` |
| `type="messages"` on Gradio 6? | Removed — messages format is already default |
| Why `get_text`? | History `content` may be a string or a list of text parts |

---

## Common problems

| Problem | Likely cause / fix |
|---------|---------------------|
| `unexpected keyword argument 'type'` | Gradio 6 — remove `type="messages"` |
| Auth / model errors | Check `.env` for `OPENAI_API_KEY` and `MODEL_NAME` |
| Odd history content | Use `get_text(turn["content"])` before sending to OpenAI |

---

## Related files

| File | What it teaches |
|------|-----------------|
| [`01_gpt_chat.py`](./01_gpt_chat.py) | Single prompt UI (`gr.Interface`) — no chat memory |
| [`gradio_chatbot.py`](./gradio_chatbot.py) | Chat UI with memory (`gr.ChatInterface`) |
| [`what_is_gradio.md`](./what_is_gradio.md) | What Gradio is + Interface options |
| [`01_gpt_chat.md`](./01_gpt_chat.md) | Line-by-line for the simple GPT UI |
