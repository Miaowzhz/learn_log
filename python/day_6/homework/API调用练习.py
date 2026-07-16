"""
API调用练习

需求：使用Python代码调用大模型API
思路：1) 获取API密钥 2) 编写HTTP请求 3) 处理响应数据
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": "你是Agent开发工程师"},
        {"role": "user", "content": "你是谁,你能帮我做什么"},
    ],
    stream=False,
)

print(response.choices[0].message.content)