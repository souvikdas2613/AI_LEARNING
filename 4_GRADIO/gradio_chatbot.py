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


def get_text(content):
    """Gradio 6 may give content as a string OR a list of parts. Return plain text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                parts.append(part.get("text", ""))
            elif isinstance(part, str):
                parts.append(part)
        return "".join(parts)
    return str(content)


def chat(message, history):
    """
    Gradio ChatInterface calls this on every Send.

    message  = the new text the user just typed
    history  = earlier chat turns already on screen
               e.g. [{"role": "user", "content": "Hi"},
                     {"role": "assistant", "content": "Hello!"}]
    """

    # Start with the system message
    messages = [{"role": "system", "content": system_message}]

    print(f"\ninitial messages:\n {messages}")

    # Add past turns (keep only role + content as plain text)
    for turn in history:
        messages.append(
            {"role": turn["role"], "content": get_text(turn["content"])}
        )

    # Add the new user message
    messages.append({"role": "user", "content": message})

    print(f"\nfinal messages:\n {messages}")

    # Call the model and return the reply text
    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages)
    return response.choices[0].message.content


# Gradio 6: do NOT pass type="messages" (that arg was removed; messages is default)
gr.ChatInterface(fn=chat).launch()
