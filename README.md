# BitSum

### **ECE381 - Final Project** - Group Members: Arnav Revankar and Wilby Marcellus

![In progress shield](https://img.shields.io/badge/STILL_IN_DEVELOPMENT!!!-DA0AFF)

-----

<!-- Introduction -->
**Problem Statement:** Humans naturally have short attention spans. To be specific, the average human's attention span is only about a minute long[^1]. On the other hand, college lectures can range from an hour to three or four hours long. This presents a significant problem: *how do we optimally digest the material we hear in class?* BitSum arrives to fill that gap. It is a *local* service that you can use to summarize and annotate lectures.

BitSum is a *lecture summarizer* tool, built with [OpenAI Whisper][2] ([ggml-org Whisper.cpp][3]), [Microsoft BitNet.cpp][4], [and Ultralytics YOLOv11n][5]. It (once finished) will take input of either audio or video, then transcribe and summarize said audio/video. If a video is provided, it will create a new video with augmented closed captions, as well as bounding boxes around the people in the frame.

### Installation:

BitSum is built with docker containers in mind (it was one of the project's requirements), and so even through it's designed to run on a CPU, *it is rather disk-heavy, taking up* ***15GB*** *on our test machines*. Please keep that in mind before proceeding.

Installing BitSum takes 4 steps:

- Installing Docker (if not already installed)
- Cloning this repository
- Building the docker images
- Running the docker containers

#### Cloning the Repo

To **clone the repository**, run the following command:

```bash
git clone https://github.com/avr34/ECE381-Final.git BitSum && \
cd BitSum
```

#### Building Docker Images

Once it's cloned, you must build each of the docker images. To build BitNet, run the following commands:

```bash
cd ./LLM
bash ./build.bash
```

It's worth it to have a powerful *cpu* for this part, as compilation is a cpu-intensive task. The whole idea of using BitNet.cpp was to make this accessible to non-gpu users anyway. For reference: compilation on an NVIDIA Jetson Orin Nano took more than 2.5 hours (powerful GPU, weak CPU), while on an i7-4790, 16 GB DDR3, HDD computer, it only took 1 hour, and 20 minutes on an i5-6300U, 16 GB DDR4 computer with an SSD.

Then, build Whisper, by running the commands shown below. This will be much faster as nothing is compiled, the base image conveniently comes with pre-compiled executables :smiley:[^2]

```bash
cd ../Whisper
bash ./build.bash
```

Finally, build YOLO. Again, this is quite fast.

```bash
cd ../YOLO
bash ./build.bash
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
