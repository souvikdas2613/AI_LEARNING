# imports

import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Load environment variables from .env
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

# Create OpenAI client (uses OPENAI_API_KEY from environment)
openai = OpenAI()

# System prompt — tells the model how to behave
system_message = "You are a helpful assistant"


def message_gpt(prompt):
    """Send user prompt to the LLM and return the reply text."""

    # Chat messages: system sets behavior, user is the actual question
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt},
    ]

    # Call the model
    response = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
    )

    # Return only the assistant's text
    return response.choices[0].message.content


# Quick test in the terminal (optional)
print(message_gpt("What is the capital of France?"))

# Launch a simple Gradio UI: textbox in → textbox out
gr.Interface(
    fn=message_gpt,
    inputs="textbox",
    outputs="textbox",
    flagging_mode="never",
).launch()
