from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3.5:0.8b",
    temperature=0,
)

messages = [
    (
        "system",
        "你是一个旅游规划助手。",
    ),
    ("human", "我想去东京。"),
]
ai_msg = llm.invoke(messages)
print(ai_msg)