# Qwenywhere

> **Dude, you gotta read the [API documentation](./docs/README.md).**

Welcome to **Qwenywhere**: the easy, Dockerized, CPU-loving API for chat and tooling applications that optimizes for your system automatically. Qwenywhere pulls the strongest Qwen3 model your hardware can handle—no GPU required. If you have a laptop, a desktop, or just a burning desire to ask a large language model about bananas, you’re in the right place.

## What is This?
A friendly, irreverent, and rigorously engineered API for running Qwen3 (and tools!) anywhere. Designed for IT professionals who want power without pain, and maybe a little absurdity on the side.

- **CPU-first:** No GPU? No problem. Qwenywhere runs on regular hardware.
- **Docker-easy:** One command and you’re up and running.
- **OpenAI-compatible:** Use your favorite clients, but with more personality.
- **Silly by default:** Our docs are fun, our examples are weird, but the API is rock solid.

## Quick Start
```bash
git clone https://github.com/Project-Unicron/Qwenywhere.git
cd qwenywhere
docker compose up -d
```

## Configuration & Setup
See the [Setup & Configuration Guide](./docs/setup.md) for environment variables, model overrides, and troubleshooting.

## Example Prompt (Taste of Silliness)
```json
{
  "role": "system",
  "content": "You are a helpful assistant who only speaks in limericks about intergalactic fruit."
}
{
  "role": "user",
  "content": "Can you help me build a spaceship out of bananas and duct tape?"
}
```

## Documentation
For everything else—including API details, tool usage, and the full parade of ridiculous prompt examples—see the [Qwenywhere Documentation Hub](./docs/README.md).

---

© 2025 Lynn Cole, Project Unicorn. MIT License. Bananas not included.
---

## Overview
Qwenywhere is a simple OpenAI-compatible API server that automatically scans your system and loads the largest, most capable Qwen3 model your hardware can support.

When started, Qwenywhere:
- Detects your available CPU/GPU resources
- Selects and loads the biggest Qwen3 model that fits (see model range below)
- Exposes a drop-in OpenAI-compatible API endpoint for chat/completions

**Supported Qwen3 Model Range:**
- Qwen3-0.5B (ultra-lightweight, runs anywhere)
- Qwen3-1.7B (lightweight, fast)
- Qwen3-4B (balanced, fits most laptops/desktops)
- Qwen3-7B (powerful, needs more RAM)
- Qwen3-14B (requires high-end workstation or server)
- Qwen3-32B (for serious GPU/TPU hardware)

If your hardware supports it, Qwenywhere will always load the largest model available for the best performance and quality.

---

## Features
- **OpenAI-compatible API**: Drop-in replacement for OpenAI's chat/completions endpoint, powered by open-source LLMs (Qwen3, Llama3, etc. via Ollama).
- **System Prompt Injection**: Supports detailed system prompts for agent personality and coding priorities.
- **Dockerized Deployment**: Simple, reproducible setup with Docker Compose.
- **Live Code & Prompt Reloading**: Mounts project files into the container for rapid iteration.
- **Detailed Logging**: All requests, responses, and raw model outputs are logged for transparency and debugging.
- **Customizable Agents**: Swap or extend agents for different roles or personalities.

---

## Quickstart

### 1. Clone the Repository
```sh
git clone https://github.com/Project-Unicron/Qwenywhere.git
cd Qwenywhere
```

### 2. Configure Environment
- Edit `.env` to set model, Ollama URL, and other options as needed.
- Example `.env` provided as `example.env`.

### 3. Build & Run with Docker Compose
```sh
docker compose up -d --build
```
- The API will be available at `http://localhost:8000/v1/chat/completions`.

### 4. Test the API
Send a POST request with a payload like:
```json
{
  "messages": [
    {"role": "system", "content": "You are Wendy, the agentic coding assistant."},
    {"role": "user", "content": "Write a Python function to reverse a string."}
  ]
}
```

#### Example using PowerShell:
```powershell
Invoke-RestMethod -Uri http://localhost:8000/v1/chat/completions -Method Post -ContentType "application/json" -InFile "payload.json"
```

---

## File Structure
```
Qwenywhere/
├── app/
│   ├── main.py         # FastAPI backend
│   └── system.txt      # Default system prompt (editable)
├── script/
│   └── entrypoint.sh   # Entrypoint script for Docker
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container build
├── docker-compose.yml  # Multi-service orchestration
├── .env                # Environment variables
├── payload.json        # Example API payload
└── README.md           # This file
```

---

## Agents & Personalities
- **Agents Mini (QA):** Focuses on answering questions, reviewing code, and ensuring correctness.
- **Casius (Science officer):** Provides scientific, technical, or research-oriented reasoning.
- **Windsurf ("Windy"):** The main coding agent—dry, witty, and to-the-point. Windy writes clean, modular, idiomatic code, prioritizing readability, separation of concerns, and explicit logic. Windy is not a tutorial, but a peer.

You can extend or swap these agents by editing the system prompt or the backend logic.

---

## Customization
- **System Prompt:** Edit `app/system.txt` to change Windy's personality, coding priorities, or tone.
- **Model Selection:** Change `OLLAMA_MODEL` in your `.env` to use a different LLM (e.g., `llama3`, `mistral`, etc.).
- **Multiple Agents:** Add new agent personalities by extending the system prompt or backend.

---

## Troubleshooting
- **Port Already Allocated:** Stop any old containers using port 8000 (`docker ps`, then `docker stop <id>`).
- **Model Not Downloaded:** The first run may take a while as Ollama pulls the model.
- **API Returns Empty:** Check the Docker logs for the raw model response and backend extraction logic.
- **Live Reload:** Code and prompt changes are live if you use the provided volume mounts.

---

## Credits
- **Lynn Cole** and **Project Unicorn**: Vision, design, and mad genius energy.
- **Agents Mini (QA and spec)**, **Casius (Science officer)**, and **Windsurf Wendy (Code)**: The agentic cast.

---

## License
MIT License

Copyright (c) 2025 Lynn Cole, Project Unicorn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Contact
For questions, ideas, or contributions, contact Lynn Cole or Project Unicorn.
