# ask_chatgpt

This small Python project allows you to send chat messages to ChatGPT using OpenAI's API from your command line.

## Requirements

- Python >= 3.11.0
- openai python module
- A valid OpenAI API key

:warning: **Important:** Using the OpenAI API has costs associated with it. To avoid spending too much, you can:

1. Set a rate limit on your API key to control usage.
2. Monitor your usage and set alerts in the OpenAI dashboard.
3. Always test your code with a small number of requests before scaling up.

## Getting Started

### Configuring Basic Settings

The project comes with an example configuration file, `config.toml.example`. To set up your basic settings, follow these steps:

1. Open the `config.toml.example` file and fill in the required values:
```toml
[openai]
api_key = "sk-XXXXXXXXXXXXX"
model = "gpt-3.5-turbo"
max_tokens = 1500
```
Replace `sk-XXXXXXXXXXXXX` with your actual OpenAI API key.

2. Save the file as `config.toml` in the same directory as the main solution.
The project will now use the values from config.toml for its settings. Make sure not to share your config.toml file or API key with others, as this could lead to unauthorized usage and increased costs.

### Setting up a Virtual Environment

1. Make sure you have Python 3.11.0 or higher installed.
2. Create a virtual environment using the `venv` module:
`python -m venv venv`
3. Activate the virtual environment:
- **Windows:** `.\venv\Scripts\activate`
- **macOS/Linux:** `source venv/bin/activate`
4. Install the dependencies:
`pip install -r requirements.txt`

### Using the Bash Script Wrapper

1. Add the following Bash script to your path, and name it `ask_chatgpt.sh`:
```bash
#!/bin/bash
    
dir_base="ADD HERE THE FULL PATH TO THE LOCATION YOU SAVED THIS PROJECT"
   
prompt="${1}"
if [[ -z ${prompt} ]]; then
    prompt="$(cat -)"
fi
source ${dir_base}/venv/bin/activate
python ${dir_base}/ask_chatgpt.py "${prompt}"
deactivate
exit 0
```
2. Make the script executable:
`chmod +x ask_chatgpt.sh`
3. Add the script to your system's `PATH`.

### Usage Example
You can now use the `ask_chatgpt.sh` script to send prompts to ChatGPT. To send a prompt directly:

```bash
ask_chatgpt.sh "What's the weather like today?"
```

Or you can pipe the output of another command to `ask_chatgpt.sh`:
```bash
echo "What's the weather like today?" | ask_chatgpt.sh
```
