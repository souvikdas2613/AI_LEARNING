import os

from dotenv import load_dotenv

from memory_extractor import extract_memory

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise SystemExit("OPENAI_API_KEY not set — add it to .env")

print("=== Tool turn (expect NONE) ===")
print(extract_memory("What is the current time?", "The current time is 10 PM."))

print("\n=== Intro turn (expect a fact about Souvik) ===")
print(
    extract_memory(
        "My name is Souvik and I work on OSAC.",
        "Nice to meet you, Souvik! OSAC sounds like an interesting project.",
    )
)
