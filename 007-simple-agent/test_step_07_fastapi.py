from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage

from step_07_fastapi import app, get_agent


class FakeAgent:
    def __init__(self):
        self.last_input = None
        self.last_config = None

    async def ainvoke(self, input_data, config):
        self.last_input = input_data
        self.last_config = config
        return {
            "messages": [
                AIMessage(content="这是测试回答"),
            ]
        }


def test_chat_passes_message_and_thread_id():
    fake_agent = FakeAgent()
    app.dependency_overrides[get_agent] = lambda: fake_agent

    try:
        with TestClient(app) as client:
            response = client.post(
                "/chat",
                json={
                    "thread_id": "test-thread-001",
                    "message": "我想学习 FastAPI",
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "thread_id": "test-thread-001",
        "answer": "这是测试回答",
    }
    assert fake_agent.last_input["messages"][0].content == "我想学习 FastAPI"
    assert (
        fake_agent.last_config["configurable"]["thread_id"]
        == "test-thread-001"
    )