# Qwenywhere: Current State (as of 2025-05-21)

## Overview
Qwenywhere is a lightweight, hardware-adaptive local agent distribution for running Qwen3 LLMs via Ollama, with a focus on clean, production-grade code and minimal configuration. The system is designed to run on a wide range of hardware, from low-power devices to business workstations, automatically selecting the optimal model size for the host.

---

## Key Features
- **OpenAI-compatible FastAPI proxy** for Qwen3 models via Ollama
- **Dynamic model selection** at startup (GPU VRAM, RAM, CPU cores)
- **.env-based configuration** with override support
- **Dockerized deployment**
- **Minimal, Pythonic, testable codebase**
- **Ultra-conservative fallback:** Always runs at least qwen3:0.6b

---

## Dynamic Model Selection Logic
- On startup, `select_model.sh` detects:
  - GPU VRAM (if present)
  - System RAM
  - CPU core count
- Selects the largest Qwen3 model the system can handle:
  - **GPU present:** up to 235b, based on VRAM
  - **CPU-only:** never selects >4b; core/RAM thresholds for 0.6b, 1.7b, 4b
- **Override:** If `OLLAMA_MODEL` is set in `.env`, it is used directly and all checks are skipped.
- Always falls back to `qwen3:0.6b` for ultra-low spec systems (no refusal to run).

---

## Configuration
- `.env` supports:
  - `OLLAMA_URL` (default: http://localhost:11434)
  - `OLLAMA_MODEL` (optional, to force a model)
- All config loaded via `python-dotenv` and respected by both the FastAPI app and startup scripts.

---

## Docker Entrypoint Flow
1. Call `select_model.sh` to set `OLLAMA_MODEL`
2. Start Ollama in the background
3. Wait for Ollama to be ready
4. Pull the selected model if not present
5. Start the FastAPI server

---

## Codebase Structure
- `app/main.py` — FastAPI OpenAI-compatible API
- `app/test_main.py` — Unit tests (pytest)
- `intake.py` — Interview/test CLI utility
- `entrypoint.sh` — Docker entrypoint, runs model selection and server
- `select_model.sh` — Hardware-aware model selection logic
- `.env` / `example.env` — Config
- `system.txt` — System prompt and coding priorities
- `docs/` — Documentation

---

## Coding Philosophy
- See `system.txt` for the full system prompt and coding priorities
- Emphasis on readability, explicitness, separation of concerns, and minimal dependencies

---

## Next Steps / TODO
- Add more robust and granular tests
- Optionally refine model selection (e.g., ARM vs x86 detection)
- Expand documentation (usage, troubleshooting, benchmarks)
- Add health check endpoints and improved error handling

---

_Last updated: 2025-05-21_
