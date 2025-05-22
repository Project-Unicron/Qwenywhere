# Tool Usage Guide

Welcome to the Qwenywhere Tool Usage Guide—where every function is a tool, and every tool is a potential punchline.

## What’s a Tool?
A tool is a function you define and expose to the model. When the model gets stuck, it calls a tool. Sometimes it does this to be helpful. Sometimes, just to see if you’re paying attention.

## Defining Tools
Tools are defined in your API payload under the `tools` field. Each tool is described by a name, description, and parameters (if any).

**Example:**
```json
"tools": [
  {
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Returns the current weather as a string.",
      "parameters": {"type": "object", "properties": {}, "required": []}
    }
  }
]
```

## Single Tool Call Example
See [API Reference](./api.md) for the full request, but here’s a snippet:

```json
{
  "role": "assistant",
  "content": "",
  "tool_calls": [
    {"id": "call-weather-1", "function": {"name": "get_weather", "arguments": {}}}
  ]
}
```

## Multi-Tool Call Example
Why stop at one? (See [API Reference](./api.md) for the full banana split.)

## Tool Results
When you get a tool call, respond with a `tool` message:
```json
{
  "role": "tool",
  "name": "get_weather",
  "tool_call_id": "call-weather-1",
  "content": "Result of get_weather: {\"weather\": \"cloudy\"}"
}
```

## Gotchas
- Always match `tool_call_id` to the `id` from the tool call.
- If you get lost, just remember: the banana is always in the last place you look.
