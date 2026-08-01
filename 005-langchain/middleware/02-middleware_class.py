from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langchain.messages import AIMessage
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.runtime import Runtime
from typing import Any
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from typing import Callable

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


# 环绕式钩子
class RetryMiddleware(AgentMiddleware):
    def __init__(self, max_retries: int = 3):
        super().__init__()
        self.max_retries = max_retries

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        for attempt in range(self.max_retries):
            try:
                return handler(request)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                print(f"Retry {attempt + 1}/{self.max_retries} after error: {e}")


agent = create_agent(
    model="deepseek:deepseek-v4-flash",
    system_prompt=SystemMessage("你是一个旅游规划小助手,请用言简意赅的语言帮我做简短的旅游规划。"),
    middleware=[RetryMiddleware()],
)

response = agent.invoke({"messages": HumanMessage("我想去东京。")})

print(response)