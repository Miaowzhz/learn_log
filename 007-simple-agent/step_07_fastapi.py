import logging

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
load_dotenv()

from study_agent.graph import build_graph


fastapi_agent = build_graph(checkpointer=InMemorySaver())

def get_agent():
    return fastapi_agent

class ChatRequest(BaseModel):
    thread_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    thread_id: str
    answer: str

app = FastAPI(
    title="学习规划 Agent API",
    version="1.0.0",
)

@app.exception_handler(Exception)
async def handle_unexpected_error(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.error(
        "处理请求时发生未知异常：%s %s",
        request.method,
        request.url.path,
        exc_info=(type(exc), exc, exc.__traceback__),
    )

    return JSONResponse(
        status_code=500,
        content={"detail": "服务暂时不可用，请稍后重试"},
    )

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    agent=Depends(get_agent),
) -> ChatResponse:
    config = {
        "configurable": {
            "thread_id": request.thread_id,
        }
    }

    result = await agent.ainvoke(
        {
            "messages": [
                HumanMessage(content=request.message),
            ]
        },
        config=config,
    )

    final_message = result["messages"][-1]

    return ChatResponse(
        thread_id=request.thread_id,
        answer=final_message.content,
    )