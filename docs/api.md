# Qwenywhere API Reference

Welcome to the Qwenywhere API! This is not your average API reference. Here, we believe in rigorous technical detail, but also in Klingon stand-up comedy and the healing power of bananas.

## Endpoints

### POST `/v1/chat/completions`

Initiate a chat completion, with or without tool calls. Works with OpenAI-compatible payloads, but with more personality.

#### Request Body
```json
{
  "model": "qwen3:1.7b",
  "messages": [ ... ],
  "stream": false,
  "tools": [ ... ]
}
```

**Fields:**
- `model`: (string) The model to use. Qwen3 is the default, and it’s strong enough to arm-wrestle a GPU.
- `messages`: (array) The conversation history. See [Prompting & Persona Guide](./prompting.md).
- `stream`: (bool) If true, responses are streamed. If false, you get it all at once, like a banana split.
- `tools`: (array) Tool/function definitions. See [Tool Usage Guide](./tools.md).

#### Response
A JSON object with `choices`, `usage`, and (if applicable) `tool_outputs`. If the model is feeling funny, you’ll know.

### Example: Multi-Tool Call

**Request:**
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3:1.7b",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant who happens to be a stand up comedian from the klingon empire. You have access to two tools: get_weather and get_time_of_day. When you receive tool results as messages with role 'tool', you must always synthesize a final answer for the user using the information in those tool messages. Do not stop until you have given a final, natural language answer to the user."},
      {"role": "user", "content": "What is the weather and time of day for the banana planet?"},
      {"role": "assistant", "content": "", "tool_calls": [
        {"id": "call-weather-1", "function": {"name": "get_weather", "arguments": {}}},
        {"id": "call-time-1", "function": {"name": "get_time_of_day", "arguments": {}}}
      ]},
      {"role": "tool", "name": "get_weather", "tool_call_id": "call-weather-1", "content": "Result of get_weather: {\"weather\": \"peel storm\"}"},
      {"role": "tool", "name": "get_time_of_day", "tool_call_id": "call-time-1", "content": "Result of get_time_of_day: {\"time_of_day\": \"ripe noon\"}"}
    ],
    "stream": false
  }'
```

**Response:**
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "On the banana planet, it's a peel storm at ripe noon. Qapla'!"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": { ... },
  "tool_outputs": [ ... ]
}
```

---

## Error Codes
- 422: You sent something so wild, even the banana planet can’t parse it. Check your roles and fields.
- 500: Too many tool call iterations. The model is lost in the produce aisle.

---

For more, see [Prompting & Persona Guide](./prompting.md), [Tool Usage Guide](./tools.md), or just ask the model something silly.
