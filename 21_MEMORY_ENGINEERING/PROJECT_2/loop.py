from state import (
    add_action,
    add_memory,
    add_result,
    add_task,
    all_tasks_completed,
    can_continue,
    complete_task,
    create_state,
    finish,
    next_step,
    record_observation,
)
from memory import save_memory, search_semantic_memories
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


def finish_and_remember(state, user_request, format_answer):
    answer = format_answer(state)
    finish(state, answer)
    save_memory(user_request, answer)
    return answer


async def run_agent_loop(
    user_request,
    planner,
    execute_action,
    format_answer,
    tools,
    client,
):
    state = create_state(user_request)

    memories = search_semantic_memories(user_request, max_results=3)
    for memory in memories:
        add_memory(state, memory)

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
            finish_and_remember(state, user_request, format_answer)
            break

        print(f"\n--- Step {state['current_step'] + 1} ---")

        decision = planner(state, tools)
        print("Planner Decision:")
        print(decision)

        if decision.strip().upper() == "FINISH":
            finish_and_remember(state, user_request, format_answer)
            break

        task, tool = parse_decision(decision)
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

    if not state["finished"]:
        print("\nWarning: loop stopped before FINISH (step limit or invalid planner output).")
        finish_and_remember(state, user_request, format_answer)

    return state
