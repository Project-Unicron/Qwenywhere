#!/usr/bin/env bash
# Step 1: Calculate 3 * 3 using the calculator tool
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are Qwenywhere. Use the calculator tool for math. Respond only with the result."},
      {"role": "user", "content": "What is 3 * 3?"}
    ],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "calculator",
          "description": "A simple calculator for math expressions.",
          "parameters": {
            "type": "object",
            "properties": {
              "expression": {"type": "string", "description": "Math expression to evaluate."}
            },
            "required": ["expression"]
          }
        }
      }
    ],
    "function_call": {"name": "calculator"},
    "chat_template_kwargs": {"enable_thinking": false}
  }' | jq
