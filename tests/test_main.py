import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_minimal_single_tool_call():
    """
    Minimal test for Qwen3 function calling with a single tool call and explicit tool_call_id.
    """
    import uuid
    tool_call_id = str(uuid.uuid4())
    system_prompt = (
        "You are Qwenywhere. You have access to the tool get_weather (returns the current weather as a string). "
        "When you receive tool results as messages with role 'tool', you must always synthesize a final answer for the user using the information in those tool messages. "
        "Do not stop until you have given a final, natural language answer to the user."
    )
    payload = {
        "model": "qwen3:1.7b",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "What's the weather today?"},
            {"role": "assistant", "content": "", "tool_calls": [
                {"id": tool_call_id, "function": {"name": "get_weather", "arguments": {}}}
            ]},
            {"role": "tool", "name": "get_weather", "tool_call_id": tool_call_id, "content": "Result of get_weather: {\"weather\": \"cloudy\"}"}
        ],
        "stream": False
    }
    response = client.post("/v1/chat/completions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "choices" in data
    assert data["choices"][0]["message"]["content"]
    assert "weather" in data["choices"][0]["message"]["content"].lower() or "cloudy" in data["choices"][0]["message"]["content"].lower()