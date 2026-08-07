from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage

from step_03_agent import build_agent


def describe_message(message: BaseMessage) -> str:
    """把 Agent 状态中的一条消息转换成便于观察的文字。"""
    # 1: HumanMessage 返回“用户输入：{content}”。
    if isinstance(message, HumanMessage):
        return f"用户输入：{message.content}"

    # 2: 带有 tool_calls 的 AIMessage 返回工具调用列表。
    # 每个调用只保留 name 和 args，例如：
    # 模型决定调用工具：[{'name': '工具名', 'args': {...}}]
    if isinstance(message, AIMessage) and message.tool_calls:
        calls = [
            {
                "name": tool_call["name"],
                "args": tool_call["args"],
            }
            for tool_call in message.tool_calls
        ]
        return f"模型决定调用工具：{calls}"


    # 3: ToolMessage 返回“工具结果[{name}]：{content}”。
    if isinstance(message, ToolMessage):
        return f"工具结果[{message.name}]：{message.content}"

    # 4: 没有 tool_calls 的 AIMessage 返回“模型最终回答：{content}”。
    if isinstance(message, AIMessage) and not message.tool_calls:
        return f"模型最终回答：{message.content}"

    return f"未处理的消息类型：{type(message).__name__}"


def main() -> None:
    agent = build_agent()
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "我想用 7 天复习 LangChain，每天学习 45 分钟，请帮我制定计划。",
                }
            ]
        }
    )

    for index, message in enumerate(result["messages"], start=1):
        print(f"\n--- 第 {index} 条：{type(message).__name__} ---")
        print(describe_message(message))


if __name__ == "__main__":
    main()
