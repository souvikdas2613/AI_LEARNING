import os
from dotenv import load_dotenv
from openai import OpenAI

from state import get_pending_tasks

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_tool_descriptions(tools):
    descriptions = ""
    for tool in tools:
        descriptions += f"""
        Tool:
        {tool.name}
        Description:
        {tool.description}
        ----------------------------
        """
    return descriptions


def planner(state, tools):
    tool_descriptions = build_tool_descriptions(tools)
    pending = get_pending_tasks(state)
    prompt = f"""
    You are an AI planner.
    Your job is to select the next unfinished task and the best tool to complete it.

    User Request:
    {state["user_request"]}

    Tasks:
    {state["tasks"]}

    Pending Tasks:
    {pending}

    Completed Actions:
    {state["actions"]}

    Observations:
    {state["observations"]}

    Intermediate Results:
    {state["results"]}

    Available Tools:
    {tool_descriptions}

    Rules:
    1. Select only ONE pending task.
    2. The TASK must be copied EXACTLY from the pending task list.
    3. Do not change the task wording.
    4. Do not select a completed task.
    5. Select the best available tool for that task.
    6. Use previous observations and results.
    7. If an action failed, reconsider the task.
    8. If there are no pending tasks, return ONLY the word: FINISH
    9. If tasks are still pending, return exactly two lines in this format:
       TASK: <exact pending task>
       TOOL: <tool_name>
    10. Do not explain anything.

    Next Decision:
    """
    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME"),
        messages=[
            {"role": "system", "content": "You are an AI planner."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()
