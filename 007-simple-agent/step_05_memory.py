import os

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from step_02_tools import calculate_study_budget, get_topic_outline
from step_03_agent import SYSTEM_PROMPT


def build_memory_agent():
    if not os.getenv("DEEPSEEK_API_KEY"):
        raise RuntimeError("请先设置 DEEPSEEK_API_KEY 环境变量")

    model = init_chat_model(
        model="deepseek-v4-flash",
        model_provider="deepseek",
        temperature=0,
    )

    # 1: 创建内存检查点存储器 InMemorySaver。
    checkpointer = InMemorySaver()

    # 2: 创建 Agent，并通过 checkpointer 参数接入检查点存储器。
    return create_agent(
        model=model,
        tools=[calculate_study_budget, get_topic_outline],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )


def main() -> None:
    agent = build_memory_agent()

    # 3: 创建 config，在 configurable 中设置 thread_id="student-001"。
    config = {
        "configurable": {
            "thread_id": "student-001",
        }
    }

    first_result = agent.invoke(
        {"messages": [{"role": "user", "content": "我想复习 FastAPI。"}]},
        config=config,
    )
    print("\n第一轮回答：")
    print(first_result["messages"][-1].content)

    second_result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": "安排 5 天，每天学习 30 分钟。"}
            ]
        },
        config=config,
    )
    print("\n第二轮回答：")
    print(second_result["messages"][-1].content)

    human_messages = [
        message.content
        for message in second_result["messages"]
        if isinstance(message, HumanMessage)
    ]
    print("\n该线程中的用户消息：")
    for message in human_messages:
        print(f"- {message}")


if __name__ == "__main__":
    main()
