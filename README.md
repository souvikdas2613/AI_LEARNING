# AI_LEARNING

Personal notes and small experiments for OpenAI Cloud vs local Ollama.

## Start here

1. [What is an LLM?](3_LLM/what_is_an_llm.md) — definition, generative AI, closed vs open, how to use models  
2. [What are tokens?](3_LLM/what_are_tokens.md) — character → word → token  
3. [OpenAI API vs ChatGPT subscription](OpenAI_API_vs_ChatGPT_subscription.md) — package, cloud API, billing vs ChatGPT plans  
4. [Ollama install on Linux](Ollama_install_linux.md) — what Ollama is, why use it, then install / serve / pull / run

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
