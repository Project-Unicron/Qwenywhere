#!/bin/bash
set -e

# Dynamically select the best Qwen3 model for this system
source /app/script/select_model.sh

# Start Ollama in the background
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"
until curl -s "$OLLAMA_URL/api/tags" > /dev/null; do
  echo "Waiting for Ollama to start..."
  sleep 2
done

echo "Ollama is running."

# Unicorn-grade Qwenywhere banner
printf '\n   █ ▓ ▒  Q W E N Y W H E R E  ▒ ▓ █\n'
printf '        — Portable • Smart • Yours —\n'
printf '     — Now Running: %s —\n\n' "$OLLAMA_MODEL"

# API Endpoints and Tips
printf 'API Endpoints:\n'
printf '  • POST /v1/chat/completions   (OpenAI-compatible chat)
'
printf '  • [docs at] http://localhost:8000/docs\n'
printf '\nTips:\n'
printf '  • Use the /v1/chat/completions endpoint for chat, tool use, and code generation.\n'
printf '  • Try test_weather_time_chain.sh for a multi-tool agent demo.\n'
printf '  • System prompt and tool schemas can be set per request.\n'
printf '  • See README.md for more examples and usage.\n\n'

# Pull the selected model if not present
if ! ollama list | grep -q "$OLLAMA_MODEL"; then
  echo "Pulling $OLLAMA_MODEL model..."
  ollama pull "$OLLAMA_MODEL"
else
  echo "Model $OLLAMA_MODEL already present."
fi

# Start FastAPI app
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 