# Start with ultralytics/ultralytics:latest-cpu base image
FROM ultralytics/ultralytics:latest-cpu

# Install dependencies
# RUN apt update && apt install -y \
#     curl \
#     cmake \
#     libopencv-dev \
#     build-essential
	
# Copy code directory
COPY ./code /code

# Set up virtual environment and install dependencies
RUN pip install --no-cache-dir \
    typing \
    fastapi \
    uvicorn \
    ultralytics \
    opencv-python \
    python-multipart

# Download weights
WORKDIR /code
RUN python getWeights.py yolov8s.pt

# Run server/inference engine
CMD python ./runInference.py yolov8s.onnx
