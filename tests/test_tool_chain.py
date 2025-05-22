import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_two_step_tool_call():
    """
    Minimal multi-turn tool call test: calculator tool, two sequential calls.
    """
    import uuid
    # Step 1: 3 * 3
    tool_call_id1 = str(uuid.uuid4())
    payload1 = {
        "model": "qwen3:1.7b",
        "messages": [
            {"role": "system", "content": "You are Qwenywhere. Use the calculator tool for math. Respond only with the result."},
            {"role": "user", "content": "What is 3 * 3?"},
            {"role": "assistant", "content": "", "tool_calls": [
                {"id": tool_call_id1, "function": {"name": "calculator", "arguments": {"expression": "3 * 3"}}}
            ]},
            {"role": "tool", "name": "calculator", "tool_call_id": tool_call_id1, "content": "Result of calculator: {\"result\": 9}"}
        ],
        "stream": False
    }
    response1 = client.post("/v1/chat/completions", json=payload1)
    assert response1.status_code == 200
    data1 = response1.json()
    assert "choices" in data1
    assert data1["choices"][0]["message"]["content"]
    assert "9" in data1["choices"][0]["message"]["content"]

    # Step 2: 10 / 2
    tool_call_id2 = str(uuid.uuid4())
    payload2 = {
        "model": "qwen3:1.7b",
        "messages": [
            {"role": "system", "content": "You are Qwenywhere. Use the calculator tool for math. Respond only with the result."},
            {"role": "user", "content": "What is 10 / 2?"},
            {"role": "assistant", "content": "", "tool_calls": [
                {"id": tool_call_id2, "function": {"name": "calculator", "arguments": {"expression": "10 / 2"}}}
            ]},
            {"role": "tool", "name": "calculator", "tool_call_id": tool_call_id2, "content": "Result of calculator: {\"result\": 5.0}"}
        ],
        "stream": False
    }
    response2 = client.post("/v1/chat/completions", json=payload2)
    assert response2.status_code == 200
    data2 = response2.json()
    assert "choices" in data2
    assert data2["choices"][0]["message"]["content"]
    assert "5" in data2["choices"][0]["message"]["content"]
