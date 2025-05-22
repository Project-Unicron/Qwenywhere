#!/usr/bin/env bash
# Test tool/function call (calculator)
# Requires jq for pretty-printing JSON
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is 2 + 2?"}
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
    ]
  }' | jq
