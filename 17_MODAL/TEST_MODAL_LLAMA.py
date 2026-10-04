"""Run: python TEST_MODAL_LLAMA.py — ask Llama one question on Modal."""
import modal
from dotenv import load_dotenv

load_dotenv(override=True)

from llama import app, generate

QUESTION = "What is 2+2? Reply with only the number."

with modal.enable_output():
    with app.run():
        answer = generate.remote(QUESTION)

print("Question:", QUESTION)
print("Answer:", answer)
