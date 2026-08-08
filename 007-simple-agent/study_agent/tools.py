from langchain.tools import tool


TOPIC_OUTLINES = {
    "python": "语法与容器 -> 函数 -> 面向对象 -> 异常与模块 -> 综合练习",
    "fastapi": "路由与参数 -> Pydantic 模型 -> 依赖注入 -> 数据库 -> 测试与部署",
    "langchain": "模型与消息 -> 提示词 -> 工具 -> Agent -> 记忆与中间件",
}


@tool
def calculate_study_budget(days: int, minutes_per_day: int) -> str:
    """根据学习天数和每天可用分钟数，计算总学习时间。"""
    if days <= 0 or minutes_per_day <= 0:
        raise ValueError("天数和每天可用分钟数必须大于 0。")

    total_minutes = days * minutes_per_day
    return f"总学习时间：{total_minutes} 分钟（{days} 天 x {minutes_per_day} 分钟）"


@tool
def get_topic_outline(topic: str) -> str:
    """从本地知识库查询指定学习主题的大纲；只支持 Python、FastAPI 和 LangChain。"""
    original_topic = topic.strip()
    normalized_topic = original_topic.lower()

    if normalized_topic in TOPIC_OUTLINES:
        return TOPIC_OUTLINES[normalized_topic]

    display_topic = original_topic or "空主题"
    return f"暂不支持 {display_topic}；可选主题：Python、FastAPI、LangChain"

