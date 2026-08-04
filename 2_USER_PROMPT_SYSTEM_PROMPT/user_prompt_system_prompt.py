# imports

import os
from dotenv import load_dotenv
from openai import OpenAI
from bs4 import BeautifulSoup
import requests

# Load environment variables in a file called .env

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME')

# Check the key

if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
else:
    print("API key found and looks good so far!")

if not MODEL_NAME:
    print("\n\nNo model name was found - please head over to the .env file to identify & fix!")
else:
    print("\n\nModel name found " + MODEL_NAME + " and looks good so far!\n\n")


# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

def fetch_website_contents(url):
    """
    Return the title and contents of the website at the given url;
    truncate to 2,000 characters as a sensible limit
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n" + text)[:2_000]

print ("\n\n\nFirst part of the program starts here | NO LLM CALL \n==================================================\n\n")

hp = fetch_website_contents("https://www.harrypotter.com/")
print ("Harry Potter Website Contents:\n\n\n")
print(hp)

print ("\n\n\nFirst part of the program ends here | NO LLM CALL \n==================================================\n\n")

print ("\n\n\nSecond part of the program starts here | LLM CALL \n==================================================\n\n")

# Define our system prompt - you can experiment with this later, changing the last sentence to 'Respond in markdown in Spanish."

system_prompt = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""


# Define our user prompt

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.

"""

# See how this function creates exactly the format above

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website}
    ]

# And now: call the OpenAI API. You will get very familiar with this!

openai = OpenAI()

def summarize(url):
    website = fetch_website_contents(url)
    response = openai.chat.completions.create(
        model = MODEL_NAME,
        messages = messages_for(website)
    )

    print("\n\nMessages for the website:\n\n", messages_for(website))
    print ("\n\nSummarizing the website...\n\n")

    return response.choices[0].message.content


print(summarize("https://www.harrypotter.com/"))

print ("\n\n\nSecond part of the program ends here | LLM CALL \n==================================================\n\n")