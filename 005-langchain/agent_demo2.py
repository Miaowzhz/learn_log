from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

agent = create_agent(model="deepseek:deepseek-v4-flash")

response = agent.invoke({"messages": HumanMessage("你好")})
print(response['messages'][1].content)