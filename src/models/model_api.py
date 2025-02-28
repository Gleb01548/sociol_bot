import requests

import yaml
from openai import OpenAI

with open("conf.yaml") as fh:
    config = yaml.load(fh, Loader=yaml.FullLoader)


headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {config["token_minmax"]}",
}
url = "https://api.minimaxi.chat/v1/text/chatcompletion_v2"


def use_min_max(system_prompt, message):
    data = {
        "model": "MiniMax-Text-01",
        "messages": [
            {
                "role": "system",
                "name": "MM Intelligent Assistant",
                "content": system_prompt,
            },
            {"role": "user", "name": "user", "content": message},
        ],
    }
    response = requests.post(url, headers=headers, json=data).json()
    return response["choices"][0]["message"]["content"]


client = OpenAI(api_key=config["token_deepseek"], base_url="https://api.deepseek.com")


def use_deepseek(system_prompt, message):
    return (
        client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            stream=False,
        )
        .choices[0]
        .message.content
    )
