import os
import requests
import json

API_URL = "https://api.deepseek.com/chat/completions"
MODEL_NAME = "deepseek-v4-flash"

MAX_TURNS = 4
def create_system_message() -> dict[str,str]:
    return {
        "role": "system",
        "content": ( "你是我的助手，请根据我的问题给出回答" 
                        "请根据上下文回答问题"
                        "请使用中文回答"
        )

    }
def trim_messages(messages:list[dict[str,str]],max_turns:int) -> list[dict[str,str]]:
    '''裁剪最近的对话历史，只保留max_turns轮'''
    if not messages:
        return messages
    system_message = messages[0]
    recent_messages = messages[1:]
    max_message_cnt = max_turns * 2
    if len(recent_messages) <= max_message_cnt:
        return messages
    return [system_message] + recent_messages[-max_message_cnt:]
def call_llm(api_key:str,messages:list[dict[str,str]]) -> str:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "max_tokens": 300,
        "temperature": 0.7,
        "thinking": {
            "type": "disabled"
        }
    }
    response = requests.post(API_URL, headers=headers, json = data, timeout = 30)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
if __name__ == "__main__":
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise SystemExit("请设置环境变量 DEEPSEEK_API_KEY")
    messages = [create_system_message()]
    print("Assistant: 你好，我是你的助手，请问我有什么可以帮你的？")
    while True:
        user_input = input("\n你: ").strip()
        if not user_input:
            print("请输入问题")
            continue
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("再见！")
            break
        messages.append({"role": "user", "content": user_input})
        trimmed_messages = trim_messages(messages, MAX_TURNS)
        try:
            response = call_llm(api_key, trimmed_messages)
            messages.append({"role": "assistant", "content": response})
            print("Assistant: ", response)
        except Exception as e:
            if len(messages) > 1 and messages[-1]["role"] == "user":
                messages.pop()
            continue
        messages.append({"role": "assistant", "content": response})
        messages = trim_messages(messages, MAX_TURNS)