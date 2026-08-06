import os

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from step_02_tools import calculate_study_budget, get_topic_outline


SYSTEM_PROMPT = """
你是一个严谨的学习规划助手。

规则：
1. 用户要求制定学习计划时，如果主题、学习天数或每天可用分钟数缺失，先追问，不得猜测。
2. 信息完整时，必须调用 calculate_study_budget 计算总学习时间。
3. 信息完整时，必须调用 get_topic_outline 查询主题大纲。
4. 只能根据工具返回的总时长和大纲制定计划，不得伪造资料、链接或额外知识点。
5. 计划必须覆盖用户指定的天数，安排的总时长不得超过工具计算结果。
""".strip()


def build_agent():
    if not os.getenv("DEEPSEEK_API_KEY"):
        raise RuntimeError("请先设置 DEEPSEEK_API_KEY 环境变量")

    # 使用 init_chat_model 初始化 deepseek-v4-flash。
    # 为减少输出随机性，把 temperature 设置为 0。
    model = init_chat_model(
        model="deepseek-v4-flash",
        model_provider="deepseek",
        temperature=0,
    )

    # 把两个工具放进 tools 列表。
    tools = [calculate_study_budget, get_topic_outline]

    # 使用 model、tools 和 SYSTEM_PROMPT 创建并返回 Agent。
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )
    return agent


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

    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
