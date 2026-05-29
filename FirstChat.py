import os
import requests
import json

API_URL = "https://api.deepseek.com/chat/completions"
MODEL_NAME = "deepseek-v4-flash"

def build_message() -> list[dict[str,str]]:
    return [
        {
            "role": "system",
            "content": "你是我的助手，请根据我的问题给出回答"
        },
        {
            "role": "user",
            "content": "请你用一句话介绍一下Python"
        }
    ]
def call_llm(api_key:str,messages:list[dict[str,str]]) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "max_tokens": 200,
        "thinking": {
            "type": "enabled"
        }
    }
    response = requests.post(API_URL, headers=headers, json = data, timeout = 30)
    response.raise_for_status()
    return response.json()
if __name__ == "__main__":
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise SystemExit("请设置环境变量 DEEPSEEK_API_KEY")
    messages = build_message()
    print(json.dumps(messages,ensure_ascii=False))
    response = call_llm(api_key, messages)
    print("answer:")
    print(response["choices"][0]["message"]["content"])
    print("usage:")
    print(json.dumps(response.get("usage"),indent=2,ensure_ascii=False))