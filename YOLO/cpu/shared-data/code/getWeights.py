import sys
from ultralytics import YOLO

if __name__=="__main__":
    if(len(sys.argv) != 2):
        print("Usage: python getWeights.py <FILE>.pt")
        sys.exit(1)
    elif(sys.argv[1][-3:] != '.pt'):
        print("Incorrect usage. Filename must end in .pt")
        sys.exit(1)

    try:
        model = YOLO(sys.argv[1])

        model.export(format='onnx')

        sys.exit(0)
    except Exception as e:
        print(f"Error occurred. {e}")
        sys.exit(1)
