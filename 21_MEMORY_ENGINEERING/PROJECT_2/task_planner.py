import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _looks_like_tool_request(user_request):
    lower = user_request.lower()
    hints = (
        "time",
        "dice",
        "die",
        "roll",
        "password",
        "passwd",
        "current_time",
        "roll_dice",
        "generate_password",
    )
    return any(h in lower for h in hints)


def _memory_or_chat_only(user_request):
    lower = user_request.lower().strip()
    patterns = (
        r"what('s| is) my name",
        r"who am i",
        r"what did we (talk|discuss)",
        r"^(hi|hello|hey)\b",
        r"how are you",
        r"my name is ",
    )
    return any(re.search(p, lower) for p in patterns)


def _heuristic_tool_tasks(user_request):
    lower = user_request.lower()
    tasks = []
    if "time" in lower:
        tasks.append("Get the current time")
    if "dice" in lower or "die" in lower or "roll" in lower:
        tasks.append("Roll a dice")
    if "password" in lower or "passwd" in lower:
        tasks.append("Generate a password")
    return tasks if tasks else [user_request.strip()]


def _parse_task_lines(result):
    tasks = []
    for line in result.splitlines():
        line = line.strip()
        if not line or line.upper() == "NONE":
            continue
        for prefix in ("- ", "* ", "• "):
            if line.startswith(prefix):
                line = line[len(prefix) :].strip()
                break
        if len(line) >= 2 and line[0].isdigit() and line[1] in ".)":
            line = line[2:].strip()
        elif len(line) >= 3 and line[0].isdigit() and line[1].isdigit() and line[2] in ".)":
            line = line[3:].strip()
        if line:
            tasks.append(line)
    return tasks


def decompose_task(user_request):
    prompt = f"""
You are an AI task planner.

Break the user's request into smaller tasks.

Rules:

1. Create only necessary tasks.
2. Put tasks in execution order.
3. Each task should be a short action.
4. Return one task per line.
5. Do not number the tasks.
6. Do not explain anything.

If the user asks for MCP-style actions, you MUST return tasks (never NONE):
- current time / clock / date → a task to get the time
- roll dice / roll a die → a task to roll the dice
- generate password / passwd → a task to generate a password

CRITICAL RULE — return NO tasks (or only the word NONE) only when the request is clearly:
   1. Greetings or casual conversation (e.g., "hi", "hello")
   2. Introductions or personal details (e.g., "my name is Souvik")
   3. Memory questions (e.g., "what is my name?", "what did we discuss earlier?")
   4. General knowledge with no tool action (e.g., "what is Machine Learning?")

User Request:

{user_request}
"""

    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You are an AI task planner."},
            {"role": "user", "content": prompt},
        ],
    )

    result = response.choices[0].message.content.strip()
    tasks = _parse_task_lines(result)

    if tasks:
        return tasks

    if _memory_or_chat_only(user_request):
        return []

    if _looks_like_tool_request(user_request):
        return _heuristic_tool_tasks(user_request)

    return []
