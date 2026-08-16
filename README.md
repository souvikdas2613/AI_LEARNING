
# Welcome to the learning journey with **Souvik**

This is **Souvik’s** personal AI learning space — notes, practice scripts, and small experiments while exploring LLMs, prompts, Gradio, and more.

---

## Why people should read this

If you are new to AI and feel lost in big words, this journey is for you.

**Souvik** is learning AI the practical way — not only theory, but small programs you can run, break, and understand. Each folder builds on the last:

- start with *what AI even is*
- make your first real LLM calls (cloud + local)
- learn how prompts work
- understand tokens and how chat “memory” really works
- build simple Gradio UIs and chatbots
- teach the LLM to use **tools** (real Python functions) for accurate answers
- understand **AI Agents** — brain (LLM) + body (tools) working toward a goal
- explore **Hugging Face** — open models, Hub, transformers, Spaces
- use **Google Colab** — cloud notebooks + GPUs for heavier model experiments
- learn **quantization** — load big models with fewer bits (8-bit / 4-bit)
- try **audio transcription** — free HF Whisper vs paid OpenAI API

These notes are written in plain language, with step-by-step explanations, so beginners can follow along without fear.  
If **Souvik** can learn it this way, you can too.

---

## Index

| # | Topic | What’s inside |
|---|--------|----------------|
| 0 | [`0_WHAT_IS_AI`](0_WHAT_IS_AI/) | Basics — what AI / ML / DL / generative AI mean |
| 1 | [`1_PRACTICE_ON_OLLAMA_and_OPENAI`](1_PRACTICE_ON_OLLAMA_and_OPENAI/) | First API calls — OpenAI cloud + local Ollama |
| 2 | [`2_USER_PROMPT_SYSTEM_PROMPT`](2_USER_PROMPT_SYSTEM_PROMPT/) | System prompt vs user prompt |
| 3 | [`3_LLMs_and_TOKENS`](3_LLMs_and_TOKENS/) | What an LLM is, tokens, stateless calls |
| 4 | [`4_GRADIO`](4_GRADIO/) | Gradio UIs + chatbot with chat history |
| 5 | [`5_TOOLS_FUNCTIONS`](5_TOOLS_FUNCTIONS/) | LLM tools / function calling (FlightAI ticket price) |
| 6 | [`6_AGENTS_AND_TOOLS`](6_AGENTS_AND_TOOLS/) | AI Agents, workflow patterns, frameworks, tools theory |
| 7 | [`7_HUGGING_FACE`](7_HUGGING_FACE/) | Hugging Face — Hub, pipelines, Spaces |
| 8 | [`8_GOOGLE_COLAB`](8_GOOGLE_COLAB/) | Google Colab — cloud notebooks, GPUs, secrets |
| 9 | [`9_QUANTIZATION`](9_QUANTIZATION/) | Quantization — 8-bit / 4-bit, BitsAndBytes |
| 10 | [`10_AUDIO_TRANSCRIPTION`](10_AUDIO_TRANSCRIPTION/) | Audio → text — free HF Whisper vs paid OpenAI |

### Topic 5 highlight

- Chapter intro: [`5_TOOLS_FUNCTIONS/README.md`](5_TOOLS_FUNCTIONS/README.md) — what tools mean in AI  
- Script: [`tool_functions_1.py`](5_TOOLS_FUNCTIONS/tool_functions_1.py)  
- Notes: [`tool_functions_1.md`](5_TOOLS_FUNCTIONS/tool_functions_1.md) — tool schema, `handle_tool_call`, why 2 LLM calls, real Paris price print trace  

### Topic 6 highlight

- Notes: [`agents_and_tools.md`](6_AGENTS_AND_TOOLS/agents_and_tools.md) — what is an Agent, workflow vs agent patterns, frameworks, LLM brain, tools theory  

### Topic 7 highlight

- Notes: [`what_is_huggingface.md`](7_HUGGING_FACE/what_is_huggingface.md) — Hugging Face Hub, `pipeline`, Spaces, inference APIs, create `HF_TOKEN`  
- Scripts: [`test_hugging_face_using_huggingFaceHUB.py`](7_HUGGING_FACE/test_hugging_face_using_huggingFaceHUB.py) · [`test_hugging_face_using_OPENAI.py`](7_HUGGING_FACE/test_hugging_face_using_OPENAI.py)  
- Script notes: [`test_hugging_face_using_huggingFaceHUB.md`](7_HUGGING_FACE/test_hugging_face_using_huggingFaceHUB.md) · [`test_hugging_face_using_OPENAI.md`](7_HUGGING_FACE/test_hugging_face_using_OPENAI.md)  

### Topic 8 highlight

- Notes: [`what_is_google_colab.md`](8_GOOGLE_COLAB/what_is_google_colab.md) — free tier limits, how to check GPU/usage, Colab vs local  

### Topic 9 highlight

- Notes: [`what_is_quantization.md`](9_QUANTIZATION/what_is_quantization.md) — fewer bits per weight, BitsAndBytesConfig, double quant, path to QLoRA  
- Practice: [`colab_quantization_explained.ipynb`](9_QUANTIZATION/colab_quantization_explained.ipynb) — Colab GPU 4-bit load + generate  

### Topic 10 highlight

- Practice: [`colab_audio_transcription.ipynb`](10_AUDIO_TRANSCRIPTION/colab_audio_transcription.ipynb) — free HF Whisper vs paid `gpt-4o-mini-transcribe`  

### Extra notes

- [`OpenAI_API_vs_ChatGPT_subscription.md`](OpenAI_API_vs_ChatGPT_subscription.md) — API billing vs ChatGPT plans  
- [`Ollama_install_linux.md`](Ollama_install_linux.md) — install and run Ollama on Linux  
=======
# AI_LEARNING

Personal notes and small experiments for OpenAI Cloud vs local Ollama.

## Start here

1. [OpenAI API vs ChatGPT subscription](OpenAI_API_vs_ChatGPT_subscription.md) — package, cloud API, billing vs ChatGPT plans  
2. [Ollama install on Linux](Ollama_install_linux.md) — what Ollama is, why use it, then install / serve / pull / run

## Hands-on scripts

Folder: [`1_PRACTICE_ON_OLLAMA_and_OPENAI/`](1_PRACTICE_ON_OLLAMA_and_OPENAI/)

| Script | Notes |
|--------|--------|
| [`Test_OPENAI_LLM_with_openAI.py`](1_PRACTICE_ON_OLLAMA_and_OPENAI/Test_OPENAI_LLM_with_openAI.py) · [md](1_PRACTICE_ON_OLLAMA_and_OPENAI/Test_OPENAI_LLM_with_openAI.md) | Call OpenAI cloud (`gpt-4.1-nano`) |
| [`Test_ollama_with_OPENAI.py`](1_PRACTICE_ON_OLLAMA_and_OPENAI/Test_ollama_with_OPENAI.py) · [md](1_PRACTICE_ON_OLLAMA_and_OPENAI/Test_ollama_with_OPENAI.md) | Call local Ollama via OpenAI-compatible API |

## Run (this laptop)

```bash
source ~/miniforge3/bin/activate
conda activate my-proj
cd /home/soudas/PERSONAL/AI_LEARNING/AI_LEARNING
```

Keep secrets in `.env` at this repo root (`OPENAI_API_KEY=<your_openai_api_key_here>`). It is gitignored.
