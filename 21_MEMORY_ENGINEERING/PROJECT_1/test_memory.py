import os

from dotenv import load_dotenv
from memory import *

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise SystemExit("OPENAI_API_KEY not set — add it to .env")

create_database()
clear_memories()

save_memory("My name is Souvik.", "Nice to meet you, Souvik.")
save_memory("I am learning Python.", "Python is useful for AI development.")
save_memory("I am learning about MCP.", "MCP allows AI applications to use tools.")

print("\nStored Memories")
print("-----------------")
for entry in list_memories():
    print(f"\n[{entry['id']}] {entry['created_at']}")
    print("User:", entry["user_message"])
    print("Assistant:", entry["assistant_message"])

results = search_semantic_memories("What is my name")

print("\nRelevant Memories")
print("-----------------")

for result in results:
    print("\nScore:", result["score"])
    print("User:", result["user_message"])
    print("Assistant:", result["assistant_message"])
