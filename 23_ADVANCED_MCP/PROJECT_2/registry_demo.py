import asyncio
from mcp_manager import close_servers, create_tool_registry, run_tool

SERVERS = ["time-mcp-server/server.py", "weather-mcp-server/server.py"]

async def main():
    clients, tool_registry = await create_tool_registry(SERVERS)
    try:
        print("\nAvailable Tools")
        print("----------------")
        for tool_name in sorted(tool_registry):
            print(tool_name)
        result = await run_tool(tool_registry, "get_weather", {"city": "Delhi"})
        print("\nTool Result:")
        print(result)
    finally:
        await close_servers(clients)

if __name__ == "__main__":
    asyncio.run(main())