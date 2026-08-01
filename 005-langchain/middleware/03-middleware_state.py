from pprint import pprint

from langchain.agents import create_agent
from langchain.agents.middleware import after_model, AgentState
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from typing import Any
from typing_extensions import NotRequired


@after_model()
def increment_after_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:

    pprint(state)

    return {"model_call_count": state.get("model_call_count", 0) + 1}

class TrackingState(AgentState):
    model_call_count: NotRequired[int]

agent = create_agent(
    model="deepseek:deepseek-v4-flash",
    system_prompt=SystemMessage("你是一个旅游规划小助手,请用言简意赅的语言帮我做简短的旅游规划。"),
    middleware=[increment_after_model],
    state_schema=TrackingState,
)

response = agent.invoke({
    "messages": HumanMessage("我想去东京。")
})

pprint(response)