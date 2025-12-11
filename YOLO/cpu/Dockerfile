# Start with ultralytics/ultralytics:latest-cpu base image
#
# Then run fully custom YOLO inference server
FROM ultralytics/ultralytics:latest-cpu
WORKDIR /ultralytics

# Set up virtual environment and install dependencies
# RUN python3 -m venv .env
# ENV PATH="/ultralytics/.env/bin/:$PATH"
RUN pip install --no-cache-dir \
    typing \
    fastapi \
    uvicorn \
    ultralytics \
    opencv-python \
    python-multipart

# Copy code directory
COPY ./shared-data /data

# Download weights
WORKDIR /data/code
RUN mkdir /weights && \
    cd /weights && \
    python3 /data/code/getWeights.py yolov8s.pt

# Run server/inference engine
ENTRYPOINT ["python3"]
CMD ["./runInference.py", "/weights/yolov8s.onnx", "8080"]
