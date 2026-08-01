from pprint import pprint
from typing import Callable
from langgraph.prebuilt.tool_node import ToolCallRequest
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import (
    wrap_model_call,
    ModelRequest,
    ModelResponse,
    AgentState,
    ExtendedModelResponse, wrap_tool_call
)
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.types import Command
from typing_extensions import NotRequired

class UsageTrackingState(AgentState):
    """Agent state with token usage tracking."""

    last_model_call_tokens: NotRequired[int]


@wrap_model_call(state_schema=UsageTrackingState)
def track_usage(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ExtendedModelResponse:
    pprint(f"wrap_model_call {request.state.get('last_model_call_tokens')}")
    response = handler(request)
    return ExtendedModelResponse(
        model_response=response,
        command=Command(update={"last_model_call_tokens": 150}),
    )

@wrap_tool_call
def wrap_tool_call(request: ToolCallRequest,
                   handler: Callable[[ToolCallRequest], Command]
                   ) -> Command:
    pprint(f"wrap_tool_call {request.state.get('last_model_call_tokens')}")
    response = handler(request)
    return Command(update={
        "last_model_call_tokens": 300,
        "messages": [response]
    })


@tool
def search(location: str):
    """Search the information."""
    return f"{location} 的搜索结果。"

agent = create_agent(
    model="deepseek:deepseek-v4-flash",
    system_prompt=SystemMessage("你是一个旅游规划小助手,请用言简意赅的语言帮我做简短的旅游规划。"),
    middleware=[track_usage, wrap_tool_call],
    tools=[search],
)

response = agent.invoke({
    "messages": HumanMessage("我想去东京。")
})

pprint(response)