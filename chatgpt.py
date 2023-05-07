import openai
import paginate as pag
import re

from string import Template

class ChatGPT:
    def __init__(self, api_key, model_engine, max_tokens = 2048):
        openai.api_key = api_key
        self.model_engine = model_engine
        self.max_token_length = max_token_length
        self.messages = []

    def _paginate(self, words_list, mtpp):
        tpages = []
        pages = []
        mcpp = mtpp * 4 #maximum number of characters in a page
        page = ''
        carry_word = ''
        header = Template('PART $pagenumber OF $totalpages:\n')
        reserved_chars = 21
        for word in words_list:
            wl = len(word) + 1 #to account for the extra space between words
            if (len(page) + wl + len(carry_word) + reserved_chars) < mcpp:
                if len(carry_word) > 0:
                    page += carry_word
                    carry_word = ''
                page += f' {word}'
            else:
                tpages.append(page)
                carry_word = f' {word}'
                page = ''
        tpages.append(page)
        npages = len(tpages)
        if npages > 1:
            i = 0
            for page in tpages:
                i += 1
                h = header.substitute(pagenumber = f'{i}', totalpages = f'{npages}')
                page = h + page
                pages.append(page)
        else:
            pages = tpages
        return pages

    def _paginate_input(self, prompt):
        tokens = prompt.split()
        return self._paginate(tokens, self.max_token_length)

    def _send_prompt(self, prompt):
        self._chat_session('user', prompt)
        print('Sending prompt: ', prompt)
        response = openai.ChatCompletion.create(
            model = self.model_engine,
            messages = self.messages,
            max_tokens = self.max_token_length,
            n = 1,
            stop = None,
            temperature = 0.6,
#            stream = True
        )
        self.messages.append(response['choices'][0]['message'])
        text = response['choices'][0]['message']['content']
        return text

    def _chat_session(self, role, content):
        message = {'role': f'{role}', 'content': f'{content}'} 
        self.messages.append(message)

    def ask(self, prompt):
        prompt_pages = self._paginate_input(prompt)
        output_pages = []
        if len(prompt_pages) > 1:
            self._send_prompt('My prompt is split in multiple parts. Each part starts with a "PART NUMBER OF TOTAL:" string where NUMBER is the number of the part and TOTAL is the total amount of parts. Please consider all parts together as a single input.')
        for prompt_page in prompt_pages:
            response = self._send_prompt(prompt_page)
        output_pages.append(response)
        continue_asking = 1
        while continue_asking == 1:
            for c in response[-1:]:
                if c == '.':
                    continue_asking = 0
                else:
                    response = self._send_prompt(f'The answer was truncated or incomplete. Please continue from where it stopped.')
                    output_pages.append(response)
        return output_pages

    def ask_debug(self, prompt):
        prompt_pages = self._paginate_input(prompt)
        return prompt_pages

