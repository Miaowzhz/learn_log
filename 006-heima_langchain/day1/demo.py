from pprint import pprint

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

agent = create_agent(
    "deepseek-v4-flash"
)

response = agent.invoke({
    "messages": [HumanMessage(content="今天郑州的天气怎么样？")],
})

pprint(response)


# 学习LangChain扩展学习视频
# 进度: 13-15