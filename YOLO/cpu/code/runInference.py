import os
import sys
import cv2
import uuid
import uvicorn

from ultralytics import YOLO
from typing import Annotated
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File, Response

# Define the FastAPI api
app = FastAPI(
    title="YOLO Video Inference Server",
    description="Accepts MP4, and returns MP4 with augmented bounding boxes"
)

# Create model
model = YOLO(sys.argv[1])

def handle_arguments():
    if (len(sys.argv) != 2):
        print("Must enter model path as a cli argument")
        sys.exit(1)
    elif (sys.argv[1][-5:] != ".onnx"):
        print("Must be an onnx model")
        sys.exit(1)

def infer_w_yolo(input_path, output_path) -> bool:
    cap = cv2.VideoCapture(input_path)

    # Make sure video exists
    if not cap.isOpened():
        print(f"Error occurred, could not open video: {e}")
        return False

    # Get video metadata
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the file format and VideoWriter object for output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        # Get and validate frame
        ret, frame = cap.read()
        if not ret:
            break

        # Run inference on the current frame, not verbose
        results = model(frame, verbose=False)[0]

        # Annotate current frame
        annotated_frame = results.plot()

        # Write to VideoWriter output
        out.write(annotated_frame)

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return True

# FastAPI Endpoint for POST requests. Heavily influenced by
# geeksforgeeks.com/python/creating-first-rest-api-with-fastapi, and
# fastapi.tiangolo.com/tutorial/request-files/
@app.post("/process-video/", summary="Upload MP4, server runs YOLO inference, and returns annotated MP4")
async def api_endpoint(file: Annotated[UploadFile, File(description="MP4 video file to process")]):
    # Generate unique paths to guarantee no collisions
    file_id = str(uuid.uuid4())
    TEMP_DIR="/code/temp_videos"
    input_path = os.path.join(TEMP_DIR, f'{file_id}_input.mp4')
    output_path = os.path.join(TEMP_DIR, f'{file_id}_output.mp4')

    try:
        # Write file content to input file
        file_content = await file.read()
        with open(input_path, "wb") as f:
            f.write(file_content)

        success = infer_w_yolo(input_path, output_path)

        if not success:
            return Response(content="Video processing failed.", status_code=500)

        return FileResponse(
            path=output_path,
            filename=f'annotated_{file.filename}',
            media_type="video/mp4"
        )
    except Exception as e:
        print(f'An error occurred: {e}')
        return Response(content=f'Server-side error: {e}', status_code=500)
    # finally:
    #     if(os.path.exists(input_path)):
    #        os.remove(input_path)
    #     if(os.path.exists(output_path)):
    #        os.remove(output_path)

if __name__=="__main__":
    # Handle input arguments
    handle_arguments()

    uvicorn.run("runInference:app", host="0.0.0.0", port=8000, log_level="info", reload=True)

