#!/usr/bin/env bash
# Test basic chat completion
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Say hello!"}
    ]
  }' | jq
