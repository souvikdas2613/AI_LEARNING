from mcp_client import connect, disconnect, discover_tools, execute_tool


def print_registry_summary(clients, tool_registry):
    print(f"\nMCP sessions: {len(clients)}")
    for i, client in enumerate(clients):
        tool_names = sorted(
            name for name, entry in tool_registry.items() if entry["client"] is client
        )
        label = getattr(client, "name", f"client-{i}")
        print(f"  [{i}] {label} → {', '.join(tool_names) or '(no tools)'}")
    print(f"\nTool registry keys ({len(tool_registry)}):")
    for name in sorted(tool_registry):
        print(f"  - {name}")


async def create_tool_registry(servers):
    clients = []
    tool_registry = {}
    for server in servers:
        client = await connect(server)
        clients.append(client)
        for tool in await discover_tools(client):
            tool_registry[tool.name] = {"client": client, "tool": tool}
    print_registry_summary(clients, tool_registry)
    return clients, tool_registry


async def close_servers(clients):
    for client in clients:
        await disconnect(client)


async def run_tool(tool_registry, tool_name, arguments):
    entry = tool_registry.get(tool_name)
    if entry is None:
        raise ValueError(f"Unknown tool: {tool_name}")
    return await execute_tool(entry["client"], tool_name, arguments)