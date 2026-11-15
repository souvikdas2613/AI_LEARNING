import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from executor import execute_action
from loop import run_agent_loop
from mcp_manager import close_servers, create_tool_registry
from planner import MODEL, planner

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SERVERS = ["time-mcp-server/server.py", "weather-mcp-server/server.py"]


def format_answer(state):
    prompt = (
        f"The user asked: {state['user_request']}\n"
        f"Actions performed: {state['actions']}\n"
        f"Observations: {state['observations']}\n"
        "Answer the user naturally. Do not mention planning, state, or tools."
    )
    return client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}]).choices[0].message.content.strip()


async def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY not set — add it to AI_LEARNING/AI_LEARNING/.env")
    clients, tool_registry = await create_tool_registry(SERVERS)
    tools = [entry["tool"] for entry in tool_registry.values()]
    print("\nAvailable Tools")
    print("----------------")
    for tool in tools:
        print(tool.name)
    user_request = input("\nUser : ")
    try:
        state = await run_agent_loop(user_request, planner, execute_action, format_answer, tools, tool_registry)
        print("\nFinal Answer:")
        print(state["final_answer"])
    finally:
        await close_servers(clients)


if __name__ == "__main__":
    asyncio.run(main())