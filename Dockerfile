FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl git gcc make && \
    rm -rf /var/lib/apt/lists/*

# Install Ollama (CPU-only)
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python dependencies
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ ./app/
COPY script/ ./script/
COPY app/system.txt ./app/system.txt
RUN chmod +x ./script/entrypoint.sh ./script/select_model.sh

EXPOSE 8000
ENTRYPOINT ["/app/script/entrypoint.sh"]