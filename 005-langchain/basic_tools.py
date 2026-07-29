import os

from langchain.chat_models import init_chat_model
from langchain.tools import tool

api_key = os.getenv("DEEPSEEK_API_KEY")
llm = init_chat_model(
    model="deepseek-v4-flash",
    api_key=api_key,
    temperature=0.7,
    max_tokens=1024,
    timeout=20, # 秒
    max_retries=2, # 最大重试次数
    extra_body={"thinking": {"type": "disabled"}}
)

@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."

@tool
def search(location: str) -> str:
    """Search the web for information."""
    return f"{location} 的搜索结果。"



# # 将（可能多个）工具绑定到模型
# model_with_tools = llm.bind_tools([get_weather])
#
# # 第1步：模型生成工具调用
# messages = [{"role": "user", "content": "波士顿的天气怎么样？"}]
# ai_msg = model_with_tools.invoke(messages)
# print(f"第一步: {ai_msg}")
# messages.append(ai_msg)
#
# # 第2步：执行工具并收集结果
# for tool_call in ai_msg.tool_calls:
#     # 使用生成的参数执行工具
#     tool_result = get_weather.invoke(tool_call)
#     messages.append(tool_result)
#
# # 第3步：将结果传回模型，生成最终回复
# final_response = model_with_tools.invoke(messages)
# print(final_response.text)
# # "波士顿当前天气晴朗，气温72°F。"

# 强制工具调用
# model_with_tools = llm.bind_tools([get_weather, search], tool_choice="search")
# res = model_with_tools.invoke("重庆今天天气怎么样?")
# print(res.tool_calls)

# 并行工具调用
#
# response = model_with_tools.invoke(
#     "What's the weather in 上海 and 北京?"
# )
#
#
# # The model may generate multiple tool calls
# print(response.tool_calls)
# # [
# #   {'name': 'get_weather', 'args': {'location': 'Boston'}, 'id': 'call_1'},
# #   {'name': 'get_weather', 'args': {'location': 'Tokyo'}, 'id': 'call_2'},
# # ]
#
#
# # Execute all tools (can be done in parallel with async)
# results = []
# for tool_call in response.tool_calls:
#     if tool_call['name'] == 'get_weather':
#         result = get_weather.invoke(tool_call)
#     ...
#     results.append(result)
#
# print(results)


# 流媒体工具调用

model_with_tools = llm.bind_tools([get_weather])

for chunk in model_with_tools.stream(
    "What's the weather in Boston and Tokyo?"
):
    # Tool call chunks arrive progressively
    for tool_chunk in chunk.tool_call_chunks:
        if name := tool_chunk.get("name"):
            print(f"Tool: {name}")
        if id_ := tool_chunk.get("id"):
            print(f"ID: {id_}")
        if args := tool_chunk.get("args"):
            print(f"Args: {args}")