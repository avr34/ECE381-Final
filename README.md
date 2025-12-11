# BitSum

### **ECE381 - Final Project** - Group Members: Arnav Revankar and Wilby Marcellus

![In progress shield](https://img.shields.io/badge/STILL_IN_DEVELOPMENT!!!-DA0AFF)

-----

<!-- Introduction -->
**Problem Statement:** Humans naturally have short attention spans. To be specific, the average human's attention span is only about a minute long[^1]. On the other hand, college lectures can range from an hour to three or four hours long. This presents a significant problem: *how do we optimally digest the material we hear in class?* BitSum arrives to fill that gap. It is a *local* service that you can use to summarize and annotate lectures.

BitSum is a *lecture summarizer* tool, built with [OpenAI Whisper][2] ([ggml-org Whisper.cpp][3]), [Microsoft BitNet.cpp][4], [and Ultralytics YOLOv11n][5]. It (once finished) will take input of either audio or video, then transcribe and summarize said audio/video. If a video is provided, it will create a new video with augmented closed captions, as well as bounding boxes around the people in the frame.

### Installation:

BitSum is built with docker containers in mind (it was one of the project's requirements), and so even through it's designed to run on a CPU, *it is rather disk-heavy, taking up* ***15GB*** *on our test machines*. Please keep that in mind before proceeding.

Installing BitSum takes 5 steps:

- **Installing Docker** (if not already installed)
- **Cloning this repository**
- **Running Docker Containers**
- **Installing Python Dependencies**
- **Running the Program**

#### Installing docker

For the most up to date instructions, please visit [docker's website][6]

#### Cloning the Repo

To **clone the repository**, run the following command:

```bash
git clone https://github.com/avr34/ECE381-Final.git BitSum && \
cd BitSum
```

#### Building Docker Images

Once it's cloned, you must build the docker images. Thankfully, we have `docker compose` which makes that very simple.

```bash
docker compose up
```

It's worth it to have a powerful *cpu* for this part (compiling BitNet.cpp, binaries are not distributed), as compilation is a cpu-intensive task. The whole idea of using BitNet.cpp was to make this accessible to non-gpu users anyway. For reference: compilation on an NVIDIA Jetson Orin Nano took more than 2.5 hours (powerful GPU, weak CPU), while on an i7-4790, 16 GB DDR3, HDD computer, it only took 1 hour, and 20 minutes on an i5-6300U, 16 GB DDR4 computer with an SSD.

Building the images for Whisper and Yolo should be much faster, but still expect no less than 30-40 minutes at least.

#### Installing the Python Dependencies

For this part, a virtual environment is highly advised; it takes up more disk space, but guarantees that you won't break any of your other applications by upgrading to a new package version. To create the virual environment, make sure `python3-venv` is installed. Then run:

```
# Windows
python3 -m venv .env
cd .env/Scripts/
activate.bat
cd ../../

# Linux/MacOS
python3 -m venv .env
source .env/bin/activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

#### Running the Program

Finally:

```bash
python3 ./transcribe_gui.py
```

#### Misc

Also, in each project folder, there are `run.bash` and `test.bash` files, which contain simple commands to test each module individually.

<!-- TODO: Add rest of the instructions -->

[^1]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10621754/
[^2]: https://github.com/ggml-org/whisper.cpp?tab=readme-ov-file#docker

<!-- Links -->
[2]: https://github.com/openai/whisper
[3]: https://github.com/ggml-org/whisper.cpp
[4]: https://github.com/microsoft/BitNet
[5]: https://github.com/ultralytics/ultralytics
[6]: https://www.docker.com/get-started/
