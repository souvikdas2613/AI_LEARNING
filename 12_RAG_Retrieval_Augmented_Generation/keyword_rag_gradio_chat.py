# Keyword RAG + Gradio: load markdown dict → match words in question → OpenAI chat.

import os
import glob
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

os.chdir(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

MODEL_NAME = os.getenv("MODEL_NAME")
if MODEL_NAME:
    print(f"Using model: {MODEL_NAME}")
else:
    print("MODEL_NAME not set in .env")
openai = OpenAI()

# Load employee (key = last name) and product (key = filename) markdown into one dict.
knowledge = {}
employee_keys = set()

for filename in glob.glob("knowledge-base/employees/*"):
    key = Path(filename).stem.split(" ")[-1].lower()
    employee_keys.add(key)
    with open(filename, encoding="utf-8") as f:
        knowledge[key] = f.read()

print(f"[RAG load] {len(employee_keys)} employees + {len(knowledge) - len(employee_keys)} products in knowledge dict.")

print ("employee_keys:\n\n")
print (employee_keys)
print ("knowledge:\n\n")
for key, value in knowledge.items():
    print (key)           
    print (value)           
    print ("\n\n")


SYSTEM_PREFIX = """
You represent Insurellm, the Insurance Tech company.
You are an expert in answering questions about Insurellm; its employees and its products.
You are provided with additional context that might be relevant to the user's question.
Give brief, accurate answers. If you don't know the answer, say so.

Relevant context:
"""


def chat(message, history):
    print(f"\n[Gradio] user: {message!r}")

    # Retrieve: any word in the message that matches a dict key
    words = "".join(ch for ch in message if ch.isalpha() or ch.isspace()).lower().split()

    print ("words:\n\n")
    print (words)
    print ("\n\n")  

    for w in words:
        if w in knowledge and w in employee_keys:
            print(f"[RAG retrieve] employee file for last name '{w}'")
        elif w in knowledge:
            print(f"[RAG retrieve] product file for '{w}'")

    retrieved_employee_data = [knowledge[w] for w in words if w in knowledge]

    print ("retrieved_employee_data:\n\n")
    print (retrieved_employee_data)
    print ("\n\n")

    if retrieved_employee_data:
        extra = "The following additional context might be relevant in answering the user's question:\n\n"
        extra += "\n\n".join(retrieved_employee_data)
        print(f"[RAG augment] {len(retrieved_employee_data)} file(s), {sum(len(c) for c in retrieved_employee_data)} chars")
    else:
        extra = "There is no additional context relevant to the user's question."
        print("[RAG augment] nothing matched — no docs in prompt")

    system_message = SYSTEM_PREFIX + extra
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]

    print(f"[OpenAI] model={MODEL_NAME}")
    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages)
    return response.choices[0].message.content


gr.ChatInterface(chat).launch(inbrowser=True)
