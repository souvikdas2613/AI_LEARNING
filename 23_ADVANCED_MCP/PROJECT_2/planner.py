import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", os.getenv("MODEL_NAME", "gpt-4.1-mini"))


def build_tool_descriptions(tools):
    lines = []
    for tool in tools:
        schema = getattr(tool, "input_schema", None) or getattr(tool, "inputSchema", {})
        lines.append(f"Tool: {tool.name}\nDescription: {tool.description or ''}\nInput Schema: {schema}\n----------------------------")
    return "\n".join(lines)


def _parse_planner_json(text):
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)
    return json.loads(text)


def planner(state, tools):
    prompt = (
        "You are an AI Planner. Decide ONLY the next action.\n\n"
        f"User Request:\n{state['user_request']}\n\n"
        f"Completed Actions:\n{state['actions']}\n\n"
        f"Previous Observations:\n{state['observations']}\n\n"
        f"Available Tools:\n{build_tool_descriptions(tools)}\n\n"
        "Rules:\n"
        "1. Choose only ONE next action.\n"
        "2. Never repeat a completed action.\n"
        "3. Use observations for what is still required.\n"
        "4. If satisfied, return FINISH.\n"
        "5. Return ONLY valid JSON (no markdown).\n\n"
        'Format: {"tool": "tool_name", "arguments": {}}\n'
        'FINISH: {"tool": "FINISH", "arguments": {}}\n\n'
        "Next Action:"
    )
    raw = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an AI planner. Output JSON only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    ).choices[0].message.content.strip()
    return _parse_planner_json(raw)