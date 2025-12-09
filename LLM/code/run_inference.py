import os
import sys
import signal
import platform
import argparse
import subprocess

# SECTION: Running inference. This portion is heavily influenced by
# github.com/microsoft/BitNet/blob/main/run_inference.py

# Runs a command (a list)
def run_command(command, shell=False, cap=True):
    """Run a system command and ensure it succeeds."""
    try:
        result = subprocess.run(
            command,
            capture_output=cap,
            text=cap,
            shell=shell,
            check=True
        )

        if cap:
            return result.stdout
        else:
            return ""
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running command: {e}")
        sys.exit(1)

class InferArgs:
    n_predict = 256
    threads = 2
    prompt = "Hello BitNet!"
    ctx_size = 2048
    temperature = 0.8
    conversation = False
    host = "127.0.0.1"
    port = 8080

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Calls llama-cli executable to run inference, and returns response
def Infer(args):
    # This is for linux, as docker container should be. If on windows for
    # some reason, change to '/BitNet/build/bin/Release/llama-cli.exe'
    main_path = "/BitNet/build/bin/llama-cli"

    command = [
        f'{main_path}',
        '-m', '/BitNet/models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf',
        '-n', str(args.n_predict),
        '-t', str(args.threads),
        '-p', args.prompt,
        '-ngl', '0',
        '-c', str(args.ctx_size),
        '--temp', str(args.temperature),
        "-b", "1",
        '--host', args.host,
        '--port', str(args.port)
    ]

    ret = run_command(command)

    return ret

# Signal handler for graceful exits.
def signal_handler(sig, frame):
    print("Ctrl+C pressed, exiting...")
    sys.exit(0)
