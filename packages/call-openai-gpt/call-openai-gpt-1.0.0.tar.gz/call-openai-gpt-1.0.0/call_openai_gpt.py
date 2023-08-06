#!/usr/bin/env python
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"


def call_openai_gpt(prompt, model="gpt-4", temperature=0.1, max_tokens=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    messages = [
        {"role": "system", "content": prompt},
    ]

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens is not None:
        data["max_tokens"] = max_tokens
    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


def main():
    prompt = "你好!用繁體中文打招呼吧~"
    print(call_openai_gpt(prompt))


if __name__ == "__main__":
    main()
