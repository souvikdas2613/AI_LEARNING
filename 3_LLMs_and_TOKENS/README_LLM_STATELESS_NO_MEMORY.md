# LLM Calls Are Stateless — No Built-in Memory

Companion notes for `LLM_CALL_STATELESS_NO_MEMORY.py`.

Key idea: ChatGPT *feels* like it remembers you — but each API call starts from scratch unless **you** send the history again.

---

## The big idea (recap)

1. **Every call to an LLM is stateless** — the model does not keep your previous request in memory on the server between calls.
2. **We pass in the entire conversation so far** in the `messages` list, every time.
3. That **gives the illusion of memory** — it looks like the model “remembers” the chat.
4. **It is a trick** — a by-product of *you* resending the full conversation.
5. An LLM mainly **predicts the next likely tokens**. If the prompt sequence already contains “Hi! I'm Souvik” and later “What's my name?”, it can predict “Souvik”.

ChatGPT (the product) uses the same pattern: each new message is sent with the whole thread so far. You pay for those earlier tokens again — and that is intentional, because you *want* the model to condition on the full history.

---

## What this script demonstrates

Three API calls:

| Call | What you send | Result |
|------|----------------|--------|
| 1 | System + “Hi! I'm Souvik” | Greets you by name |
| 2 | System + “What's my name?” only | Does **not** know your name |
| 3 | Full history (user + assistant + follow-up) | Answers **Souvik** |

Call 2 proves there is no memory. Call 3 shows how we fake it by resending the conversation.

---

## How the script works

### Setup

```python
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME')
openai = OpenAI()
```

Uses `.env` (`OPENAI_API_KEY`, `MODEL_NAME` — e.g. `gpt-4.1-nano`).

### Call 1 — introduce yourself

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hi! I'm Souvik"}
]
response = openai.chat.completions.create(model=MODEL_NAME, messages=messages)
reply_1 = response.choices[0].message.content
```

### Call 2 — ask for the name (fresh messages list)

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What's my name?"}
]
response = openai.chat.completions.create(model=MODEL_NAME, messages=messages)
```

Notice: Call 2 builds a **new** `messages` list. Nothing from Call 1 is included.

### Call 3 — same question, but with full history

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hi! I'm Souvik"},
    {"role": "assistant", "content": reply_1},
    {"role": "user", "content": "What's my name?"}
]
response = openai.chat.completions.create(model=MODEL_NAME, messages=messages)
```

`reply_1` is the real Call 1 answer, so the model sees the prior turn and can answer with your name.

---

## Example output (real run)

```text
API key found and looks good so far!


Model name found gpt-4.1-nano and looks good so far!





===========CALL LLM - STATELESS - NO MEMORY ===================================



Hello Souvik! Nice to meet you. How can I assist you today?



===========CALL LLM - STATELESS - NO MEMORY - 2 ===================================



I'm sorry, but I don't have that information. Could you please tell me your name?



===========CALL LLM - WITH FULL HISTORY (FAKE MEMORY) - 3 ===================================



Your name is Souvik. How can I help you today?
```

### How to read this

| Call | Model reply | Why |
|------|-------------|-----|
| 1 | Greets **Souvik** | The name was in *this* request’s `messages` |
| 2 | **Does not know** the name | New request; “Souvik” was never sent again |
| 3 | **Your name is Souvik** | Full history was passed in again |

That “Wait, what?? We just told you!” moment (Call 2) is the AHA: **stateless**. Call 3 shows the fix.

---

## How “memory” is faked (the fix)

To make the model answer “Souvik”, **you** must resend the prior turns (as Call 3 does).

Now the prompt sequence contains the name, so next-token prediction can answer with it.

As an AI engineer, **managing conversation history** (what to keep, truncate, summarize) is part of your job — the API does not do it for free.

---

## Mental model

```text
Call 1:  [system] [user: Hi! I'm Souvik]  →  "Hello, Souvik! ..."
              ↓
         (server forgets — no session memory for your app)

Call 2:  [system] [user: What's my name?]  →  "I don't know..."
              ↑
         No prior turns in this payload
```

With history injected:

```text
Call 3:  [system] [user: Hi! I'm Souvik] [assistant: ...] [user: What's my name?]
         →  "Your name is Souvik"
```

---

## Cost note

Sending the full history every time means you **pay again** for earlier tokens. That is expected: you are buying compute over the whole sequence so the model can condition on it.

---

## Run it yourself

```bash
python LLM_CALL_STATELESS_NO_MEMORY.py
```

---

## Summary

- LLM API calls are **stateless**.
- “Memory” = **you** resending the conversation in `messages`.
- Call 2 fails on purpose to prove that; Call 3 succeeds with full history.
- Chat products feel sticky only because they keep and resubmit the thread for you.
