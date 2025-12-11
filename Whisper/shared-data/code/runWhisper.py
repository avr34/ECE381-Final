import os
import io
import sys
import time
import httpx
import uvicorn
import subprocess

from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from contextlib import asynccontextmanager

# whisper server runs on port 8000 within container, 
# this script serves on 8080 within this container,
# docker compose links this container 8080 to 8080 of device
server_run = [
    "whisper-server",
    "-m", "/app/models/ggml-small.bin",
    "--host", "0.0.0.0",
    "--port", "8000",
    "--convert"
]

server_url = "http://localhost:8000/inference"

port = 8080

app = FastAPI(
    title = "Whisper Inference Server",
    description = "Accepts video/audio input, converts to WAV with ffmpeg if necessary, and transcribes to english text",
)

async def get_http_client():
    client = httpx.AsyncClient(timeout=30.0)
    try:
        yield client
    finally:
        await client.aclose()
        print('HTTPX Client Closed')

def handle_arguments():
    if (len(sys.argv) != 3):
        print('Usage: runWhisper.py <PATH TO MODEL> <PORT>')
        sys.exit(1)
    elif (sys.argv[1][-4:] != '.bin'):
        print('Model must be in .bin format')
        sys.exit(1)
    try:
        port = int(sys.argv[2])
    except Exception:
        print('Invalid port number. Must be an int')

@app.post('/inference/')
async def forward_file(
    file: UploadFile = File(...),
    http_client: httpx.AsyncClient = Depends(get_http_client)
):
    try:
        file_content = await file.read()
    except Exception as e:
        return JSONResponse(
            content={"message": f"Server error: {e}"},
            status_code=500
        )

    files = {
        "file": (file.filename, io.BytesIO(file_content), file.content_type)
    }

    print(f"Forwarding request to {server_url}")

    try:
        response = await http_client.post(
            server_url,
            files = files
        )

        return StreamingResponse(
            content = response.aiter_bytes(),
            status_code = response.status_code,
            headers = response.headers
        )

    except Exception as e:
        return JSONResponse(
            content = {"message": f"Server error: {e}"},
            status_code = 500
        )

if __name__=="__main__":
    handle_arguments()
    
    proc = subprocess.Popen(server_run)

    time.sleep(5)

    uvicorn.run("runWhisper:app", host="0.0.0.0", port=int(sys.argv[2]), log_level="info", reload=True)
