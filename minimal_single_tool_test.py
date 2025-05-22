import requests
import json
import uuid

# Minimal test for Qwen3 function calling with a single tool call and explicit tool_call_id
url = "http://localhost:8000/v1/chat/completions"
headers = {"Content-Type": "application/json"}

system_prompt = (
    "You are Qwenywhere. You have access to the tool get_weather (returns the current weather as a string). "
    "When you receive tool results as messages with role 'tool', you must always synthesize a final answer for the user using the information in those tool messages. "
    "Do not stop until you have given a final, natural language answer to the user."
)

# Generate a unique tool_call_id
tool_call_id = str(uuid.uuid4())

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What's the weather today?"},
    {"role": "assistant", "content": "", "tool_calls": [
        {"id": tool_call_id, "function": {"name": "get_weather", "arguments": {}}}
    ]},
    {"role": "tool", "name": "get_weather", "tool_call_id": tool_call_id, "content": "Result of get_weather: {\"weather\": \"cloudy\"}"}
]

payload = {
    "model": "qwen3:1.7b",
    "messages": messages,
    "stream": False
}

response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
print("Status:", response.status_code)
print("Response:", response.text)
