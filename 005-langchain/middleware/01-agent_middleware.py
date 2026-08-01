from pprint import pprint
from typing import Callable
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_agent, before_model, after_agent, after_model, wrap_model_call, \
    wrap_tool_call, ModelRequest, ModelResponse
from langchain_core.messages import SystemMessage, ToolMessage, HumanMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.runtime import Runtime
from langchain.tools import tool


@before_agent
def before_agent(state: AgentState, runtime: Runtime):
    print("before_agent")

@before_model
def before_model(state: AgentState, runtime: Runtime):
    print("before_model")


@wrap_model_call
def wrap_model_call(request: ModelRequest,
                    handler: Callable[[ModelRequest], ModelResponse]
                    ) -> ModelResponse:
    print("wrap_model_call")
    response = handler(request)
    pprint(f"wrap_model_call, {response}")
    return response

@wrap_tool_call
def wrap_tool_call(request: ToolCallRequest,
                   handler: Callable[[ToolCallRequest], ToolMessage]
                   ) -> ToolMessage:
    print("wrap_tool_call")
    response = handler(request)
    pprint(f"wrap_tool_call, {response}")
    return response

@after_model
def after_model(state: AgentState, runtime: Runtime):
    print("after_model")
    return

@after_agent
def after_agent(state: AgentState, runtime: Runtime):
    print("after_agent")
    return

@tool
def search(location: str):
    """Search the location."""
    return f"{location} 的搜索结果。"

agent = create_agent(
    model="deepseek:deepseek-v4-flash",
    system_prompt=SystemMessage("你是一个旅游规划小助手,请用言简意赅的语言帮我做简短的旅游规划。"),
    middleware=[before_agent, before_model, wrap_model_call, wrap_tool_call, after_model, after_agent],
    tools=[search]
)

response = agent.invoke({"messages": HumanMessage("我想去东京。")})

print(response)