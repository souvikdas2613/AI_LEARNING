# imports

import os
from dotenv import load_dotenv
from openai import OpenAI


# environment

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME')

# initialize OpenAI client
openai = OpenAI()

system_message = "You are an assistant that reimplements Python code in high performance C++ for an M1 Mac. Respond only with C++ code; use comments sparingly and do not provide any explanation other than occasional comments. The C++ response needs to produce an identical output in the fastest possible time."

print ("system prompt messge :\n")
print (system_message)

def user_prompt_for(python):
    user_prompt = "Rewrite this Python code in C++ with the fastest possible implementation that produces identical output in the least time. Respond only with C++ code; do not explain your work other than a few comments. Pay attention to number types to ensure no int overflows. Remember to #include all necessary C++ packages such as iomanip.\n\n"
    user_prompt += python
    return user_prompt

def messages_for(python):
    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt_for(python)}
    ]


def write_output(cpp):
    code = cpp.replace("```cpp","\n").replace("```","\n")
    with open("Converted_CPP_Code.cpp", "w") as f:
        f.write(code)

def optimize_gpt(python):
    """Ask the model once; print and save the full C++ reply."""
    print("\n\nConverted Python to C++ Code Below :\n\n\n")
    response = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=messages_for(python),
    )
    reply = (response.choices[0].message.content or "").strip()
    print(reply)
    write_output(reply)


with open("test_python_code.py", "r") as f:
    test_python_code_file = f.read()   # Read the whole file into a string

print ("\n\nINPUT PYTHON FILE :  \n")
print(test_python_code_file)

print ("\n\nExecute INPUT PYTHON FILE :  \n")
exec(test_python_code_file)

optimize_gpt(test_python_code_file)
