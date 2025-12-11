import os
import sys
import cv2
import uuid
import uvicorn
import numpy as np

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

port = 8080

def handle_arguments():
    if (len(sys.argv) not in [2,3]):
        print("Must enter model path cli argument")
        sys.exit(1)
    elif (sys.argv[1][-5:] != ".onnx"):
        print("Must be an onnx model")
        sys.exit(1)
    
    try:
        port = int(sys.argv[2])
    except Exception:
        pass


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

    frameCounter = 0
    frameCenterX = frame_width / 2
    frameCenterY = frame_height / 2

    # Only do inference to find people
    # Value 0 comes from COCO dataset index for 'person'
    PERSON_CLASS_ID = 0

    closest_box = None

    while cap.isOpened():
        # Get and validate frame
        ret, frame = cap.read()
        if not ret:
            break

        # Run inference every 10 frames to save time
        if frameCounter % 10 == 0:
            # Run inference on the current frame, not verbose
            results = model(frame, verbose=False, classes=[PERSON_CLASS_ID], conf=0.5)[0]

            # Find the most centered box (assuming the most centered box is the professor)
            boxes_xywh = results.boxes.xywh.cpu().numpy()

            if len(boxes_xywh) == 0:
                out.write(frame)
                continue

            center_diff_x = boxes_xywh[:, 0] - frameCenterX
            center_diff_y = boxes_xywh[:, 1] - frameCenterY

            # Good 'ole pythagorean theorem :D
            distances = np.sqrt(center_diff_x ** 2 + center_diff_y ** 2)

            closest_box = np.argmin(distances)

            closest_xy  = boxes_xywh[closest_box]
            closest_box = results[closest_box]


        # Annotate frame
        x1, y1, x2, y2 = [int(val) for val in closest_xy]

        x1 = 2 * x1 - x2
        y1 = 2 * y1 - y2

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 10)

        # Write to VideoWriter output
        out.write(frame)

        frameCounter += 1

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return True

# FastAPI Endpoint for POST requests. Heavily influenced by
# geeksforgeeks.com/python/creating-first-rest-api-with-fastapi, and
# fastapi.tiangolo.com/tutorial/request-files/
@app.post("/inference/", summary="Upload MP4, server runs YOLO inference, and returns annotated MP4")
async def api_endpoint(file: Annotated[UploadFile, File(description="MP4 video file to process")]):
    # Generate unique paths to guarantee no collisions
    file_id = str(uuid.uuid4())
    TEMP_DIR="/data/temp_videos"
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

    uvicorn.run("runInference:app", host="0.0.0.0", port=port, log_level="info", reload=True)

