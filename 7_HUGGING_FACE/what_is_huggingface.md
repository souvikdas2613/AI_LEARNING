# The Hugging Face Platform

Chapter notes for **Souvik’s** AI learning journey (folder `7_HUGGING_FACE`).

---

## Index

| # | Topic |
|---|--------|
| 1 | [Introduction](#1-introduction) |
| 2 | [Hugging Face Transformers](#2-hugging-face-transformers) |
| 3 | [Inference in Hugging Face](#3-inference-in-hugging-face) |
| 4 | [What “inference” means in practice](#4-what-inference-means-in-practice) |
| 5 | [Pipeline](#5-pipeline) |
| 5.1 | [What is a classifier?](#51-what-is-a-classifier) |
| — | [pipeline is NOT the classifier itself](#important-pipeline-is-not-the-classifier-itself) |
| — | Practice notebook: [`colab_pipelines_explained.ipynb`](./colab_pipelines_explained.ipynb) (run in Colab — pipelines + tokenizer/model) |
| — | Practice notebook: [`colab_tokenizers_explained.ipynb`](./colab_tokenizers_explained.ipynb) (run in Colab — AutoTokenizer) |
| 6 | [How to create a Hugging Face API token (`HF_TOKEN`)](#6-how-to-create-a-hugging-face-api-token-hf_token) |
| 7 | [Hugging Face API call](#7-hugging-face-api-call) |
| 7.1 | [Using huggingface_hub package](#71-using-huggingface_hub-package) |
| 7.2 | [Using OpenAI Python client](#72-using-openai-python-client) |

---

## 1. Introduction

Hugging Face is ubiquitous and widely used across the community.

Upon signing up at [huggingface.co](https://huggingface.co), you gain access to **three main categories**:

- **Models:** Over 800,000 open-source models capable of various tasks, many of which we will explore.
- **Datasets:** A treasure trove of over 200,000 datasets covering almost any problem domain.
- **Spaces:** A platform to write and deploy apps on Hugging Face cloud hardware, accessible to others as open-source projects.

Spaces apps are often built using **Gradio**, though Streamlit and other frameworks are also supported. Leaderboards, which are Gradio apps, evaluate and rank different LLMs, providing scorecards useful for comparison.

Hugging Face offers several libraries that form the foundation of many open-source projects:

- **Hub:** Allows logging in, downloading, and uploading models and datasets from the Hugging Face platform.
- **Datasets:** Provides immediate access to the extensive data repositories.
- **Transformers:** A central library wrapping LLMs based on the transformer architecture, supporting both PyTorch and TensorFlow backends. This library enables local execution of inference and training without relying on external APIs.

---

## 2. Hugging Face Transformers

There are **two modes** of interacting with Hugging Face code:

### High-level API (Pipelines)

Designed for standard, everyday inference tasks where you input data and get an output.

This interface is user-friendly and allows rapid development for tasks like text generation.

In Hugging Face, a **pipeline** is a high-level API that wraps around a model, tokenizer, and any necessary preprocessing/postprocessing logic so you can run inference with just a few lines of code — without worrying about all the low-level details.

### Low-level API

For deeper interaction, including:

- detailed tokenization  
- model selection  
- parameter tuning  
- training or fine-tuning models for specialized tasks  

---

## 3. Inference in Hugging Face

In Hugging Face, **inference** refers to the process of using a trained model to make predictions (as opposed to training a model).

---

## 4. What “inference” means in practice

- **Training** = teaching a model from data (adjusting weights).
- **Inference** = applying that trained model to new inputs (getting outputs).

Example:

- You train a language model on billions of tokens → that’s **training**.
- You then feed it `Translate 'hello' to French` and it outputs `bonjour` → that’s **inference**.

**Inference = using a trained model to generate predictions.**

In Hugging Face, this can mean:

- Running the model locally with `transformers`.
- Calling the Inference API for quick results.
- Deploying a managed inference endpoint for production use.

---

## 5. Pipeline

In Hugging Face, the **pipeline** is a high-level, easy-to-use API that lets you run inference with models in just a few lines of code — without worrying about tokenization, preprocessing, or model loading details.

Think of it as a **task-specific wrapper**: you tell it what you want to do (e.g., sentiment analysis, text generation, translation), and it automatically:

1. Downloads the right model + tokenizer (from Hugging Face Hub, if needed).
2. Preprocesses your input.
3. Runs inference.
4. Postprocesses the output into human-readable form.

Think of it as a ready-made shortcut:

- You say what task you want (`sentiment-analysis`, `text-generation`, `translation`, etc.)
- It downloads the default model for that task (or lets you choose one).
- It runs the tokenizer + model + postprocessing behind the scenes.

### Example

```python
from transformers import pipeline

classifier = pipeline("sentiment-analysis")
print(classifier("I love this!"))
```

#### Is `"sentiment-analysis"` another function, or just a string?

**Just a string** — not another function.

```python
classifier = pipeline("sentiment-analysis")
#                   ^^^^^^^^^^^^^^^^^^^^
#                   plain text = task name
```

`pipeline` is a **function**. Its first argument is a **task name as text**. Internally Hugging Face looks that string up and picks the right default model + tokenizer for that job.

| What you write | What it is |
|----------------|------------|
| `pipeline` | the function (imported from `transformers`) |
| `"sentiment-analysis"` | a **string** naming the task |
| `classifier` | the **object/tool** returned |
| `classifier("I love this!")` | later: another **string** = your sentence |

Same idea for other tasks — still strings:

```python
pipeline("summarization")
pipeline("translation")
pipeline("text-generation")
```

You can also pass a model id (also a string):

```python
pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
#        ^ task string              ^ model id string
```

```text
"sentiment-analysis"  →  build a sentiment tool
"summarization"       →  build a summarization tool
```

You are **naming the job**, not passing a function.

Example run output:

```text
No model was supplied, defaulted to distilbert/distilbert-base-uncased-finetuned-sst-2-english and revision 714eb0f
(https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english).
Using a pipeline without specifying a model name and revision in production is not recommended.
config.json: 100%|...| 629/629
model.safetensors: 100%|...| 268M/268M
tokenizer_config.json: 100%|...|
vocab.txt: ...
Device set to use cpu
[{'label': 'POSITIVE', 'score': 0.9998641014099121}]
```

So:

- if you don’t pass a model, pipeline picks a default  
- it downloads config + weights + tokenizer  
- then returns a readable result like `POSITIVE` with a score  

---

## 5.1 What is a classifier?

A **classifier** is a model whose job is to put the input into a **category / label** — not to write a long free answer.

```text
Input text  →  Classifier  →  Label (one of a fixed set)
"I love this!"              →  POSITIVE
"This was awful."           →  NEGATIVE
```

| | Classifier | Chat / generative model (e.g. Qwen Instruct) |
|--|------------|-----------------------------------------------|
| Output | A **label** from a fixed list | New **text** (sentences, answers) |
| Example | POSITIVE / NEGATIVE / SPAM / NOT_SPAM | “The capital of France is Paris.” |
| Pipeline demo | DistilBERT sentiment | — |
| Your API scripts | — | Qwen chat |

So **“sentiment classifier”** means: a model trained to **classify** text by sentiment (pick a label), not chat with you.

Two uses of the word in pipeline code:

| Word | Meaning |
|------|---------|
| `classifier = pipeline(...)` | Just a **variable name** for the pipeline tool |
| “classifier model” | The **kind of model** (label-picker), vs a chat LLM |

### Important: `pipeline` is NOT the classifier itself

This distinction is useful:

```python
classifier = pipeline("sentiment-analysis")
```

Here, `classifier` is the **pipeline object**.

Inside that pipeline is a **pretrained classification model**.

```text
pipeline
   │
   ├── tokenizer
   ├── pretrained model
   ├── preprocessing
   └── postprocessing
```

That’s why you can call it like a normal Python function:

```python
classifier("I love this!")
```

instead of manually handling tensors and model outputs.

That is why `pipeline("sentiment-analysis")` uses DistilBERT (a classifier), not Qwen Instruct (a chat LLM).

Same idea is also in the Colab notebook: [`colab_pipelines_explained.ipynb`](./colab_pipelines_explained.ipynb).

---

## 6. How to create a Hugging Face API token (`HF_TOKEN`)

This is the same *idea* as creating an OpenAI API key — just on Hugging Face.

| | **OpenAI** | **Hugging Face** |
|---|------------|------------------|
| Website | platform.openai.com | huggingface.co |
| Secret name in `.env` | `OPENAI_API_KEY` | `HF_TOKEN` |
| Used for | Call OpenAI models via API | Hub access, gated models, Inference / router API |
| Keep secret? | Yes | Yes |

### Steps (like OpenAI)

1. Create / log in to a Hugging Face account: [https://huggingface.co](https://huggingface.co)  
2. Open your account settings → **Access Tokens**  
   Direct-ish path: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)  
3. Click **Create new token**  
4. Give it a name (e.g. `souvik-laptop`)  
5. Choose access type:
   - **Read** is enough for many download / inference uses  
   - use stronger permissions only if you need write/upload  
6. Create the token and **copy it once** (you may not see the full value again)  
7. Put it in your `.env` (same place as your OpenAI key)

### Your `.env` style

```env
OPENAI_API_KEY=sk-proj-...
HF_TOKEN=XXXXXXXXXXXXXXXXXX
```

Example matching how you store it:

```env
HF_TOKEN="XXXXXXXXXXXXXXXXXX"
```

(Quotes are optional in many `.env` setups; either style is fine if `python-dotenv` loads it correctly.)

### Use it in Python (same pattern as OpenAI)

```python
import os
from dotenv import load_dotenv

load_dotenv(override=True)

hf_token = os.getenv("HF_TOKEN")
if hf_token:
    print("HF_TOKEN loaded")
else:
    print("HF_TOKEN missing — add it to .env")
```

Then pass it where needed, e.g.:

```python
api_key=os.environ["HF_TOKEN"]
```

### Colab note

On Colab, store the same value as a **Colab Secret** named `HF_TOKEN` (not in Google Drive).  
See [`8_GOOGLE_COLAB/what_is_google_colab.md`](../8_GOOGLE_COLAB/what_is_google_colab.md).

### Safety rules (same as OpenAI)

- Never commit `.env` to GitHub  
- Never paste the full token into shared notebooks  
- If a token leaks → revoke it on Hugging Face and create a new one  

---

## 7. Hugging Face API call

Besides local pipelines, you can call hosted models over the API.

Two common ways:

1. `huggingface_hub` package (`InferenceClient`)
2. OpenAI Python client pointed at Hugging Face’s router

---

### 7.1 Using `huggingface_hub` package

Using `InferenceClient` from `huggingface_hub` is the official way to call models hosted on Hugging Face. It’s much cleaner than using raw requests.

Here’s how you can set it up with `Qwen/Qwen2.5-7B-Instruct`:

```python
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv(override=True)

client = InferenceClient(
    provider="together",
    api_key=os.environ["HF_TOKEN"],
)

completion = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ],
)

print(completion.choices[0].message.content)
```

Example output:

```text
The capital of France is Paris.
```

#### What each import / line means

- `os` → lets you read environment variables (e.g., API keys).
- `InferenceClient` → Hugging Face’s high-level client for inference, which can connect to multiple providers (Hugging Face, Together, etc.).

`from huggingface_hub import InferenceClient` means:

- You are importing the class `InferenceClient` from the `huggingface_hub` Python library.
- `huggingface_hub` is the official Hugging Face SDK for:
  - downloading/uploading models, datasets, and spaces  
  - managing tokens and repos  
  - and now also running inference (querying models)  

- `dotenv` → loads variables from a `.env` file into your environment.

```python
load_dotenv(override=True)
```

Loads any keys/values from your `.env` file.

```python
client = InferenceClient(
    provider="together",
    api_key=os.environ["HF_TOKEN"],
)
```

- Creates an inference client.
- `provider="together"` → tells Hugging Face to route calls to the Together AI backend (instead of Hugging Face’s own inference or another provider).
- `api_key=os.environ["HF_TOKEN"]` → uses your API key for authentication.

⚠️ Normally, for `provider="together"`, you would supply a Together API key, not a Hugging Face token — so this will only work if your HF token is actually linked to Together in your setup.

```python
completion = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ],
)
```

- Calls the Chat Completions API in an OpenAI-style format.
- `model="Qwen/Qwen2.5-7B-Instruct"` → specifies which model to query.
- `messages` → the conversation history, using roles (`system`, `user`, `assistant`).
- Here the user asks: “What is the capital of France?”
- The model should reply: “Paris.”

---

### 7.2 Using OpenAI Python client

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

MODEL = "Qwen/Qwen2.5-7B-Instruct:together"

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

completion = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ],
)

print(completion.choices[0].message.content)
```

Example output:

```text
The capital of France is Paris.
```

#### What each import / line means

- `os` → lets you access environment variables.
- `openai.OpenAI` → the OpenAI-compatible Python client, which can also connect to Hugging Face, Together, DeepInfra, etc., if you point it to the right `base_url`.
- `dotenv` → loads environment variables from a `.env` file (like API keys).

```python
load_dotenv(override=True)
```

- Loads any key/value pairs from your `.env` file into the environment (e.g., `HF_TOKEN=xxx`).
- `override=True` means it will replace existing environment variables if duplicates exist.

```python
MODEL = "Qwen/Qwen2.5-7B-Instruct:together"
```

- This sets the model you want to query.
- ⚠️ The `:together` suffix is something used in Together AI’s routing, not Hugging Face’s. If you use Hugging Face’s router, it should just be `"Qwen/Qwen2.5-7B-Instruct"`.

```python
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)
```

- Creates an OpenAI-style client, but points it at Hugging Face’s OpenAI-compatible Router API.
- `api_key=os.environ["HF_TOKEN"]` pulls your Hugging Face access token from the environment (loaded via `.env`).

```python
completion = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ],
)
```

- Sends a chat completion request to the model.
- The request structure is the same as OpenAI’s chat API:
  - `model` → which model to use  
  - `messages` → list of chat messages (roles: `system`, `user`, `assistant`)  
- Expected behavior: the model should respond with `"The capital of France is Paris."`
