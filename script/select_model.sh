#!/bin/bash
# Select the largest Qwen3 model that fits system resources
# Official model tags: 0.6b, 1.7b, 4b, 8b, 14b, 30b, 32b, 235b
# Reference: https://ollama.com/library/qwen3
#
# Approximate requirements (RAM or GPU VRAM):
#   0.6b  ~2GB
#   1.7b  ~4GB
#   4b    ~8GB
#   8b    ~16GB
#   14b   ~24GB
#   30b   ~40GB
#   32b   ~48GB
#   235b  ~142GB

# Allow override from environment/.env
if [ -n "$OLLAMA_MODEL" ]; then
    echo "OLLAMA_MODEL override detected: $OLLAMA_MODEL"
    export OLLAMA_MODEL
    # Do not exit; allow entrypoint to continue
fi

MODEL="qwen3:0.6b"  # Default to smallest

# Detect RAM in GB
TOTAL_MEM=$(awk '/MemTotal/ {printf "%.0f", $2/1024/1024}' /proc/meminfo)
# Detect CPU core count
CPU_CORES=$(nproc)

# Detect NVIDIA GPU (if present)
if command -v nvidia-smi &> /dev/null; then
    GPU_MEM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -n1)
    if [ "$GPU_MEM" -ge 142 ]; then
        MODEL="qwen3:235b"
    elif [ "$GPU_MEM" -ge 48 ]; then
        MODEL="qwen3:32b"
    elif [ "$GPU_MEM" -ge 40 ]; then
        MODEL="qwen3:30b"
    elif [ "$GPU_MEM" -ge 24 ]; then
        MODEL="qwen3:14b"
    elif [ "$GPU_MEM" -ge 16 ]; then
        MODEL="qwen3:8b"
    elif [ "$GPU_MEM" -ge 8 ]; then
        MODEL="qwen3:4b"
    elif [ "$GPU_MEM" -ge 4 ]; then
        MODEL="qwen3:1.7b"
    fi
else
    # CPU-only: never select models >4b
    if [ "$CPU_CORES" -ge 8 ] && [ "$TOTAL_MEM" -ge 8 ]; then
        MODEL="qwen3:4b"
    elif [ "$CPU_CORES" -ge 4 ] && [ "$TOTAL_MEM" -ge 4 ]; then
        MODEL="qwen3:1.7b"
    elif [ "$CPU_CORES" -ge 2 ] && [ "$TOTAL_MEM" -ge 2 ]; then
        MODEL="qwen3:0.6b"
    else
        MODEL="qwen3:0.6b"  # fallback for ultra-low spec
    fi
fi

export OLLAMA_MODEL="$MODEL"
echo "Selected OLLAMA_MODEL=$MODEL"

# Optionally, update .env (uncomment if you want to persist)
# sed -i "/^OLLAMA_MODEL=/c\OLLAMA_MODEL=$MODEL" /app/.env 2>/dev/null || true
