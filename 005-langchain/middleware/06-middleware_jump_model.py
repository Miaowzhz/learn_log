from pprint import pprint

from langchain.agents import create_agent
from langchain.agents.middleware import AgentState, hook_config
from langchain.messages import AIMessage
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.runtime import Runtime
from typing import Any, NotRequired
from langchain.agents.middleware import AgentMiddleware

# class MessageLimitMiddleware(AgentMiddleware):
#     def __init__(self, max_messages: int = 1):
#         super().__init__()
#         self.max_messages = max_messages
#
#     @hook_config(can_jump_to=["end"])
#     def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
#         print("before model!!!!!")
#         if len(state["messages"]) >= self.max_messages:
#             return {
#                 "messages": [AIMessage("Conversation limit reached.")],
#                 "jump_to": "end"
#             }
#         return None
#
#     def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
#         print(f"after model")
#         return None



class AnswerCheckState(AgentState):
    """Agent state: trace_layer uses last-wins (outer overwrites inner), messages use additive reducer."""
    # 记录已经要求模型回答的次数
    trace_layer: NotRequired[int]


class AnswerCheckMiddleware(
    AgentMiddleware[AnswerCheckState]
):
    state_schema = AnswerCheckState

    @hook_config(can_jump_to=["model"])
    def after_model(
            self,
            state: AnswerCheckState,
            runtime: Runtime,
    ) -> dict[str, Any] | None:
        last_message = state["messages"][-1]
        rewrite_count = state.get("trace_layer", 0)

        # 只检查模型生成的消息
        if not isinstance(last_message, AIMessage):
            return None

        answer = last_message.text

        # 回答少于50个字符,并且还没有重新生成过
        if len(answer) > 50 and rewrite_count < 1:
            return {
                "messages": [
                    HumanMessage(
                        "刚才的回答过于冗余."
                        "言简意赅的回答。."
                    )
                ],
                # 更新重新回答次数
                "rewrite_count": rewrite_count + 1,
                # 跳转到模型节点
                "jump_to": "model",
            }

        return None



agent = create_agent(
    model="deepseek:deepseek-v4-flash",
    system_prompt=SystemMessage("是一个数学老师。"),
    middleware=[AnswerCheckMiddleware()],
    state_schema=AnswerCheckState,
)

response = agent.invoke({"messages": HumanMessage("给我讲解一下乘法的逻辑。")})

pprint(response)