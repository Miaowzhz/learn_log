from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.runnables import Runnable
from langgraph.config import get_stream_writer
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """获取某个城市的天气"""
    writer = get_stream_writer()
    # stream any arbitrary data
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")
    return f"这里总是阳光明媚 {city}!"

agent: Runnable = create_agent(
    model="deepseek-v4-flash",
    tools=[get_weather],
)

stream = agent.stream_events(
    {"messages": [HumanMessage("北京天气怎么样？")]},
    version="v3",
) 
for message in stream.messages:
    for token in message.reasoning:
        print(f"[思考] {token}", end="")
    for token in message.text:
        print(token, end="", flush=True)