import os

from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallRequest, ToolErrorMiddleware
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from step_02_tools import calculate_study_budget, get_topic_outline
from step_03_agent import SYSTEM_PROMPT


FINAL_SYSTEM_PROMPT = f"""
{SYSTEM_PROMPT}
6. 如果工具返回输入错误，不要用错误参数重试；请要求用户提供正确的正整数。
7. 如果主题不受支持，明确告知支持范围，不要自行补充该主题的学习计划。
""".strip()


def handle_tool_error(
    error: Exception,
    request: ToolCallRequest,
) -> str | None:
    """只把预期的业务参数错误转换为安全的工具消息。"""
    # TODO 1: ValueError 返回不包含内部异常细节的用户可理解提示。
    if isinstance(error, ValueError):
        return "学习天数和每天时长必须是正整数，请向用户确认正确参数。"
    # 其他异常返回 None，让 LangChain 继续抛出。
    return None


def build_final_agent():
    if not os.getenv("DEEPSEEK_API_KEY"):
        raise RuntimeError("请先设置 DEEPSEEK_API_KEY 环境变量")

    model = init_chat_model(
        model="deepseek-v4-flash",
        model_provider="deepseek",
        temperature=0,
    )

    # TODO 2: 创建 ToolErrorMiddleware，并将 handle_tool_error 传给 on_error。
    tool_error_middleware = ToolErrorMiddleware(
        on_error=handle_tool_error,
    )

    # TODO 3: 创建最终 Agent：传入两个工具、系统提示词、中间件和 InMemorySaver。
    return create_agent(
        model=model,
        tools=[calculate_study_budget, get_topic_outline],
        system_prompt=FINAL_SYSTEM_PROMPT,
        checkpointer=InMemorySaver(),
        middleware=[tool_error_middleware]
    )


def main() -> None:
    agent = build_final_agent()
    config = {"configurable": {"thread_id": "cli-student-001"}}

    print("学习规划 Agent 已启动。输入“退出”结束会话。")

    while True:
        user_input = input("\n你：").strip()

        if user_input.lower() in {"退出", "exit", "quit"}:
            print("Agent：会话已结束。")
            break

        if not user_input:
            print("Agent：请输入你的学习需求。")
            continue

        # TODO 4: 只把本轮 user_input 作为一条 user 消息传给 agent.invoke，
        # 同时传入 config，然后打印最后一条消息的 content。
        result = agent.invoke(
            {"messages": HumanMessage(user_input)},
            config=config
        )
        print(f"Agent：{result['messages'][-1].content}")


if __name__ == "__main__":
    main()
