import os
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import init_chat_model
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI

api_key = os.getenv("DEEPSEEK_API_KEY")


# llm = ChatOpenAI(
#     model="deepseek-v4-flash",
#     api_key=api_key,
#     temperature=0.7,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     base_url="https://api.deepseek.com"
# )

llm = init_chat_model(
    model="deepseek-v4-flash",
    api_key=api_key,
    temperature=0.7,
    max_tokens=1024,
    timeout=20, # 秒
    max_retries=2, # 最大重试次数
)

# llm = ChatDeepSeek(
#     model="deepseek-v4-flash",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     # other params...
# )

# conversation = [
#     {"role": "system", "content": "你是一个旅游规划小助手, 最多输出 200 个字"},
#     {"role": "user", "content": "我想去天津玩一天"},
#     {"role": "assistant", "content": "天津太热了, 别去了"},
#     {"role": "user", "content": "我想去武汉玩一天"}
# ]


conversation = [
    SystemMessage("你是一个旅游规划小助手, 最多输出 200 个字"),
    HumanMessage("我想去天津玩一天"),
    AIMessage("天津太热了, 别去了"),
    HumanMessage("我想去武汉玩一天")
]

messages = [
    (
        "system",
        "你是一个旅游规划小助手"
    ),
    ("human", "我想去郑州玩"),
]
# ai_msg = llm.invoke(conversation)
# print(ai_msg.content)

for chunk in llm.stream(conversation):
    print(chunk.content)