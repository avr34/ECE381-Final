# Start with ggml-org's official whisper.cpp image
# It comes with curl and ffmpeg, and also compiled executable :D
FROM ghcr.io/ggml-org/whisper.cpp:main
WORKDIR /

# Download weights
RUN curl -L -o /app/models/ggml-small.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin

# Run server
ENTRYPOINT ["whisper-server"]
CMD ["-m", "/app/models/ggml-small.bin", "--host", "0.0.0.0", "--convert"]
