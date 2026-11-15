from state import add_action, can_continue, create_state, finish, next_step, record_observation

async def run_agent_loop(user_request, planner, execute_action, format_answer, tools, tool_registry):
    state = create_state(user_request)
    while can_continue(state):
        action = planner(state, tools)
        print("Planner Selected:", action)
        if action["tool"] == "FINISH":
            finish(state, format_answer(state))
            break
        observation = await execute_action(action, state, tool_registry)
        add_action(state, action)
        record_observation(state, action, observation)
        next_step(state)
    return state