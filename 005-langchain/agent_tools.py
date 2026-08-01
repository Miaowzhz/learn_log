from pprint import pprint
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(model="deepseek:deepseek-v4-flash", tools=[search])
response = agent.invoke({"messages": HumanMessage("帮我查询北京的天气")})
pprint(response)
