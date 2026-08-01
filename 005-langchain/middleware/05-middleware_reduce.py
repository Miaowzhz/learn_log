from pprint import pprint
from typing import Annotated, Callable

from langchain.agents import create_agent
from langchain.agents.middleware import (
    AgentMiddleware,
    AgentState,
    ExtendedModelResponse,
    ModelRequest,
    ModelResponse,
    wrap_tool_call
)
from langchain.messages import SystemMessage
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from typing_extensions import NotRequired


def _last_wins(_a: str, b: str) -> str:
    """Reducer: last writer wins (outer overwrites inner)."""
    print(f"_a: {_a}, b: {b}")
    return b


class CustomMiddlewareState(AgentState):
    """Agent state: trace_layer uses last-wins (outer wins), messages use additive reducer."""

    # Non-reducer field with last-wins: both middleware write; outermost value wins
    trace_layer: NotRequired[Annotated[str, _last_wins]]


class OuterMiddleware(AgentMiddleware):
    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ExtendedModelResponse:
        pprint("OuterMiddleware before")
        response = handler(request)
        pprint("OuterMiddleware after")
        return ExtendedModelResponse(
            model_response=response,
            command=Command(update={
                "trace_layer": "outer",
                "messages": [SystemMessage(content="[Outer ran]")],
            }),
        )


class InnerMiddleware(AgentMiddleware):
    """Adds trace_layer and message. Outer adds to same keys; trace_layer: outer wins, messages: additive."""

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ):
        pprint("InnerMiddleware before")
        response = handler(request)
        pprint("InnerMiddleware after")
        return ExtendedModelResponse(
            model_response=response,
            command=Command(update={
                "trace_layer": "inner",
                "messages": [SystemMessage(content="[Inner ran]")],
            }),
        )

agent = create_agent(
    model="deepseek:deepseek-v4-flash",
    system_prompt=SystemMessage("你是一个旅游规划小助手,请用言简意赅的语言帮我做简短的旅游规划。"),
    middleware=[ OuterMiddleware(),InnerMiddleware() ],
    state_schema=CustomMiddlewareState,
)

response = agent.invoke({
    "messages": HumanMessage("我想去东京。")
})

pprint(response)