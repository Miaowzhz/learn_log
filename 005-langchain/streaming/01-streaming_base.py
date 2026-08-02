from pprint import pprint
from langchain.tools import tool
from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(
    model="deepseek-v4-flash",
    # extra_body={"thinking": {"type": "disabled"}}
)

@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"这个城市 {location} 的天气晴朗"

llm_with_tools = llm.bind_tools([get_weather])

reasoning_content = ""

llm_content = ""

tool_calls = []

response = llm_with_tools.stream("北京天气怎么样？")

for chunk in response:
    print(chunk)
    if chunk.additional_kwargs:
        reasoning_content += chunk.additional_kwargs.get("reasoning_content")

    if chunk.content:
        llm_content += chunk.content

    if chunk.tool_calls:
        for index, tool_call in enumerate(chunk.tool_calls):
            if tool_call["name"]: tool_calls.append({"tool_name": tool_call["name"]})

print(f"Agent正在思考: {reasoning_content}")
print(f"LLM正在生成: {llm_content}")
print(f"工具调用: {tool_calls}")
