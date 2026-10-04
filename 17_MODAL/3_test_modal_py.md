# `TEST_MODAL.py` — line by line

Companion to [`TEST_MODAL.py`](TEST_MODAL.py). Defines the app: [`2_hello_py.md`](2_hello_py.md) · [`hello.py`](hello.py).

This script is a **smoke test**: load Modal credentials, import `hello`, call **`hello.local()`** then **`hello.remote()`**, and print both replies so you can see local vs cloud behavior.

---

## Which file is the “main” program?

| File | Role | Think of it as… |
|------|------|------------------|
| [`hello.py`](hello.py) | **Defines** the Modal app and `hello()` | A **module** / recipe (reusable building block) |
| [`TEST_MODAL.py`](TEST_MODAL.py) | **Runs** the test: imports `hello`, calls `.local()` / `.remote()` | The **entry point** when you `python TEST_MODAL.py` |

So:

- **`hello.py` is not “less important”** — it holds the real Modal setup (`App`, `Image`, `@app.function`). Without it, there is nothing to call.
- **`TEST_MODAL.py is the main program for running this demo`** — it is the script you execute; it **uses** `hello.py` like an import.

```text
hello.py          →  defines app + hello()
TEST_MODAL.py     →  main: load .env, from hello import …, run local/remote
```

Later, a notebook or agent might do the same as `TEST_MODAL.py` (`from hello import app, hello`) without using `TEST_MODAL.py` at all. The **definition** stays in `hello.py`; whatever file calls `.remote()` is the “runner” for that moment.

---

## Security warning (read before pushing to GitHub)

Lines 9–10 **print your Modal token ID and secret**. That is useful for debugging **once**, but:

- Never commit real tokens in code or screenshots.  
- Remove or comment out those `print` lines before sharing the repo publicly.  
- Keep tokens in **`.env`** only (gitignored).

---

## Full source (reference)

```python
# Just one import to start with!!
#pip install modal
import modal
from dotenv import load_dotenv
load_dotenv(override=True)
import os

print(os.environ["MODAL_TOKEN_ID"])
print(os.environ["MODAL_TOKEN_SECRET"])

from hello import app, hello

with app.run():
    reply=hello.local()

print (reply)

with app.run():
    reply=hello.remote()

print (reply)
```

---

## Line by line

### Comments and Modal import

| Line | Code | Explanation |
|------|------|-------------|
| 1–2 | Comments | Reminder that you need `pip install modal` in the **same** env as this script. |
| 3 | `import modal` | Loads Modal client libraries (used indirectly when `app.run()` talks to Modal’s API). |
| 4 | `from dotenv import load_dotenv` | Reads a **`.env`** file into environment variables. |
| 5 | `load_dotenv(override=True)` | Load `.env` from the current working directory. **`override=True`** — values in the file replace existing env vars. Run this **before** reading `MODAL_TOKEN_*`. |
| 6 | `import os` | Access environment variables via `os.environ`. |

### Credentials (debug only)

| Line | Code | Explanation |
|------|------|-------------|
| 9 | `print(os.environ["MODAL_TOKEN_ID"])` | Prints token id (`ak-...`). **`KeyError`** if missing from `.env`. |
| 10 | `print(os.environ["MODAL_TOKEN_SECRET"])` | Prints secret (`as-...`). **Do not share** these values. |

**`.env` example** (repo root, not committed):

```bash
MODAL_TOKEN_ID=ak-...
MODAL_TOKEN_SECRET=as-...
```

Modal uses these to authenticate when you call `.remote()`.

### Import the app and run locally

| Line | Code | Explanation |
|------|------|-------------|
| 12 | `from hello import app, hello` | Import the **`App`** instance and the **`hello`** function from [`hello.py`](hello.py). Python must find `hello.py` on the path — run from folder `17_MODAL`. |
| 14–15 | `with app.run():` / `reply=hello.local()` | **`app.run()`** — Modal client context for this session. **`hello.local()`** — run `hello()` **on your machine** (no Modal container). Still executes the function body (including `requests.get`). |
| 17 | `print (reply)` | Show the local result string. |

### Run on Modal cloud

| Line | Code | Explanation |
|------|------|-------------|
| 19–20 | `with app.run():` / `reply=hello.remote()` | **`hello.remote()`** — Modal schedules the function on their infrastructure using the `image` from `hello.py`. Network call goes out from **their** IP → ipinfo often shows a different location. |
| 22 | `print (reply)` | Show the cloud result string. |

**Full explanation** of `def hello() -> str`, `.local()`, and `.remote()`: [`2_hello_py.md`](2_hello_py.md#what-def-hello---str-means) and [deep dive](2_hello_py.md#hellolocal-vs-helloremote-deep-dive).

---

## Why two `with app.run():` blocks?

Each block is a separate **run**. For a tiny script this is fine. In larger code you can use **one** block:

```python
with app.run():
    local_reply = hello.local()
    remote_reply = hello.remote()
```

Both styles work; the file uses two blocks to mirror “try local, then try remote” step by step.

---

## Expected output pattern

```text
ak-...                    # remove these prints in shared repos
as-...
Hello from <your city>, <region>, <country>!!
Hello from <cloud city>, <region>, <country>!!
```

If `.remote()` fails with auth errors, fix tokens (Modal dashboard → API Tokens) and rerun after `load_dotenv`.

---

## How to run

```bash
cd /path/to/AI_LEARNING/AI_LEARNING/17_MODAL
conda activate my-proj   # or your env with modal installed
python TEST_MODAL.py
```

---

## Quick recap

1. **`load_dotenv`** — load `MODAL_TOKEN_ID` / `MODAL_TOKEN_SECRET`.  
2. **`from hello import app, hello`** — reuse the Modal app definition.  
3. **`hello.local()`** — same code, **your** machine.  
4. **`hello.remote()`** — same code, **Modal** container.  
5. **Don’t print secrets** in a public portfolio — delete lines 9–10 when done debugging.
