from state import create_state, add_task, add_action, record_observation, add_result, complete_task, all_tasks_completed, next_step, can_continue, finish
from task_planner import decompose_task


def parse_decision(decision):
    task = None
    tool = None
    for line in decision.splitlines():
        line = line.strip()
        if line.startswith("TASK:"):
            task = line[5:].strip()
        elif line.startswith("TOOL:"):
            tool = line[5:].strip()
    if task and "TOOL:" in task:
        parts = task.split("TOOL:", 1)
        task = parts[0].strip()
        if not tool:
            tool = parts[1].strip()
    return task, tool


async def run_agent_loop(user_request, planner, execute_action, format_answer, tools, client):
    state = create_state(user_request)
    planned_tasks = decompose_task(user_request)
    for task in planned_tasks:
        add_task(state, task)
    print("\nTask Plan")
    print("---------")
    for item in state["tasks"]:
        print("-", item["task"])
    while can_continue(state):
        if all_tasks_completed(state):
            print(f"\n--- Step {state['current_step'] + 1} ---")
            print("Planner Decision:")
            print("TASK: FINISH")
            answer = format_answer(state)
            finish(state, answer)
            break
        print(f"\n--- Step {state['current_step'] + 1} ---")
        decision = planner(state, tools)
        print("Planner Decision:")
        print(decision)
        if decision.strip().upper() == "FINISH":
            answer = format_answer(state)
            finish(state, answer)
            break
        task, tool = parse_decision(decision)
        print("\ninside loop.py file - Task and Tool")
        print("---------")
        print(task)
        print(tool)
        if not task or not tool:
            add_result(state, "Invalid planner decision.")
            next_step(state)
            continue
        state["current_task"] = task
        observation = await execute_action(tool, state, client)
        print("Observation:", observation)
        add_action(state, tool)
        record_observation(state, tool, observation)
        add_result(state, observation)
        if not observation.lower().startswith("error"):
            complete_task(state, task)
            print("completed")
        else:
            add_result(state, "The previous action failed. The planner must reconsider.")
        next_step(state)
    return state
