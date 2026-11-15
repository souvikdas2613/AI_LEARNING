from mcp_manager import run_tool

async def execute_action(action, state, tool_registry):
    result = await run_tool(tool_registry, action["tool"], action.get("arguments", {}))
    return result.content[0].text if hasattr(result, "content") and result.content else str(result)