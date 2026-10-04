"""
Simple Llama chat on Modal — instruct model, short answer only.
Needs Modal secret hf-secret (HF_TOKEN). See 4_llama_py.md
"""
import modal
from modal import Image

app = modal.App("llama-inference")
image = Image.debian_slim().pip_install("torch", "transformers", "accelerate")
secrets = [modal.Secret.from_name("hf-secret")]

MODEL = "meta-llama/Llama-3.2-3B-Instruct"


@app.function(image=image, secrets=secrets, timeout=1800)
def generate(question: str) -> str:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.float32)

    messages = [{"role": "user", "content": question}]
    input_ids = tokenizer.apply_chat_template(
        messages,
        return_tensors="pt",
        add_generation_prompt=True,
    )["input_ids"]
    prompt_len = input_ids.shape[-1]

    new_token_ids = model.generate(input_ids, max_new_tokens=32, do_sample=False)
    answer_ids = new_token_ids[0][prompt_len:]
    return tokenizer.decode(answer_ids, skip_special_tokens=True).strip()
