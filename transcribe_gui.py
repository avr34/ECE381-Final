import cv2
import requests
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os

# -----------------------------
# Server URLs
# -----------------------------
YOLO_SERVER_URL = "http://localhost:80/process-video"      # <-- replace if needed
WHISPER_SERVER_URL = "http://localhost:8080/inference"   # <-- replace if needed

# -----------------------------
# Global variables
# -----------------------------
cap = None
bbox = None
video_running = False
current_file = None
is_video_file = False
transcript_lines = []

# -----------------------------
# Whisper transcription
# -----------------------------
def run_inference(file_path):
    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "application/octet-stream")}
            data = {
                "temperature": "0.0",
                "temperature_inc": "0.2",
                "response_format": "json"
            }
            response = requests.post(WHISPER_SERVER_URL, files=files, data=data)
            txt = response.json().get("text", "")
            lines = [line.strip() for line in txt.split("\n") if line.strip()]
            return lines
    except Exception as e:
        messagebox.showerror("Error", f"Whisper error: {e}")
        return []

#def run_yolo_inference(filepath):
  #  try:
      #  with open(filepath, "rb") as f:
          #  files = {""}
    #except:

# -----------------------------
# Browse file
# -----------------------------
def browse_file():
    global current_file, is_video_file, video_running

    # Stop any running video loop
    video_running = False

    file_path = filedialog.askopenfilename(
        title="Select audio or video file",
        filetypes=[("Audio/Video Files", "*.m4a *.mp3 *.wav *.mp4 *.mov *.avi *.mkv")]
    )
    if not file_path:
        return

    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)

    current_file = file_path
    is_video_file = file_path.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))

# -----------------------------
# YOLO detection via server
# -----------------------------
def get_professor_bbox(frame):
    try:
        _, encoded = cv2.imencode(".jpg", frame)
        files = {"file": ("frame.jpg", encoded.tobytes(), "image/jpeg")}
        res = requests.post(YOLO_SERVER_URL, files=files)
        data = res.json()
        if data.get("bbox") and data.get("label") == "person":
            return tuple(data["bbox"])
    except Exception as e:
        print("YOLO error:", e)
    return None

def draw_professor_box(frame, bbox):
    if bbox:
        x1, y1, x2, y2 = bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(frame, "Professor", (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    return frame

# -----------------------------
# Overlay transcript on frame
# -----------------------------
def overlay_transcript(frame, lines, max_lines=4):
    # Only show last few lines so video is not cluttered
    to_show = lines[-max_lines:]

    y0 = frame.shape[0] - (len(to_show)*25) - 20
    for i, line in enumerate(to_show):
        y = y0 + i*25
        cv2.putText(frame, line, (10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    return frame

# -----------------------------
# Audio placeholder
# -----------------------------
def show_audio_placeholder(lines):
    global video_running
    video_running = False

    frame = np.zeros((360, 640, 3), dtype=np.uint8)
    cv2.putText(frame, "Audio file", (220, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0,255,0), 2)

    frame = overlay_transcript(frame, lines, max_lines=8)

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img_rgb)
    imgtk = ImageTk.PhotoImage(image=img)
    label_video.imgtk = imgtk
    label_video.configure(image=imgtk)

# -----------------------------
# Transcribe and display
# -----------------------------
def transcribe_file():
    global transcript_lines
    if not current_file:
        messagebox.showwarning("Warning", "Select a file first")
        return

    transcript_lines = run_inference(current_file)
    if not transcript_lines:
        return

    # Update transcript text box
    text_result.config(state=tk.NORMAL)
    text_result.delete("1.0", tk.END)
    for line in transcript_lines:
        text_result.insert(tk.END, line + "\n")

    text_result.tag_add("last_line", f"{len(transcript_lines)}.0", tk.END)
    text_result.tag_config("last_line", foreground="blue", font=("Helvetica", 12, "bold"))
    text_result.config(state=tk.DISABLED)

    # If audio file → show placeholder instead of video
    if not is_video_file:
        show_audio_placeholder(transcript_lines)

# -----------------------------
# Video playback
# -----------------------------
def play_video():
    global cap, bbox, video_running

    if not current_file:
        messagebox.showwarning("Warning", "Select a file first")
        return

    if not is_video_file:
        show_audio_placeholder(transcript_lines)
        return

    cap = cv2.VideoCapture(current_file)
    bbox = None
    video_running = True

    def update_frame():
        global bbox, video_running

        if not video_running:
            return

        ret, frame = cap.read()
        if not ret:
            cap.release()
            video_running = False
            return

        # Detect professor on the first frame only
        if bbox is None:
            bbox = get_professor_bbox(frame)

        frame = draw_professor_box(frame, bbox)
        frame = overlay_transcript(frame, transcript_lines)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        label_video.imgtk = imgtk
        label_video.configure(image=imgtk)

        label_video.after(30, update_frame)

    update_frame()

# -----------------------------
# Save transcription
# -----------------------------
def save_transcription():
    if not current_file:
        messagebox.showwarning("Warning", "No file selected!")
        return
    content = text_result.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Warning", "No transcription to save!")
        return

    default_name = os.path.splitext(os.path.basename(current_file))[0] + "_transcription.txt"
    save_path = filedialog.asksaveasfilename(
        title="Save Transcription",
        defaultextension=".txt",
        initialfile=default_name
    )
    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Saved to {save_path}")

# -----------------------------
# GUI Layout
# -----------------------------
root = tk.Tk()
root.title("Audio/Video Transcription GUI")

# Top file row
frame_file = tk.Frame(root)
frame_file.pack(padx=10, pady=5, fill=tk.X)
entry_file = tk.Entry(frame_file, width=50)
entry_file.pack(side=tk.LEFT, padx=5)
btn_browse = tk.Button(frame_file, text="Browse File", command=browse_file)
btn_browse.pack(side=tk.LEFT, padx=5)

# Video frame
label_video = tk.Label(root)
label_video.pack(padx=10, pady=10)

# Buttons
frame_btn = tk.Frame(root)
frame_btn.pack(pady=5)
tk.Button(frame_btn, text="Transcribe", command=transcribe_file).pack(side=tk.LEFT, padx=5)
tk.Button(frame_btn, text="Play Video", command=play_video).pack(side=tk.LEFT, padx=5)
tk.Button(frame_btn, text="Save Transcription", command=save_transcription).pack(side=tk.LEFT, padx=5)

# Transcript text box
frame_text = tk.Frame(root)
frame_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
scroll = tk.Scrollbar(frame_text)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
text_result = tk.Text(frame_text, yscrollcommand=scroll.set, wrap=tk.WORD)
text_result.pack(fill=tk.BOTH, expand=True)
scroll.config(command=text_result.yview)
text_result.config(state=tk.DISABLED)

# Run GUI
root.mainloop()
