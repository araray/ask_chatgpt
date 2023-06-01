import openai
import time
import requests
import logging

from string import Template

logging.basicConfig(level=logging.INFO)

class ChatGPT:
    def __init__(self, api_key, model_engine, max_tokens = 2048, temperature=0.6, top_p=1.0):
        openai.api_key = api_key
        self.model_engine = model_engine
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.messages = []

    def _create_paginated_prompts(self, words_list, tokens_per_page):
        paginated_prompts, prompt, leftover_word = [], '', ''
        max_chars_per_page = tokens_per_page * 4 
        reserved_chars = 21 
        for word in words_list:
            word_length = len(word) + 1 
            if (len(prompt) + word_length + len(leftover_word) + reserved_chars) < max_chars_per_page:
                prompt += leftover_word + f' {word}'
                leftover_word = ''
            else:
                paginated_prompts.append(prompt)
                leftover_word = f' {word}'
                prompt = ''
        paginated_prompts.append(prompt)

        for index, prompt in enumerate(paginated_prompts):
            header = f'PART {index+1} OF {len(paginated_prompts)}:\n'
            paginated_prompts[index] = header + prompt if len(paginated_prompts) > 1 else prompt

        return paginated_prompts

    def _split_prompt_into_words(self, prompt):
        return self._create_paginated_prompts(prompt.split(), self.max_tokens)

    def _get_chat_response(self, prompt):
        print('---', '\n', 'Sending prompt: ', prompt, '\n')
        
        for i in range(5):  # Retry up to 5 times
            try:
                response = openai.ChatCompletion.create(
                    model=self.model_engine,
                    messages=[{'role': 'user', 'content': prompt}] + self.messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    top_p=self.top_p
                )
                self.messages.append(response['choices'][0]['message'])
                return response['choices'][0]['message']['content']
            except requests.exceptions.RequestException as e:
                logging.error("Request failed with %s, retrying...", e)
                time.sleep((2 ** i) + (random.randint(0, 1000) / 1000))  # Exponential backoff
        raise Exception("API request failed after multiple attempts")

    def ask(self, prompt, role='user'):
        self.messages.append({'role': role, 'content': prompt})
        paginated_prompts = self._split_prompt_into_words(prompt)
        chat_responses = []

        for paginated_prompt in paginated_prompts:
            response = self._get_chat_response(paginated_prompt)
            chat_responses.append(response)
            while not response.strip().endswith('.'):
                response = self._get_chat_response('Please continue the incomplete response.', role='user')
                chat_responses.append(response)

        return chat_responses
