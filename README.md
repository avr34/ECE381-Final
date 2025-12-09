# BitSearch

## ECE381 - Final Project

### Group Members: Arnav Revankar and Wilby Marcellus

![In progress shield](https://img.shields.io/badge/STILL_IN_PROGRESS!!!-DA0AFF)

-----

<!-- Introduction -->
BitSearch is a *video summarizer* tool, built with [OpenAI Whisper][01], [Microsoft BitNet.cpp][02], [and Ultralytics YOLOv11n][03]. It (once finished) will be able to take input of either video or audio, process said video/audio, and then create a BitNet interface, where a user can ask questions about the contents of the video/audio. If a video is provided, it will create a new video with augmented closed captions, as well as bounding boxes around the people in the frame.

### Installation:

Installation is done in 3 steps:

- Clone this repository
- Build the docker images
- Run the docker container

To **clone the repository**, run the following command:

```
git clone https://github.com/avr33-boop/BitSearch.git
```

Once it's cloned, you must build each of the docker images. To build BitNet, run the following commands:

```
cd BitSearch/LLM
docker build -t BitSearch/LLM .
```

It's worth it to have a powerful *cpu* for this part, as compilation is a cpu-intensive task. The whole idea of using BitNet.cpp was to make this accessible to non-gpu users anyway. For reference: compilation on an NVIDIA Jetson Orin Nano took more than 2.5 hours, while on an i7-4790, 16 GB DDR3, HDD computer, it only took 1 hour.

<!-- TODO: Add rest of the instructions -->

<!-- Links -->
[01]: https://github.com/openai/whisper
[02]: https://github.com/microsoft/BitNet
[03]: https://github.com/ultralytics/ultralytics
