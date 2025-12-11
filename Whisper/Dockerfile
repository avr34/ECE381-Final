# Start with ggml-org's official whisper.cpp image
# It comes with curl and ffmpeg, and also compiled executable :D
#
# Most of the hard work here is done by whisper.cpp, very conveniently.
# All that we do is run a custom python wrapper.
FROM ghcr.io/ggml-org/whisper.cpp:main
WORKDIR /app

# Download weights
RUN curl -L -o models/ggml-small.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin

# Install python3 if we don't already have it
RUN apt update && apt install -y \
    vim \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    && apt clean

# Create venv, add venv to PATH, and install dependencies
RUN python3 -m venv .env
ENV PATH="/app/.env/bin/:$PATH"
RUN pip install --no-cache-dir \
    httpx \
    typing \
    fastapi \
    uvicorn \
    python-multipart

# Copy code directory
COPY ./shared-data /data

# Run server
WORKDIR /data/code
ENTRYPOINT ["python3"]
CMD ["./runWhisper.py", "/app/models/ggml-small.bin", "8080"]
