from openai import OpenAI
client = OpenAI()

def strip_code_fence(script: str) -> str:
    lines = script.strip().splitlines()

    # Remove first line if it's a markdown-style code block start
    if lines and lines[0].strip().startswith("```python"):
        lines = lines[1:]
    elif lines and lines[0].strip().startswith("'''python"):
        lines = lines[1:]

    # Remove last line if it's a markdown-style code block end
    if lines and lines[-1].strip() in ("```", "'''"):
        lines = lines[:-1]

    return "\n".join(lines)

def extract_python(prompt):
    response = client.responses.create(
        model="gpt-4.1",
        input=f"Extract the python code from the following response and return it only: \n {prompt}"
    )

    return strip_code_fence(response.output_text)

def code_func(prompt):
    response = client.responses.create(
        model="gpt-4.1",
        input=f"Write a Python function that does the following: {prompt} \n The only code in your response should be the function."
    )

    return response.output_text

def append_to_utils(script):
    with open("utils.py", "a", encoding="utf-8") as f:
        f.write('\n' + script + '\n')
    update_file_in_git("utils.py", "Added utility")


def append_to_logfile(filename, message):
    with open(filename, 'a') as f:
        f.write(message + '\n')

import subprocess

def update_file_in_git(file_path, commit_message):
    subprocess.run(["git", "add", file_path], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push"], check=True)

def pull_git(path):
    subprocess.run(["git", "fetch", "origin"], check=True),
    subprocess.run(["git", "origin/main", "--", path], check=True)
    

def estimate_gpt41_cost(input_text, output_text, input_rate=0.005, output_rate=0.015, model_token_per_dollar=1000):
    """
    Estimates the cost (in USD) for using GPT-4.1 with the given input and output strings.
    Default rates and context window based on OpenAI's 2024 GPT-4.1 pricing.
    - input_rate: $/1K input tokens (default $0.005)
    - output_rate: $/1K output tokens (default $0.015)
    Returns estimated cost as a float.
    """
    import tiktoken

    # Use the GPT-4 encoding
    enc = tiktoken.encoding_for_model("gpt-4")

    input_tokens = len(enc.encode(input_text))
    output_tokens = len(enc.encode(output_text))

    cost = (input_tokens / 1000) * input_rate + (output_tokens / 1000) * output_rate
    return cost


