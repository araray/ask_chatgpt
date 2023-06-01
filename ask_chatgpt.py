## Requires Python >= 3.11.0
import sys
from typing import List
import tomllib

from chatgpt import ChatGPT


def load_config(file_path: str) -> dict:
    with open(file_path, "rb") as conf_file:
        return tomllib.load(conf_file)


def ask_chatgpt(question: str, config_path: str) -> List[str]:
    config = load_config(config_path)

    api_key = config["openai"]["api_key"]
    model = config["openai"]["model"]
    max_tokens = config["openai"]["max_tokens"]
    temperature = config["openai"]["temperature"]
    top_p = config["openai"]["top_p"]

    chat_model = ChatGPT(api_key, model, max_tokens = max_tokens, temperature = temperature, top_p = top_p)
    answer_pages = chat_model.ask(question)

    return answer_pages


def main() -> None:
    question = sys.argv[1]
    config_path = "config.toml"
    answers = ask_chatgpt(question, config_path)

    for answer in answers:
        print('\n', answer, '\n')


if __name__ == "__main__":
    main()
