from pprint import pprint

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain_core.messages import HumanMessage, SystemMessage

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:

    # print("中间件")
    #
    # pprint(request)

    return handler(request.override(system_message=SystemMessage("你是一个翻译助手，能把我说的话全部转成英文。")))

agent = create_agent(
    model="deepseek:deepseek-v4-flash",
    system_prompt=SystemMessage("你是一个旅游规划小助手。"),
    middleware=[dynamic_model_selection]
)

response = agent.invoke({"messages": HumanMessage("我想去东京。")})
pprint(response)
