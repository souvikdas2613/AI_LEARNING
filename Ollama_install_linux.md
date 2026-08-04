# Ollama Install & Run on Linux

Guide for understanding **what Ollama is**, **why you’d install it**, then how to install / serve / pull / run models on Linux.

Includes **real outputs from this laptop** (WSL2) captured while writing these notes.

Pair with: [OpenAI API vs ChatGPT](OpenAI_API_vs_ChatGPT_subscription.md) · hands-on script [`Test_ollama_with_OPENAI.py`](1_PRACTICE_ON_OLLAMA_and_OPENAI/Test_ollama_with_OPENAI.py)

---

## 1) What is Ollama?

[Ollama](https://ollama.com/) is a **local LLM runner** for your machine.

In plain terms:

- It downloads open-weight models (e.g. Llama, Qwen, Mistral) onto your disk
- It runs them on **your** CPU/GPU — not on OpenAI’s servers
- It gives you a simple CLI (`ollama run …`) **and** a local HTTP API (default `http://localhost:11434`)

So Ollama is not “another ChatGPT website.” It is more like a **small model server + app** that lives on your laptop.

Typical pieces:

| Piece | Role |
|-------|------|
| `ollama` CLI | Install models, chat in terminal, check status |
| `ollama serve` | Background API server on port `11434` |
| Model files under `~/.ollama/` | The actual weights you pulled |
| OpenAI-compatible `/v1` API | Lets Python’s `openai` package talk to local models |

***You can chat in the terminal, or call the same model from Python — both go through Ollama.***

---

## 2) Why use and install Ollama?

### Why people use it

| Reason | What it means for you |
|--------|------------------------|
| **No API bill for inference** | Once the model is on disk, asking questions does not charge OpenAI tokens |
| **Works offline** (after pull) | Great for travel, demos, or flaky internet |
| **Private by default** | Prompts stay on your machine (unless you configure something else) |
| **Fast iteration for learning** | Same chat/API pattern as cloud, without burning credits while practicing |
| **Many free models** | Pick small models for weak laptops, bigger ones if you have GPU/RAM |
| **Plays nice with the `openai` package** | Change `base_url` → reuse the same Python style as cloud scripts |

### Why install it for *this* learning folder

Your cloud script talks to OpenAI. Your Ollama script talks to **localhost**. Installing Ollama lets you:

1. Learn LLM coding **without** spending API money every experiment
2. Compare cloud vs local quality/speed with almost the same Python structure
3. Understand servers, ports, and “model must be pulled first” — skills that transfer to real apps

When cloud still wins: strongest models, no local hardware pain, zero setup beyond an API key.  
When Ollama wins: practice, privacy, offline, cost control.

### What you need to know before installing

- Disk space: models are large (hundreds of MB to many GB)
- RAM/CPU: small tags like `1.5b` are friendlier on laptops; big models can be slow
- You must **pull** a model before you can run or call it from Python
- The server must be **running** (`ollama serve` or the desktop app) for API calls

---

## Official references

- Home: [https://ollama.com](https://ollama.com)
- Download / install: [https://ollama.com/download](https://ollama.com/download)
- Linux install script docs: [https://github.com/ollama/ollama/blob/main/docs/linux.md](https://github.com/ollama/ollama/blob/main/docs/linux.md)
- Models library: [https://ollama.com/library](https://ollama.com/library)

---

## 3) Install Ollama on Linux

### Quick install (recommended)

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Same command again (as you noted):

```bash
$ curl -fsSL https://ollama.com/install.sh | sh
```

Or follow the **manual** steps in the official Linux doc:

[ollama/docs/linux.md on GitHub](https://github.com/ollama/ollama/blob/main/docs/linux.md)

After install, the `ollama` binary is usually at:

```text
/usr/local/bin/ollama
```

### From this laptop (already installed)

```text
which ollama
/usr/local/bin/ollama

ollama --version
ollama version is 0.24.0

ls -la /usr/local/bin/ollama
-rwxr-xr-x 1 root root 44943968 May 15 03:11 /usr/local/bin/ollama
```

Machine context:

```text
uname -a
Linux C-PF33FDKQ 6.6.114.1-microsoft-standard-WSL2 ... x86_64 GNU/Linux
```

So on this machine Ollama is running under **WSL2 Linux**.

Models are stored under:

```text
~/.ollama/models
```

Example listing from this laptop:

```text
~/.ollama/models/
  blobs/
  manifests/
```

---

## 4) Start the Ollama server

Foreground (terminal stays busy):

```bash
ollama serve
```

Background (terminal free for other commands):

```bash
ollama serve &
```

### Notes

- If you see `bind: address already in use` on port `11434`, Ollama is **already running** — that is fine.
- Default API URL: `http://localhost:11434`

### From this laptop

Server process already running:

```text
ps aux | grep ollama
soudas   2753  ...  ollama serve
soudas   2874  ...  ollama run qwen2.5:1.5b
```

---

## 5) Check that Ollama is up

```bash
curl http://localhost:11434
```

### From this laptop

```text
curl http://localhost:11434
Ollama is running
```

---

## 6) List installed models

```bash
ollama list
```

### From this laptop

```text
NAME            ID              SIZE      MODIFIED
qwen2.5:1.5b    65ec06548149    986 MB    2 hours ago
```

Currently this machine has **`qwen2.5:1.5b`** (used by [`Test_ollama_with_OPENAI.py`](1_PRACTICE_ON_OLLAMA_and_OPENAI/Test_ollama_with_OPENAI.py)), not `llama3` yet.

---

## 7) See Ollama-related processes

```bash
ps aux | grep ollama
```

Useful to confirm:

- `ollama serve` is alive
- any interactive `ollama run ...` sessions

### From this laptop (example)

```text
soudas   2753  ...  ollama serve
soudas   2874  ...  ollama run qwen2.5:1.5b
```

---

## 8) Install / pull a model (example: LLaMA 3)

Pull downloads the model weights into `~/.ollama`:

```bash
ollama pull llama3
```

Other useful pulls (examples):

```bash
ollama pull qwen2.5:1.5b   # already on this laptop
ollama pull llama3
ollama pull llama3.2
```

After pull, confirm:

```bash
ollama list
```

---

## 9) Run a model (interactive chat)

```bash
ollama run llama3
```

This opens a chat prompt in the terminal. Type questions; exit with `/bye` or Ctrl+D (depending on version/UI).

On this laptop you can also run the model you already have:

```bash
ollama run qwen2.5:1.5b
```

### Important: `ollama run` is optional for Python

`ollama run` is only for **direct interactive chat** in the terminal (you type, it replies).

If you already have:

1. **Model pulled** — `ollama pull …` then `ollama list` shows it  
2. **Server running** — `ollama serve` (or Ollama already up; `curl http://localhost:11434` works)

…then you do **not** need `ollama run` to test from Python.

Your Python script talks to the **same local API** (`http://localhost:11434`). Ollama loads the model when the API request arrives and answers in your script’s output.

| Goal | Need `ollama run`? |
|------|--------------------|
| Chat yourself in the terminal | **Yes** |
| Run `Test_ollama_with_OPENAI.py` (or any API client) | **No** — serve + pulled model is enough |

Think of it like this:

- `ollama serve` = the restaurant kitchen is open  
- `ollama pull` / `ollama list` = the dish is on the menu  
- `ollama run` = you sit at the counter and order by hand  
- Python script = an app places the same order via the kitchen’s API — no counter seat needed  

---

## 10) See currently loaded / running models

```bash
ollama ps
```

Shows models loaded in memory (actively serving), separate from `ollama list` (downloaded models).

### From this laptop (at capture time)

```text
NAME    ID    SIZE    PROCESSOR    CONTEXT    UNTIL
```

(Empty table = no model currently loaded in memory right then. Downloaded models can still show in `ollama list`.)

---

## Quick command cheat sheet

| Goal | Command |
|------|---------|
| Install on Linux | `curl -fsSL https://ollama.com/install.sh \| sh` |
| Start server | `ollama serve` or `ollama serve &` |
| Health check | `curl http://localhost:11434` |
| List downloaded models | `ollama list` |
| OS processes | `ps aux \| grep ollama` |
| Download LLaMA 3 | `ollama pull llama3` |
| Chat with model (interactive) | `ollama run llama3` — optional if you only use Python |
| Call model from Python | Server up + model in `ollama list` (no `ollama run`) |
| Loaded models | `ollama ps` |

---

## How this connects to your Python learning files

Your script [`1_PRACTICE_ON_OLLAMA_and_OPENAI/Test_ollama_with_OPENAI.py`](1_PRACTICE_ON_OLLAMA_and_OPENAI/Test_ollama_with_OPENAI.py) talks to the same local server:

```python
openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
```

Requirements for that script:

1. `ollama serve` (or Ollama already running)
2. Model pulled (this laptop uses `qwen2.5:1.5b`) — confirm with `ollama list`
3. Conda env
4. **`ollama run` is not required** — that is only for interactive terminal chat

```bash
source ~/miniforge3/bin/activate
conda activate my-proj
cd /home/soudas/PERSONAL/AI_LEARNING/AI_LEARNING
python 1_PRACTICE_ON_OLLAMA_and_OPENAI/Test_ollama_with_OPENAI.py
```

More detail: [`Test_ollama_with_OPENAI.md`](1_PRACTICE_ON_OLLAMA_and_OPENAI/Test_ollama_with_OPENAI.md)

---

## Troubleshooting

| Symptom | Meaning / fix |
|---------|----------------|
| `curl` connection refused | Start with `ollama serve` (or `ollama serve &`) |
| `address already in use` on serve | Already running — ignore / use existing server |
| Model not found in Python / CLI | `ollama pull <model>` then `ollama list` |
| Slow answers | Small CPU laptop / large model — try smaller tags like `:1.5b` |

---

## Snapshot: this laptop (reference)

Captured for these notes:

| Item | Value |
|------|--------|
| OS | WSL2 Linux (`C-PF33FDKQ`) |
| Binary | `/usr/local/bin/ollama` |
| Version | `0.24.0` |
| API check | `Ollama is running` |
| Downloaded model | `qwen2.5:1.5b` (~986 MB) |
| Models dir | `~/.ollama/models` |
| Python test model name | `qwen2.5:1.5b` in [`Test_ollama_with_OPENAI.py`](1_PRACTICE_ON_OLLAMA_and_OPENAI/Test_ollama_with_OPENAI.py) |
