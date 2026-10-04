# `hello.py` — line by line

Companion to [`hello.py`](hello.py). Read first: [`1_what_is_modal.md`](1_what_is_modal.md).

This file defines a **minimal Modal app**: one function that runs in a cloud container and tells you **where** that container appears to be on the internet (city / region / country via [ipinfo.io](https://ipinfo.io)).

---

## Full source (reference)

```python
import modal
from modal import App, Image

# Setup

app = modal.App("hello")
image = Image.debian_slim().pip_install("requests")

# Hello!

@app.function(image=image)
def hello() -> str:
    import requests
    response = requests.get('https://ipinfo.io/json')
    data = response.json()
    city, region, country = data['city'], data['region'], data['country']
    return f"Hello from {city}, {region}, {country}!!"
```

---

## Line by line

### Imports

| Line | Code | Explanation |
|------|------|-------------|
| 1 | `import modal` | Loads the Modal SDK. Everything cloud-related goes through this package. |
| 2 | `from modal import App, Image` | **`App`** — groups your cloud functions under one name (`"hello"`). **`Image`** — defines the **container environment** (OS + pip packages). `App` is also available as `modal.App`; both styles work. |

### Setup block

| Line | Code | Explanation |
|------|------|-------------|
| 4 | `# Setup` | Comment only — separates “infrastructure” from the function body. |
| 6 | `app = modal.App("hello")` | Creates a Modal **application** object. The string **`"hello"`** is the **app name on Modal’s dashboard** — it is **not** the Python function you decorate next. See [App name vs function name](#app-name-vs-function-name-not-the-same-thing) below. |
| 7 | `image = Image.debian_slim().pip_install("requests")` | Builds a **container image**: slim Debian Linux, then installs **`requests`** for HTTP. Your laptop might already have `requests`; the **remote** container only gets what you list here. |

### The cloud function

| Line | Code | Explanation |
|------|------|-------------|
| 11 | `@app.function(image=image)` | **Decorator** — tells Modal this function can run in the cloud. [Why it is needed](#why-appfunction-decorator-is-needed). |
| 12 | `def hello() -> str:` | Defines function **`hello`**; **`-> str`** is a type hint: return value should be a string. [Details below](#what-def-hello---str-means). |
| 13 | `import requests` | Import **inside** the function so it runs in the container (where `requests` was installed on line 7). |
| 14 | `response = requests.get('https://ipinfo.io/json')` | HTTP GET to ipinfo — “where is **this** machine on the internet?” [Full breakdown](#requestsgethttpsipinfoiojson). |
| 15 | `data = response.json()` | Parse JSON body into a Python `dict`. |
| 16 | `city, region, country = data['city'], data['region'], data['country']` | Unpack three fields. If a key is missing, you get `KeyError` — fine for this demo. |
| 17 | `return f"Hello from {city}, {region}, {country}!!"` | String sent back to whoever called `.local()` or `.remote()`. |

---

## `requests.get('https://ipinfo.io/json')`

This line is how the demo proves **where the code is running** — your laptop vs Modal’s cloud.

### Breaking the line apart

```python
response = requests.get('https://ipinfo.io/json')
```

| Piece | Meaning |
|-------|---------|
| `requests` | Popular Python library for **HTTP** (talking to websites/APIs). Installed in the Modal `image` via `.pip_install("requests")`. |
| `.get(...)` | **HTTP GET** — “please **read** this URL” (no form body; like opening a link in a browser). |
| `'https://ipinfo.io/json'` | URL of a small **public API** that returns info about **your public IP address**. |
| `response` | Object holding status code, headers, and **response body** (the JSON text). |

Other common methods: `requests.post(url, json={...})` for sending data; not needed here.

### What is ipinfo.io?

[ipinfo.io](https://ipinfo.io) looks at the **IP address of whoever called it** and replies with rough **geolocation** and network metadata.

- When you run **`hello.local()`**, the request leaves **your home/office network** → ipinfo sees **your** public IP → city/region/country near you.
- When you run **`hello.remote()`**, the request leaves **Modal’s datacenter** → ipinfo sees **their** egress IP → often a different city/region.

So the message is not magic — it is **“where did this HTTP request come from on the internet?”**

### What is `/json`?

The same service can return HTML or JSON. **`/json`** means: respond with **JSON** (JavaScript Object Notation) — a text format Python can parse into a `dict`.

Example body (fields can vary; free tier may omit some):

```json
{
  "ip": "203.0.113.42",
  "city": "Ashburn",
  "region": "Virginia",
  "country": "US",
  "loc": "39.0438,-77.4874",
  "org": "AS12345 Example Cloud",
  "timezone": "America/New_York"
}
```

Your code only uses **`city`**, **`region`**, and **`country`**.

### Step-by-step with the next lines

```python
response = requests.get('https://ipinfo.io/json')
data = response.json()
city, region, country = data['city'], data['region'], data['country']
```

| Step | What happens |
|------|----------------|
| 1 | TCP/TLS connection to `ipinfo.io` from the machine running `hello()` |
| 2 | Server logs **source IP** of the connection |
| 3 | Server sends JSON text in the HTTP body |
| 4 | `response.json()` converts that text → Python `dict` |
| 5 | You read keys like a dictionary: `data['city']` |

### Why use this in a Modal tutorial?

| Goal | How ipinfo helps |
|------|------------------|
| Show `.local()` vs `.remote()` | Same code, **different location strings** |
| Minimal dependencies | One URL, no API key for basic demo |
| Real network I/O | Proves the **container** can reach the internet |

For production you would not rely on ipinfo for security; it is a **teaching trick** to make cloud vs local visible.

### Things that can go wrong (good to know)

| Issue | Symptom |
|-------|---------|
| No internet in container | `requests` raises connection error |
| Rate limits on ipinfo | Slow or blocked after many calls |
| VPN on your laptop | `.local()` may show VPN exit city, not your physical city |
| Missing JSON key | `KeyError` on `data['city']` |

### Mental model

```text
hello()  →  GET https://ipinfo.io/json
                ↓
         “Who is asking?” (public IP)
                ↓
         JSON { city, region, country, ... }
                ↓
         f"Hello from {city}, {region}, {country}!!"
```

---

## Why `@app.function` decorator is needed

In plain Python you can write:

```python
def hello():
    return "Hi"
```

That runs **only on your machine**. Modal would not know:

- that this function is allowed to run in **their** cloud  
- which **container image** to use (`image=image`)  
- whether to attach a **GPU**, **secrets**, or **region**  
- how to expose **`.remote()`** and **`.local()`**

The **decorator** is Modal’s registration step:

```python
@app.function(image=image)
def hello() -> str:
    ...
```

| Without `@app.function` | With `@app.function` |
|-------------------------|----------------------|
| Normal `def` | Function is **registered** on `app` |
| No `.remote()` | You get `hello.remote()` → run in Modal container |
| You manage env yourself | Modal uses `image` (OS + `pip install ...`) |
| Not on Modal dashboard | Shows up as part of app `"hello"` |

Think of it like labeling a box for shipping:

```text
def hello()           →  recipe written on paper
@app.function(...)  →  “this recipe may be cooked in Modal’s kitchen, with THIS image”
hello.remote()        →  actually send the order to that kitchen
```

**It is not a Python language rule** — it is **Modal’s API**. Other frameworks use similar patterns (e.g. Flask `@app.route`, AWS Lambda handlers). You need *some* hook so the platform knows which functions to deploy and how to run them.

**Could you skip it?** Only if you never use Modal cloud — then you do not need Modal at all. For this project, **no decorator ⇒ no `.remote()` ⇒ no cloud demo.**

---

## App name vs function name (not the same thing)

A common question: *“I created `App("hello")` — is that the same `hello` I decorate on the next line?”*

**No.** They are three separate ideas that **happen to share the word hello** in this file:

```text
modal.App("hello")     →  name of the Modal *project* (dashboard / logs)
        app            →  Python variable holding that App instance
@app.function          →  “register the next function with this app”
def hello():           →  Python function name you import and call
```

| Piece | What it is | You change it to… |
|-------|------------|-------------------|
| `modal.App("hello")` | **Modal app label** (cloud UI) | Any string, e.g. `"price-bot"` |
| `app` | Variable for the `App` object | Any name, e.g. `my_app` — then use `@my_app.function` |
| `def hello()` | **Your function** in Python | Any name, e.g. `def greet()` — then call `greet.remote()` |

The **decorator** ties the function to **`app`**, not to the string `"hello"` inside `App("hello")`.

```python
app = modal.App("my-first-modal-app")   # dashboard name (unrelated to def name)

@app.function(image=image)
def greet() -> str:
    return "Hi"

# TEST_MODAL.py would do:
# from hello import app, greet
# greet.remote()
```

In **this** repo file:

```python
app = modal.App("hello")      # Modal project name = "hello"

@app.function(image=image)    # use variable app
def hello() -> str:           # Python callable name = hello
```

So: **next line after `App(...)` is not “creating hello as the app.”** You create **`app`**, then **`@app.function`** registers whatever function you define below (here, also named `hello` by choice).

---

## What `def hello() -> str:` means

This line is **normal Python**, plus a small **type hint**. Modal does not change the syntax.

```python
def hello() -> str:
```

| Part | Meaning |
|------|---------|
| `def` | Start defining a function |
| `hello` | Function name — you import it as `from hello import hello` and call `hello.local()` |
| `()` | No parameters — callers do not pass arguments |
| `-> str` | **Return type hint**: “this function is intended to return a `str`” (text) |
| `:` | Start of the indented function body |

**Type hints (`-> str`)** are optional in Python. They do **not** force the type at runtime by themselves (unless you use a checker like mypy). They help **you and your IDE** know what comes back.

```python
reply: str = hello.remote()   # IDE knows reply is probably a string
```

Equivalent without the hint:

```python
def hello():
    ...
    return "Hello from ..."
```

After `@app.function`, `hello` is still a Python function, but Modal wraps it so you can also call:

- `hello()` — plain call (runs locally like any function, if you call it directly)
- `hello.local()` — explicit “run this function **here**”
- `hello.remote()` — “run this function **on Modal**”

In [`TEST_MODAL.py`](TEST_MODAL.py) you use `.local()` and `.remote()`, not bare `hello()`.

---

## `hello.local()` vs `hello.remote()` (deep dive)

Once a function is decorated with `@app.function`, Modal gives you **two ways to invoke the same code**:

```python
with app.run():
    a = hello.local()
    b = hello.remote()
```

Both run the **same** `def hello()` body (ipinfo + return string). The difference is **where that code executes**.

### Comparison

| | `hello.local()` | `hello.remote()` |
|---|-----------------|------------------|
| **Runs on** | Your computer (same process as `TEST_MODAL.py`) | Modal’s server in a **container** built from `image` |
| **Network** | Your home/office IP → ipinfo | Modal datacenter IP → ipinfo |
| **Uses `image=`?** | No — uses your local Python env | Yes — Debian + `pip install requests` from `hello.py` |
| **Needs Modal tokens?** | No (for `.local()` alone) | Yes — client talks to Modal API |
| **Speed** | Instant (no container startup) | Slower first time (build/pull image, start container) |
| **Typical use** | Debug logic before paying for cloud | Real GPU/scale work, production path |

### Flow diagrams

**`.local()`**

```text
TEST_MODAL.py on your laptop
        │
        ▼
hello.local()  ──►  def hello() runs HERE
        │              requests.get(ipinfo) from YOUR network
        ▼
   return str  ──►  print on your laptop
```

**`.remote()`**

```text
TEST_MODAL.py on your laptop
        │
        ▼
hello.remote()  ──►  Modal API (auth with MODAL_TOKEN_*)
        │
        ▼
   Container starts (image: debian + requests)
        │
        ▼
   def hello() runs INSIDE container
        │              requests.get(ipinfo) from MODAL network
        ▼
   return str  ──►  sent back to your laptop  ──►  print
```

### Why both exist?

- **`.local()`** — “Does my function code make sense?” without spinning up cloud infra.
- **`.remote()`** — “Run it where I configured it (image, GPU, secrets, region).”

For a tiny `requests` demo, local vs remote mainly changes **location/IP**. For a **GPU model**, `.remote()` is what actually gives you a GPU; `.local()` would only use your laptop’s hardware.

### `with app.run():` — why it wraps both calls

`app.run()` starts a Modal **client session**: connects to your account, tracks runs, cleans up. You need it for **`.remote()`**; it is good practice to wrap **`.local()`** in the same block when mixing both in one script so one session handles everything.

### What you do **not** write

You do **not** call `hello()` like a normal function in the test script for the Modal pattern:

```python
hello()   # runs locally, but bypasses Modal’s explicit local/remote API
```

The course/portfolio style is:

```python
hello.local()
hello.remote()
```

so it is obvious **where** each run happened.

---

## How you run it (not in this file)

This file **only defines** the app — it is **not** the main program you execute by itself for the demo.

| | `hello.py` | [`TEST_MODAL.py`](TEST_MODAL.py) |
|---|------------|----------------------------------|
| Role | **Define** `app` + `hello()` | **Run** smoke test (`python TEST_MODAL.py`) |
| Contains `if __name__` / top-level calls? | No | Yes (prints, `app.run()`, `.local()` / `.remote()`) |

You run the flow from another script or notebook, for example [`TEST_MODAL.py`](TEST_MODAL.py) (the usual **entry point** for this folder):

```python
from hello import app, hello

with app.run():
    print(hello.local())   # runs on YOUR machine (still uses your network IP)
    print(hello.remote())  # runs on MODAL (different city/region often)
```

| Call | Where code runs | Typical message |
|------|-----------------|-----------------|
| `hello.local()` | Your CPU, your network | “Hello from *your* area…” |
| `hello.remote()` | Modal container | “Hello from *datacenter region*…” |

More detail: [`.local()` vs `.remote()` (deep dive)](#hellolocal-vs-helloremote-deep-dive).

`with app.run():` opens a Modal **run context** so the client can schedule `.remote()` calls and shut down cleanly.

---

## Mental model

```text
hello.py
  app + image  →  recipe for a container
  @app.function →  hello() can execute in that container
  .remote()     →  Modal builds/uses image, runs hello(), returns string
```

---

## Quick recap

1. **`modal.App("…")`** — **dashboard** name for the Modal project (independent of `def` name).  
2. **`app`** — variable; **`@app.function`** registers functions on that app.  
3. **`Image.debian_slim().pip_install(...)`** — what’s installed in the cloud box.  
4. **`def hello()`** — Python name for `hello.local()` / `hello.remote()`.  
5. **`hello.remote()`** — proof the code ran **in the cloud**, not only on your laptop.
