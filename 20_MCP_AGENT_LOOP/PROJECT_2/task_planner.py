import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def decompose_task(user_request):
    prompt = f"""
    You are a task decomposition assistant.
    Break the user's goal into small, independent subtasks.

    User Request:
    {user_request}

    Rules:
    1. Each line is exactly one subtask.
    2. Use short imperative phrases (e.g. "Get the current time").
    3. Do not number lines or use bullets.
    4. Do not explain anything else.
    5. If the request is already one step, return one line only.

    Subtasks:
    """
    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME"),
        messages=[
            {"role": "system", "content": "You decompose user goals into subtasks."},
            {"role": "user", "content": prompt},
        ],
    )

    print("\ninside task_planner.py file - Task Plan")
    print("---------")
    print(response.choices[0].message.content.strip())

    text = response.choices[0].message.content.strip()
    tasks = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        for prefix in ("- ", "* ", "• "):
            if line.startswith(prefix):
                line = line[len(prefix):].strip()
                break
        if len(line) >= 2 and line[0].isdigit() and line[1] in ".)":
            line = line[2:].strip()
        elif len(line) >= 3 and line[0].isdigit() and line[1].isdigit() and line[2] in ".)":
            line = line[3:].strip()
        if line:
            tasks.append(line)
    
    print("\nTask Plan")
    print("---------")
    for task in tasks:
        print(task)
    return tasks if tasks else [user_request]
