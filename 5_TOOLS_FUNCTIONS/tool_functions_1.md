# `tool_functions_1.py` — every bit explained

Detailed notes for `[tool_functions_1.py](./tool_functions_1.py)`  
(Tools / function calling notes.)

Related earlier notes: Gradio chatbot memory in `4_GRADIO/gradio_chatbot.md`.

---

## What this Python file does (one sentence)

It builds a **FlightAI Gradio chatbot** that can answer normally **and** call a real Python function (`get_ticket_price`) when the user asks about ticket prices.

---

## Big idea: what is a “tool”?

Normally the LLM only returns text.

With **tools** (also called **function calling**):

1. You give the LLM a **menu of functions** it is allowed to request
2. Sometimes the LLM replies: “Please run `get_ticket_price` with city=`Paris`”
3. **Your Python code** runs that function
4. You send the function result back to the LLM
5. The LLM writes a final human answer using that result

Important: the LLM does **not** magically execute your Python.  
It only **asks** you to run it. You run it.

```text
User: "How much is a ticket to Paris?"
        │
        ▼
OpenAI (with tools=...)
        │
        │  finish_reason = "tool_calls"
        │  wants: get_ticket_price(destination_city="Paris")
        ▼
Your Python: handle_tool_call → get_ticket_price("Paris")
        │
        │  returns: "The price of a ticket to Paris is $899"
        ▼
OpenAI again (now has tool result)
        │
        ▼
Final reply to user: short courteous sentence with the price
```

---



## How to run

```bash
python tool_functions_1.py
```

Open the Gradio URL (usually `http://127.0.0.1:7860`).  
Try: `How much is a ticket to Paris?`  
In the terminal you should also see: `Tool called for city Paris`

---



## Step 1 — Imports

```python
import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import json
```


| Import         | Why                                            |
| -------------- | ---------------------------------------------- |
| `os`           | Read env vars (`OPENAI_API_KEY`, `MODEL_NAME`) |
| `load_dotenv`  | Load secrets from `.env`                       |
| `OpenAI`       | Call the Chat Completions API                  |
| `gradio as gr` | Chat UI (`ChatInterface`)                      |
| `json`         | Parse tool arguments string → Python dict      |


---



## Step 2 — Load config

```python
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
```

Same pattern as earlier folders.  
`OpenAI()` later uses `OPENAI_API_KEY` from the environment.

---



## Step 3 — The real Python tool (your business logic)

```python
ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}

def get_ticket_price(destination_city):
    print(f"Tool called for city {destination_city}")
    price = ticket_prices.get(destination_city.lower(), "Unknown ticket price")
    return f"The price of a ticket to {destination_city} is {price}"
```



### `ticket_prices`

A simple dictionary: city name → price string.

### `get_ticket_price(destination_city)`


| Bit                                 | Meaning                                                 |
| ----------------------------------- | ------------------------------------------------------- |
| `destination_city.lower()`          | Make lookup case-insensitive (`Paris` → `paris`)        |
| `.get(..., "Unknown ticket price")` | If city missing, return unknown instead of crashing     |
| `print(...)`                        | So you can see in the terminal when the tool really ran |
| `return f"..."`                     | Text result that will be sent back to the LLM           |


This is normal Python. No OpenAI inside this function.

---



## Step 4 — `get_text(content)` (Gradio 6 helper)

```python
def get_text(content):
    if isinstance(content, list):
        return content[0]["text"]
    return content
```

Gradio 6 chat history `content` may be:

```python
"HI"
# or
[{"type": "text", "text": "HI"}]
```

OpenAI wants a plain string.  
This tiny helper converts both forms to `"HI"`.

---



## Step 5 — Tool schema: `price_function`

This is **not** the Python function itself.  
It is a **JSON-like description** you show the LLM so it knows:

- the tool name  
- what it does  
- what arguments it needs

```python
price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}
```


| Field                         | Meaning                                                             |
| ----------------------------- | ------------------------------------------------------------------- |
| `name`                        | Must match your real Python function name idea (`get_ticket_price`) |
| `description`                 | Helps the model decide **when** to use this tool                    |
| `parameters`                  | Describes the argument object                                       |
| `properties.destination_city` | One string argument: the city                                       |
| `required`                    | Model must provide `destination_city`                               |
| `additionalProperties: False` | Don’t invent extra args                                             |


Think of this as the **menu card** for the waiter (LLM).

---



## Step 6 — Wrap it in `tools`

```python
tools = [{"type": "function", "function": price_function}]
```

OpenAI expects a **list of tools**.  
Each tool item has:

- `"type": "function"`  
- `"function": <the schema dict>`

Later you pass `tools=tools` into `chat.completions.create(...)`.

---



## Step 7 — `handle_tool_call(message)`

When the model asks to use a tool, OpenAI returns an assistant message containing `tool_calls`.  
This function:

1. reads that request
2. runs your Python
3. builds a **tool role** message to send back

```python
def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    if tool_call.function.name == "get_ticket_price":
        arguments = json.loads(tool_call.function.arguments)
        city = arguments.get("destination_city")
        price_details = get_ticket_price(city)
        response = {
            "role": "tool",
            "content": price_details,
            "tool_call_id": tool_call.id
        }
    return response
```



### Bit by bit


| Line                                | Meaning                                               |
| ----------------------------------- | ----------------------------------------------------- |
| `message.tool_calls[0]`             | Take the first tool request (this demo handles one)   |
| `tool_call.function.name`           | Which tool did the model ask for?                     |
| `tool_call.function.arguments`      | JSON **string** like `'{"destination_city":"Paris"}'` |
| `json.loads(...)`                   | Convert that string → Python dict                     |
| `arguments.get("destination_city")` | Extract the city                                      |
| `get_ticket_price(city)`            | Run your real function                                |
| `"role": "tool"`                    | Special role meaning “tool result”                    |
| `"content": price_details`          | The tool’s answer text                                |
| `"tool_call_id": tool_call.id`      | Links this result to the exact tool request           |


Without the matching `tool_call_id`, OpenAI cannot connect request ↔ result.

---



## Step 8 — OpenAI client + system prompt

```python
openai = OpenAI()

system_message = """
You are a helpful assistant for an Airline called FlightAI.
Give short, courteous answers, no more than 1 sentence.
Always be accurate. If you don't know the answer, say so.
"""
```


| Piece               | Role                                              |
| ------------------- | ------------------------------------------------- |
| `openai = OpenAI()` | Client object for API calls                       |
| `system_message`    | Airline personality + short answers + be accurate |


---



## Step 9 — `chat(message, history)` — the main flow

This is what Gradio calls on every Send.

```python
def chat(message, history):
    history = [{"role": h["role"], "content": get_text(h["content"])} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)

    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        tool_response = handle_tool_call(message)
        messages.append(message)
        messages.append(tool_response)
        response = openai.chat.completions.create(model=MODEL_NAME, messages=messages)

    return response.choices[0].message.content
```



### 9a — Clean history for Gradio 6

```python
history = [{"role": h["role"], "content": get_text(h["content"])} for h in history]
```

Builds a clean list of `{role, content}` with plain-text content.

### 9b — Build full messages

```python
messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
```

Same chatbot pattern as before:

```text
[system] + [past turns] + [new user message]
```



### 9c — First LLM call (with tools enabled)

```python
response = openai.chat.completions.create(
    model=MODEL_NAME,
    messages=messages,
    tools=tools,
)
```

Now the model can either:

- answer directly with text, **or**
- request a tool (`finish_reason == "tool_calls"`)



### 9d — If tool requested

```python
if response.choices[0].finish_reason == "tool_calls":
    message = response.choices[0].message      # assistant message with tool_calls
    tool_response = handle_tool_call(message) # run Python tool
    messages.append(message)                  # keep assistant tool request
    messages.append(tool_response)            # add tool result
    response = openai.chat.completions.create( # second LLM call
        model=MODEL_NAME,
        messages=messages,
    )
```


| Append                                | Why                               |
| ------------------------------------- | --------------------------------- |
| assistant `message` (with tool_calls) | Shows what the model asked to run |
| `tool_response`                       | Shows what your tool returned     |


Then the **second** `create(...)` asks the model to write the final user-facing sentence.

### 9e — Return final text

```python
return response.choices[0].message.content
```

Gradio shows this string in the chat UI.

---



## Step 10 — Launch Gradio

```python
gr.ChatInterface(fn=chat).launch()
```


| Note      | Detail                                                      |
| --------- | ----------------------------------------------------------- |
| Gradio 6  | Do **not** pass `type="messages"` / `type="chat"` (removed) |
| `fn=chat` | Gradio calls `chat(message, history)` on Send               |


---



## Example walkthrough: you typed `ticket price for paris ?`

This is a real Gradio run explanation.

### What you see in the Gradio UI

```text
You:  ticket price for paris ?
Bot:  The ticket price for Paris is $899.
```

That final bot line is from the **second** LLM call (after the tool result).  
The prints below are what happened **before** that sentence appeared.

### Full terminal print trace (real run)

#### 1) `chat` runs — first LLM call asks for a tool

```text
----------CHAT FUNCTION RUNNING----------------------
Choice(
  finish_reason='tool_calls',
  message=ChatCompletionMessage(
    content=None,
    role='assistant',
    tool_calls=[
      Function(
        name='get_ticket_price',
        arguments='{"destination_city":"Paris"}'
      )
    ]
  )
)
```

Meaning:

- model is **not** answering with price text yet (`content=None`)
- it requests tool `get_ticket_price`
- it fills `destination_city` from your words (`paris`)

#### 2) Tool-call branch starts

```text
----------TOOL CALL FUNCTION RUNNING----------------------
ChatCompletionMessage(... tool_calls=[... Paris ...])
```

Same assistant message is passed into `handle_tool_call(...)`.

#### 3) `handle_tool_call` unpacks the request

```text
----------HANDLE TOOL CALL FUNCTION RUNNING----------------------
ChatCompletionMessageFunctionToolCall(
  id='call_3OBQaWUIBKnycvF1O56R0qIW',
  function=Function(
    arguments='{"destination_city":"Paris"}',
    name='get_ticket_price'
  )
)

----------TOOL CALL FUNCTION NAME----------------------
get_ticket_price

----------ARGUMENTS----------------------
{'destination_city': 'Paris'}

----------CITY----------------------
Paris
```

Here your code:

1. reads `tool_calls[0]`
2. checks name = `get_ticket_price`
3. `json.loads(arguments)` → `{'destination_city': 'Paris'}`
4. extracts city = `Paris`

#### 4) Real Python tool runs

```text
Tool called for city Paris

----------PRICE DETAILS----------------------
The price of a ticket to Paris is $899
```

This comes from:

```python
get_ticket_price("Paris")
# uses ticket_prices["paris"] → "$899"
```

#### 5) Build the tool-role message for OpenAI

```text
----------RESPONSE----------------------
{
  'role': 'tool',
  'content': 'The price of a ticket to Paris is $899',
  'tool_call_id': 'call_3OBQaWUIBKnycvF1O56R0qIW'
}

----------TOOL RESPONSE FUNCTION RUNNING----------------------
{ same dict as above }
```

Important: `tool_call_id` matches the call id from step 1.  
That is how OpenAI links “this result” to “that tool request”.

#### 6) Second LLM call → Gradio shows final answer

Your code appends:

1. assistant tool-request message  
2. tool result message  

Then calls OpenAI again.  
Model writes the user-facing sentence, e.g.:

```text
The ticket price for Paris is $899.
```

That is what appears in the chat bubble.

### How did it get `arguments='{"destination_city":"Paris"}'`?

**You did not hardcode `"Paris"` in Python.**  
The **LLM** created that JSON.

It used:

| What you sent | What the model used it for |
|---------------|----------------------------|
| User text: `ticket price for paris ?` | Saw the city is Paris |
| Tool schema `price_function` | Knew the arg name must be `destination_city` |
| `tools=tools` in the API call | Knew it may call `get_ticket_price` |

So:

```text
your words ("paris")
        +
tool schema (destination_city)
        ↓
LLM generates:
arguments='{"destination_city":"Paris"}'
```

Then your code does:

```python
json.loads(...)           # → {"destination_city": "Paris"}
get_ticket_price("Paris") # real Python lookup
```

### End-to-end picture for this run

```text
Gradio UI: "ticket price for paris ?"
        ↓
chat() → OpenAI #1 (tools enabled)
        ↓
finish_reason=tool_calls, city=Paris
        ↓
handle_tool_call → get_ticket_price("Paris") → "$899"
        ↓
chat() → OpenAI #2 (with tool result)
        ↓
Gradio UI: "The ticket price for Paris is $899."
```

### Real print: why the second `create(...)` still happens

Even after the tool price is already in `messages`, you call OpenAI again.
Here is what that looks like in a real run.

#### Tool result is ready

```text
----------TOOL RESPONSE FUNCTION RUNNING----------------------
{
  'role': 'tool',
  'content': 'The price of a ticket to Paris is $899',
  'tool_call_id': 'call_7Ze1tUl3j7xUpGKMFCwXrIo4'
}
```

#### `messages` now has 4 parts (fact pack for the model)

```text
----------MESSAGES----------------------
[
  {role: system,    content: FlightAI instructions...},
  {role: user,      content: 'ticket price for paris ?'},
  ChatCompletionMessage(role: assistant, content=None, tool_calls=[get_ticket_price Paris]),
  {role: tool,      content: 'The price of a ticket to Paris is $899', tool_call_id: '...'}
]
```

Read it as:

| # | Role | Meaning |
|---|------|---------|
| 1 | `system` | How to behave |
| 2 | `user` | The question |
| 3 | `assistant` + `tool_calls` | Model asked to run the tool (`content=None`) |
| 4 | `tool` | Your Python returned the price fact |

At this moment you **have the price**, but you still do **not** have the final chat sentence from the assistant.

#### Second LLM call writes the Gradio answer

```python
response = openai.chat.completions.create(model=MODEL_NAME, messages=messages)
```

Real print:

```text
----------RESPONSE FUNCTION RUNNING----------------------
Choice(
  finish_reason='stop',          # done — no more tools
  message=ChatCompletionMessage(
    content='The ticket price for Paris is $899.',
    role='assistant',
    tool_calls=None
  )
)
```

Compare the two calls:

| Call | `finish_reason` | `content` | Meaning |
|------|-----------------|-----------|---------|
| #1 | `tool_calls` | `None` | Please run the tool |
| #2 | `stop` | `The ticket price for Paris is $899.` | Final user-facing answer |

So:

- tool message = raw fact  
- second `create(...)` = turn fact into the chat reply  
- Gradio shows that `content`

### If user asks something else

Example: `What is FlightAI?`  
Usually `finish_reason` is normal (not `tool_calls`), so the `if` block is skipped and you return the first reply directly.

---



## Two LLM calls vs one


| Situation               | How many `create(...)` calls?        |
| ----------------------- | ------------------------------------ |
| Normal chat question    | **1**                                |
| Needs ticket price tool | **2** (ask tool → then final answer) |


The `for` / history building still does **not** call the LLM.  
Only `openai.chat.completions.create(...)` does.

---



## File map (quick)


| Piece in file                        | Job                                             |
| ------------------------------------ | ----------------------------------------------- |
| `ticket_prices` / `get_ticket_price` | Real data + real Python tool                    |
| `get_text`                           | Gradio 6 content cleanup                        |
| `price_function`                     | Schema describing the tool to the LLM           |
| `tools`                              | List passed into the API                        |
| `handle_tool_call`                   | Execute tool + build tool-role reply            |
| `system_message`                     | Airline assistant style                         |
| `chat`                               | Orchestrates history + tool loop + final answer |
| `gr.ChatInterface(...).launch()`     | Browser UI                                      |


---

