# Just one import to start with!!
#pip install modal
import modal
from dotenv import load_dotenv
load_dotenv(override=True)
import os


print(os.environ["MODAL_TOKEN_ID"])
print(os.environ["MODAL_TOKEN_SECRET"])

from hello import app, hello

with app.run():
    reply=hello.local()

print (reply)

with app.run():
    reply=hello.remote()

print (reply)

