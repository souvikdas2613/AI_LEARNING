import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def format_answer(state):
    prompt = f"""
    The user asked:
    {state["user_request"]}

    Tasks:
    {state["tasks"]}

    Actions:
    {state["actions"]}

    Observations:
    {state["observations"]}

    Intermediate Results:
    {state["results"]}

    Give the user a natural and concise answer.
    Do not mention planner, agent loop, MCP, internal state, tools, or internal reasoning.
    """
    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME"),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()
