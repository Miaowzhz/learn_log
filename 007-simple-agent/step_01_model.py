import os

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage


def main() -> None:
    if not os.getenv("DEEPSEEK_API_KEY"):
        raise RuntimeError("请先设置 DEEPSEEK_API_KEY 环境变量")

    # 初始化模型
    model = init_chat_model(
        model="deepseek-v4-flash",
        model_provider="deepseek",
        temperature=0,
    )

    # 设置系统提示词
    messages = [
        SystemMessage("你是一个简洁、务实的学习规划助手"),
        HumanMessage("我想用 7 天复习 LangChain，每天 45 分钟")
    ]

    response = model.invoke(messages)
    print(response.content)


if __name__ == "__main__":
    main()
