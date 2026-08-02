import asyncio

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
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

agent = create_agent(
    model="deepseek-v4-flash",
    tools=[get_weather],
)


# for chunk in agent.stream(
#     {"messages": [HumanMessage("北京的天气怎么样？")]},
#     stream_mode=["updates", "custom", "custom"],
#     version="v2",
# ):
#     print(chunk)
#     if chunk["type"] == "updates":
#         token, metadata = chunk["data"]
#         print(f"node: {metadata['langgraph_node']}")
#         print(f"content: {token.content_blocks}")
#         print("\n")


async def main():
    async for chunk in agent.astream(
        {"messages": [HumanMessage("北京的天气怎么样？")]},
        stream_mode=["updates", "messages", "custom"],
        version="v2",
    ):
        chunk_type = chunk["type"]
        data = chunk["data"]
        if chunk_type == "messages":
            token, metadata = data
            if getattr(token, "content", None):
                print(token.content, end="", flush=True)
            elif getattr(token, "additional_kwargs", None):
                print(token.additional_kwargs.get("reasoning_content"), end="", flush=True)
        elif chunk_type == "updates":
            print(f"\n updates:{data}")
        elif chunk_type == "custom":
            print(f"custom:{data}")


if __name__ == '__main__':
    asyncio.run(main())