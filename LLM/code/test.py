import sys
import signal
from run_inference import InferArgs, Infer

if __name__ == "__main__":
    inputval = input("Enter question: ")
    inputtok = int(input("Enter number of tokens: "))
    args = InferArgs(f"User: {inputval}\n\nAssistant:", n_predict=inputtok)
    ret = Infer(args)

    print(ret)
    sys.exit(0)

def signal_handler(sig, frame):
    print("Ctrl+C pressed, exiting...")
    sys.exit(0)
