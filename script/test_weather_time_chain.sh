#!/usr/bin/env bash
set -e
# Multi-step agentic tool use test: weather + time of day
# This script does NOT modify the system prompt file. It is a standalone test.

curl --max-time 30 -N -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "stream": true,
  "messages": [
    {"role": "system", "content": "You are Qwenywhere. You have access to two tools: get_weather (returns the current weather as a string) and get_time_of_day (returns the current part of the day: morning, afternoon, night, etc). When asked about the weather today, use both tools and combine their results to answer in natural language, e.g., 'It's a cloudy night'."},
    {"role": "user", "content": "What's the weather today?"}
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Returns the current weather as a string.",
        "parameters": {
          "type": "object",
          "properties": {},
          "required": []
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "get_time_of_day",
        "description": "Returns the current part of the day (morning, afternoon, night, etc).",
        "parameters": {
          "type": "object",
          "properties": {},
          "required": []
        }
      }
    }
  ],
  "tool_choice": "auto"
}
EOF
