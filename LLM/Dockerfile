# Start from python 3.13-slim base image, and
# set user to root
FROM python:3.12-slim AS builder
USER root

# Install required dependencies
RUN apt update && apt install -y \
    build-essential \
    git \
    wget \
    python3-dev \
    python3-pip \
    python3-venv \
    clang \
    cmake \
    && apt clean

# Set environment variables (for cmake)
ENV CMAKE_C_COMPILER=/usr/bin/clang
ENV CMAKE_CXX_COMPILER=/usr/bin/clang++

# Clone repository
RUN git clone --recursive https://github.com/microsoft/BitNet.git && rm -rf /BitNet/.git
WORKDIR /BitNet

# Create venv, install dependencies, as well as huggingface cli
RUN python3 -m venv .env
ENV PATH="/BitNet/.env/bin/:$PATH"
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -U "huggingface_hub[cli]"

# Use hf cli to download the bitnet 2B 4T weights, and
# Call setup_env.py to compile BitNet.cpp
#
# setup_env.py will call utils/codegen_t12.py (if on amd64), which generates C++ code.
# Then, setup_env.py will call cmake to compile the generated code.
# It also installs llama.cpp/gguf-py under 3rdparty, which is used to interact with the weights file (not sure how)
#
# Also it's being compiled for i2_s weight quantization, which is a custom 2 bit representation of weights.
# This allows 2 billion parameters to fit in just ~500 MB!!!
RUN hf download microsoft/BitNet-b1.58-2B-4T-gguf --local-dir models/BitNet-b1.58-2B-4T
RUN python3 setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s

# Make local directory available in container
COPY ./shared-data /data

# TODO rearrange these commands once the project is done
RUN apt install -y vim
RUN pip install --no-cache-dir fastapi uvicorn
COPY ./code /code

# Finally, run bash
CMD ["bash"]
