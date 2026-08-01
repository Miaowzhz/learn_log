from pprint import pprint
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import hook_config
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.tools import tool
from langgraph.runtime import Runtime
from typing import Any
from langchain.agents.middleware import AgentMiddleware


@tool
def search(param: str):
    """这是一个用来测试的工具"""
    return f"{param} 用来进行测试"


class AnswerCheckMiddleware(
    AgentMiddleware
):

    @hook_config(can_jump_to=["tools"])
    def before_model(
            self,
            state: AgentState,
            runtime: Runtime,
    ) -> dict[str, Any] | None:
        if not isinstance(state["messages"][-1], HumanMessage):
            return None


        return {
            "messages": [
                AIMessage(
                    content='',
                    id='lc_run--019fbd83-cc42-7eb0-a632-ddede41cdeac-0',
                    tool_calls=[
                        {
                            'name': 'search',
                            'args': {
                                'param': '北京'
                            },
                            'id': 'call_00_cMKkBsFh1AofhWgiToID7994',
                            'type': 'tool_call'
                        }
                    ]
                )
            ],
            # 跳转到工具节点
            "jump_to": "tools",
        }


agent = create_agent(
    model="deepseek:deepseek-v4-flash",
    system_prompt=SystemMessage("你是一个旅游规划小助手，可以帮我画旅游行程。。"),
    middleware=[AnswerCheckMiddleware()],
    tools=[search],
)

response = agent.invoke({"messages": HumanMessage("我想去成都玩一天。")})

pprint(response)