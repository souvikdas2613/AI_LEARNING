# imports

import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import json

# Load environment variables from .env
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")


ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}

def get_ticket_price(destination_city):
    print(f"Tool called for city {destination_city}")
    price = ticket_prices.get(destination_city.lower(), "Unknown ticket price")
    return f"The price of a ticket to {destination_city} is {price}"

# Gradio 6: content may be "HI" or [{"type": "text", "text": "HI"}]
def get_text(content):
    if isinstance(content, list):
        return content[0]["text"]
    return content


# There's a particular dictionary structure that's required to describe our function:

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

# And this is included in a list of tools:

tools = [{"type": "function", "function": price_function}]


# We have to write that function handle_tool_call:

def handle_tool_call(message):
    tool_call = message.tool_calls[0]

    print ("\n----------HANDLE TOOL CALL FUCNTION RUNNING----------------------\n")
    print(tool_call)
    print ("\n----------TOOL CALL FUNCTION NAME----------------------\n")
    print(tool_call.function.name)
    if tool_call.function.name == "get_ticket_price":
        arguments = json.loads(tool_call.function.arguments)
        print ("\n----------ARGUMENTS----------------------\n")
        print(arguments)
        city = arguments.get("destination_city")
        print ("\n----------CITY----------------------\n")
        print(city)
        price_details = get_ticket_price(city)
        print ("\n----------PRICE DETAILS----------------------\n")
        print(price_details)
        response = {
            "role": "tool",
            "content": price_details,
            "tool_call_id": tool_call.id
        }
        print ("\n----------RESPONSE----------------------\n")
        print(response)
    return response


# Create OpenAI client (uses OPENAI_API_KEY from environment)
openai = OpenAI()

system_message = """
You are a helpful assistant for an Airline called FlightAI.
Give short, courteous answers, no more than 1 sentence.
Always be accurate. If you don't know the answer, say so.
"""

def chat(message, history):
    history = [{"role": h["role"], "content": get_text(h["content"])} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)

    print ("\n----------CHAT FUCNTION RUNNING----------------------\n")
    print(response.choices[0])

    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message

        print ("\n----------TOOL CALL FUCNTION RUNNING----------------------\n")
        print(message)
        tool_response = handle_tool_call(message)

        print ("\n----------TOOL RESPONSE FUCNTION RUNNING----------------------\n")
        print(tool_response)

        messages.append(message)
        messages.append(tool_response)

        print ("\n----------MESSAGES----------------------\n")
        print(messages)

        print ("\n----------RESPONSE FUCNTION RUNNING----------------------\n")
        

        response = openai.chat.completions.create(model=MODEL_NAME, messages=messages)

        print(response)

    return response.choices[0].message.content


# Gradio 6: do NOT pass type=... (removed; messages format is default)
gr.ChatInterface(fn=chat).launch()
