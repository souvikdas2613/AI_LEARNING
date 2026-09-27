# `python_code_to_CPP_code_Conversion.py` — every step explained

Line-by-line walkthrough of [`python_code_to_CPP_code_Conversion.py`](./python_code_to_CPP_code_Conversion.py).

Course reference: Udemy `llm_engineering/week4/day4.ipynb` (this version drops Gradio, streaming, and auto-`clang++`).

Prompting pattern (system vs user): [`user_prompt_system_prompt.md`](../2_USER_PROMPT_SYSTEM_PROMPT/user_prompt_system_prompt.md)

---

## What this script does (one sentence)

Loads `OPENAI_API_KEY` and `MODEL_NAME` from `.env`, reads and runs `test_python_code.py`, then calls that model to rewrite the Python as fast C++, prints the result, and saves `Converted_CPP_Code.cpp`.

---

## Big picture flow

```text
.env (OPENAI_API_KEY, MODEL_NAME)  →  OpenAI client  →  read test_python_code.py
                                │
                    ┌───────────┴───────────┐
                    │                       │
              exec(python)            optimize_gpt(python)
           (baseline output)         system + user messages
                                            │
                                            ▼
                              Converted_CPP_Code.cpp
```

---

## How to run

From the directory that contains `python_code_to_CPP_code_Conversion.py` and `test_python_code.py`:

```bash
python3 python_code_to_CPP_code_Conversion.py
```

- Paths like `test_python_code.py` and `Converted_CPP_Code.cpp` are **relative to your current working directory** when you run the command.
- `.env` can live in this folder or a parent; `load_dotenv()` uses `find_dotenv()` and searches upward until it finds a `.env` file.

### Required `.env` keys

| Key | Used where | Notes |
|-----|------------|--------|
| `OPENAI_API_KEY` | `OpenAI()` | Required for authentication |
| `MODEL_NAME` | `optimize_gpt` → `model=MODEL_NAME` | **Not defined in the `.py` file.** Example: `MODEL_NAME=gpt-4.1-nano` |

```env
OPENAI_API_KEY=your-key-here
MODEL_NAME=gpt-4.1-nano
```

If `MODEL_NAME` is missing, `MODEL_NAME` is `None` and the API call will fail — always set both keys in `.env`.

---

## Execution order (what runs when)

Top-to-bottom in the file:

1. Load `.env` → read `OPENAI_API_KEY`, `MODEL_NAME`
2. Create `openai = OpenAI()`
3. Print `system_message`
4. Define functions (`user_prompt_for`, `messages_for`, `write_output`, `optimize_gpt`) — not called yet
5. Read `test_python_code.py` → print source
6. `exec(...)` → run Python baseline
7. `optimize_gpt(...)` → API call using **`MODEL_NAME` from `.env`** → print C++ → write `Converted_CPP_Code.cpp`

---

## Step 1 — Imports

```python
import os
from dotenv import load_dotenv
from openai import OpenAI
```

| Import | Why |
|--------|-----|
| `os` | `os.getenv('OPENAI_API_KEY')` and `os.getenv('MODEL_NAME')` |
| `load_dotenv` | Load secrets from `.env` into the environment |
| `OpenAI` | Official SDK for Chat Completions |

Nothing calls the API yet — only libraries load.

---

## Step 2 — Load environment

```python
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME')
```

### `load_dotenv(override=True)`

- Searches for `.env` starting in the cwd, then parent folders.
- Puts `OPENAI_API_KEY=...` and `MODEL_NAME=...` into environment variables.
- `override=True`: if a variable was already set in your shell, the `.env` value wins.

### `openai_api_key` and `MODEL_NAME`

| Variable | Purpose |
|----------|---------|
| `openai_api_key` | Loaded from env; **not used later in this script** (no `if not openai_api_key` check). `OpenAI()` still picks up `OPENAI_API_KEY` from the environment after `load_dotenv`. |
| `MODEL_NAME` | **Only** source of the model id: must be set in `.env` (e.g. `gpt-4.1-nano`). Used once: `model=MODEL_NAME` in `optimize_gpt`. |

---

## Step 3 — OpenAI client

```python
# initialize OpenAI client
openai = OpenAI()
```

Creates the client using `OPENAI_API_KEY` from the environment (after Step 2). **No model name here** — the model comes only from `MODEL_NAME` in Step 2 when `optimize_gpt` runs.

---

## Step 4 — System message

```python
system_message = "You are an assistant that reimplements Python code in high performance C++ for an M1 Mac. Respond only with C++ code; use comments sparingly and do not provide any explanation other than occasional comments. The C++ response needs to produce an identical output in the fastest possible time."

print ("system prompt messge :\n")
print (system_message)
```

### What `system_message` is

This is the **system prompt** — standing rules for the whole chat:

- Role: port Python → **fast C++**
- Target: **M1 Mac** (from the course; on WSL/Linux the model may still emit portable C++)
- Output: **code only**, almost no prose
- Goal: **same output** as Python, **minimum runtime**

### Why print it?

So when you run the script you **see** what was sent as `role: "system"` before the API call. Same learning idea as printing messages in `user_prompt_system_prompt.py`.

---

## Step 5 — `user_prompt_for(python)`

```python
def user_prompt_for(python):
    user_prompt = "Rewrite this Python code in C++ with the fastest possible implementation that produces identical output in the least time. Respond only with C++ code; do not explain your work other than a few comments. Pay attention to number types to ensure no int overflows. Remember to #include all necessary C++ packages such as iomanip.\n\n"
    user_prompt += python
    return user_prompt
```

| Part | Meaning |
|------|---------|
| First long string | **User prompt** instructions: speed, no essay, watch integer overflow, include headers (`iomanip`, etc.) |
| `user_prompt += python` | Append the **entire** Python source (from `test_python_code.py`) so the model knows what to port |
| `return user_prompt` | One string → becomes `role: "user"` content |

**System vs user:** system = who the model is; user = this job + the code body.

---

## Step 6 — `messages_for(python)`

```python
def messages_for(python):
    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt_for(python)}
    ]
```

Builds the **messages array** OpenAI expects:

1. `system` — `system_message`
2. `user` — result of `user_prompt_for(python)`

Every call to `optimize_gpt` uses this shape. No assistant/history turns — single shot.

---

## Step 7 — `write_output(cpp)`

```python
def write_output(cpp):
    code = cpp.replace("```cpp","\n").replace("```","\n")
    with open("Converted_CPP_Code.cpp", "w") as f:
        f.write(code)
```

| Line | Meaning |
|------|---------|
| `.replace("```cpp", ...)` | Models often wrap code in markdown fences; strip opening fence |
| `.replace("```", ...)` | Strip closing (or stray) fences |
| `open("Converted_CPP_Code.cpp", "w")` | Overwrite output file in the **current working directory** each run |

If the model returns pure C++ with no fences, `replace` does little harm.

---

## Step 8 — `optimize_gpt(python)`

```python
def optimize_gpt(python):
    """Ask the model once; print and save the full C++ reply."""
    print("\n\nConverted Python to C++ Code Below :\n\n\n")
    response = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=messages_for(python),
    )
    reply = (response.choices[0].message.content or "").strip()
    print(reply)
    write_output(reply)
```

Line by line:

| Line | What happens |
|------|----------------|
| `print(...)` | Banner before C++ output |
| `chat.completions.create(...)` | **One** HTTP API call; model generates full answer |
| `model=MODEL_NAME` | Value from `.env` (e.g. `gpt-4.1-nano`) — not set in the `.py` file |
| `messages=messages_for(python)` | System + user prompts from Steps 4–6 |
| `response.choices[0].message.content` | First completion’s text (the C++ source) |
| `or ""` | If content is missing, use empty string |
| `.strip()` | Trim leading/trailing whitespace |
| `print(reply)` | Show C++ in terminal |
| `write_output(reply)` | Save to `Converted_CPP_Code.cpp` |

No streaming loop — wait for the full reply, then print once (simpler to read when learning).

---

## Step 9 — Read input Python file

```python
with open("test_python_code.py", "r") as f:
    test_python_code_file = f.read()
```

| Piece | Meaning |
|-------|---------|
| `"test_python_code.py"` | Fixed filename in this lab (edit that file to change input) |
| `.read()` | Whole file into one string — same string used for `exec` and for the LLM |

---

## Step 10 — Print source, then run Python

```python
print ("\n\nINPUT PYTHON FILE :  \n")
print(test_python_code_file)

print ("\n\nExecute INPUT PYTHON FILE :  \n")
exec(test_python_code_file)
```

| Block | Meaning |
|-------|---------|
| First `print` block | You see exactly what will be ported |
| `exec(test_python_code_file)` | Runs the Python **in this process** — any `print` in `test_python_code.py` goes to your terminal. Current sample uses `calculate(10, 4, 1)` (quick demo), not the course notebook’s huge iteration count. |

**Why run before LLM?** Baseline: you know what output the C++ must match.

**Caution:** `exec` runs arbitrary code — fine for your own `test_python_code.py`; never `exec` untrusted strings in production.

---

## Step 11 — Call the converter

```python
optimize_gpt(test_python_code_file)
```

Passes the **same** Python source string to the API. Model returns C++ → printed and saved.

Script ends here; no `if __name__ == "__main__"` guard — top-level lines run on import too (OK for a small learning script you only run as main).

---

## Files in this folder

| File | Role |
|------|------|
| `python_code_to_CPP_code_Conversion.py` | This script |
| `test_python_code.py` | Input Python |
| `Converted_CPP_Code.cpp` | Created/overwritten by `write_output` |

---

## Optional — compile C++ yourself

The script does **not** run `clang++`. After a good run:

```bash
clang++ -std=c++17 -O3 Converted_CPP_Code.cpp -o converted_main
./converted_main
```

Compare numbers to the Python `exec` output. Or paste into [Programiz online C++](https://www.programiz.com/cpp-programming/online-compiler/) (course suggestion).

---

## Things to experiment with

- Change `iterations` in `test_python_code.py` (small for demo vs large for speed tests)
- Tweak `system_message` (e.g. “optimize for Linux/WSL” instead of M1)
- Change `MODEL_NAME` in `.env` (e.g. `gpt-4.1-nano` vs a larger model) and compare quality / cost
- Add `if not openai_api_key or not MODEL_NAME: raise SystemExit("missing .env vars")` after Step 2

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| 401 / authentication | Check `OPENAI_API_KEY` in `.env` (parent folder is OK) |
| API error / bad `model` | Set `MODEL_NAME` in `.env` (e.g. `gpt-4.1-nano`). If unset, `model=None` is sent to the API. |
| `FileNotFoundError: test_python_code.py` | Run from the folder that contains that file |
| Pause before C++ appears | Normal — non-streaming waits for full completion |
| Bad or non-compiling C++ | Re-run or edit prompts / fix `Converted_CPP_Code.cpp` manually |
