# Setup & Configuration

Welcome to the Setup & Configuration guide. If you can read this, you’re already halfway to running Qwenywhere. (The other half is mostly waiting for Docker to pull some very large files.)

## Requirements
- Docker
- A computer (CPU is fine! No GPU required, but if you have one, the model will still be polite.)
- A sense of adventure

## Quick Start
```bash
git clone https://github.com/your-org/qwenywhere.git
cd qwenywhere
docker compose up -d
```

## Configuration
- Edit `.env` to set your model (e.g., `OLLAMA_MODEL=qwen3:1.7b`).
- By default, Qwenywhere will optimize for your system and pull the strongest Qwen3 model your hardware can handle.
- For CPU-only systems, you’re in luck: this is what Qwenywhere was made for.

## Overrides
- You can override most settings in `.env`.
- Want to try a different model? Change `OLLAMA_MODEL`.
- Need to use a different port? Change `PORT`.

## Troubleshooting
- **Port Already Allocated:** Stop any old containers using port 8000 (`docker ps`, then `docker stop <id>`).
- **Model Not Downloaded:** The first run may take a while as Ollama pulls the model. Go make a sandwich.
- **API Returns Empty:** Check the Docker logs for the raw model response and backend extraction logic. If you see the word “banana” in the logs, you’re probably fine.
- **Live Reload:** Code and prompt changes are live if you use the provided volume mounts.

## FAQ
- **Do I need a GPU?** No! Qwenywhere is optimized for CPU use. Your laptop is a supercomputer (relatively speaking).
- **Can I use this for serious work?** Absolutely. But why be serious when you can be silly _and_ productive?
