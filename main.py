import openai
import datetime
import sys
import json

def init_openai():
    if len(sys.argv) < 2:
        print("Usage: python3 chatGPT.py <openai_api_key>")
        sys.exit(1)
    openai.api_key = sys.argv[1]

messages=[
        {"role": "system", "content": "一个专业的galgame乙女游戏对话设计师, 专注于设计游戏场景"},
]

def chat(text):
    global messages
    messages.append({"role": "user", "content": text})
    return openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )


def chat_with_gpt():
    print("Chat with GPT")
    with open("log.json", "r") as f:
        messages = json.load(f)
    print("\n".join((str(i) for i in messages)))
    # Chat with GPT
    while True:
        # Get user input
        now = datetime.datetime.now()
        d = f"{now.strftime('%Y-%m-%d %H:%M:%S')}"
        user_input = input(f"[{d}] User: ")
        if "全部确认删除" in user_input:
            print("清空对话记录")
            messages.clear()
        # Generate response
        response = chat(user_input)
        # Print response
        result = response.choices[0]['message']
        print(f"[{d}] {result['role']}: {result['content']}")    
        messages.append(result)
        with open("log.json", "w") as f:
            json.dump(messages, f)
        with open("log.txt", "a") as f:
            f.write(f"[{d}] User: {user_input}\n[{d}] {result['role']}: {result['content']}\n----------------------\n\n")

if __name__ == "__main__":
    init_openai()
    chat_with_gpt()