import os

from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallRequest, ToolErrorMiddleware
from langchain.chat_models import init_chat_model

from study_agent.tools import calculate_study_budget, get_topic_outline


SYSTEM_PROMPT = """
你是一个严谨的学习规划助手。

规则：
1. 用户要求制定学习计划时，如果主题、学习天数或每天可用分钟数缺失，先追问，不得猜测。
2. 信息完整时，必须调用 calculate_study_budget 计算总学习时间。
3. 信息完整时，必须调用 get_topic_outline 查询主题大纲。
4. 只能根据工具返回的总时长和大纲制定计划，不得伪造资料、链接或额外知识点。
5. 计划必须覆盖用户指定的天数，安排的总时长不得超过工具计算结果。
6. 如果工具返回输入错误，不要用错误参数重试；请要求用户提供正确的正整数。
7. 如果主题不受支持，明确告知支持范围，不要自行补充该主题的学习计划。
""".strip()


def handle_tool_error(
    error: Exception,
    request: ToolCallRequest,
) -> str | None:
    """Convert expected input errors into safe tool feedback."""
    if isinstance(error, ValueError):
        return "学习天数和每天时长必须是正整数，请向用户确认正确参数。"
    return None


if not os.getenv("DEEPSEEK_API_KEY"):
    raise RuntimeError("请先设置 DEEPSEEK_API_KEY 环境变量")

model = init_chat_model(
    model="deepseek-v4-flash",
    model_provider="deepseek",
    temperature=0,
)

# Agent Server injects and manages persistence at runtime.
graph = create_agent(
    model=model,
    tools=[calculate_study_budget, get_topic_outline],
    system_prompt=SYSTEM_PROMPT,
    middleware=[ToolErrorMiddleware(on_error=handle_tool_error)],
)

