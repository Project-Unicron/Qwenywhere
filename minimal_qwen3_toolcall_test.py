import requests
import json

# Minimal test for Qwen3 function calling with tool messages
url = "http://localhost:8000/v1/chat/completions"
headers = {"Content-Type": "application/json"}

system_prompt = (
    "You are Qwenywhere. You have access to two tools: get_weather (returns the current weather as a string) "
    "and get_time_of_day (returns the current part of the day: morning, afternoon, night, etc). "
    "When you receive tool results as messages with role 'tool', you must always synthesize a final answer "
    "for the user using the information in those tool messages."
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What's the weather today?"},
    {"role": "assistant", "content": "", "tool_calls": [
        {"function": {"name": "get_weather", "arguments": {}}},
        {"function": {"name": "get_time_of_day", "arguments": {}}}
    ]},
    {"role": "tool", "name": "get_weather", "content": '{"weather": "cloudy"}'},
    {"role": "tool", "name": "get_time_of_day", "content": '{"time_of_day": "night"}'}
]

payload = {
    "model": "qwen3:1.7b",
    "messages": messages,
    "stream": False
}

response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
print("Status:", response.status_code)
print("Response:", response.text)
