##
## Requires Python >= 3.11.0
import sys
import tomllib

from chatgpt import ChatGPT

question = sys.argv[1]

config = []
with open("config.toml", "rb") as conf:
    config = tomllib.load(conf)

api_key = config["openai"]["api_key"]
model = config["openai"]["model"]
max_tokens = config["openai"]["max_tokens"]

chat = ChatGPT(api_key, model, max_tokens = max_tokens)

answer_pages = chat.ask(question)
#answer_pages = chat.ask_debug(question)

for page in answer_pages:
    print(page,'\n')

