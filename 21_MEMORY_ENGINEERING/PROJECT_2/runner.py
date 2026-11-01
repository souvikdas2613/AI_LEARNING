import asyncio
import os

from dotenv import load_dotenv

from answer import format_answer
from executor import execute_action
from loop import run_agent_loop
from mcp_client import connect, disconnect, discover_tools
from memory import create_database
from planner import planner

load_dotenv()


async def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY not set — add it to .env")

    create_database()
    client = await connect()

    tools = await discover_tools(client)

    print("\nAvailable Tools")
    print("----------------")

    for tool in tools:
        print(tool.name)

    user_request = input("\nUser : ")

    state = await run_agent_loop(
        user_request,
        planner,
        execute_action,
        format_answer,
        tools,
        client,
    )

    print("\nFinal Answer")
    print("------------")
    print(state["final_answer"])

    await disconnect(client)


if __name__ == "__main__":
    asyncio.run(main())
