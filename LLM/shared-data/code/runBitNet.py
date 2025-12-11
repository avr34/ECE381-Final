import os
import sys
import time
import uvicorn
import requests
import subprocess

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from contextlib import asynccontextmanager
from typing import Dict, Any
from pydantic import BaseModel

class TextPrompt(BaseModel):
    """Defines the expected structure for incoming JSON requests."""
    prompt: str
    max_tokens: int = 256  # Default limit for the response
    temperature: float = 0.8 # Default generation randomness

server_run = [
    "/BitNet/build/bin/llama-server",
    "-m", "/BitNet/models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf",
    "-n", "256",
    "--host", "0.0.0.0",
    "--port", "8000"
]

server_url = "http://localhost:8000/completion"

port = 8080

app = FastAPI(
    title = "BitNet Inference Server",
    description = "Accepts promps, and responds accordingly"
)

# Function to call bitnet api directly
def call_bitnet(prompt: TextPrompt):
    payload = {
        "prompt": prompt.prompt,
        "n_predict": prompt.max_tokens,
        "temperature": prompt.temperature,
        "stream": False
    }

    try:
        response = requests.post(
            server_url,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        response_data = response.json()
        generated_text = response_data.get('content', '').strip()

        if not generated_text:
            raise ValueError("No response from bitnet server D:")

        return generated_text

    except Exception as e:
        print(f'Error occurred: {e}')
        raise HTTPException(status_code=500, detail=f'Server side error: {e}')

@app.post("/inference/", 
          response_model=Dict[str, Any],
          summary="Submits text prompt to llama-server")
async def forward_prompt(prompt_data: TextPrompt):
    # Check for empty prompt before sending
    if not prompt_data.prompt.strip():
        return {
            "input_prompt": prompt_data.prompt,
            "generated_text": "You didn't ask anything! >:(",
            "model_used": "BitNet/Llama.cpp Server"
        }

    # 1. Call the LLM client function
    llm_response = call_bitnet(prompt_data)

    # 2. Return the result to the user
    return {
        "input_prompt": prompt_data.prompt,
        "generated_text": llm_response,
        "model_used": "BitNet/Llama.cpp Server"
    }

if __name__ == "__main__":
    proc = subprocess.Popen(server_run)

    time.sleep(5)

    uvicorn.run("runBitNet:app", host="0.0.0.0", port=port, reload=True)
