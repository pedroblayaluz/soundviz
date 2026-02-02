# soundviz 🔊

Transform audio into mesmerizing visual animations. Make images pulse with the rhythm of sound.

## Installation

```bash
git clone https://github.com/pedroblayaluz/soundviz.git
cd soundviz
pip install -e .
```

Requires: Python 3.10+ and FFmpeg

## Usage

### Image Animator

Generate an animated visualization from audio and a static image:

```bash
soundviz --type image --input audio.wav --image image.png --output animation.mp4
```

Or process an entire folder of audio files with corresponding images:

```bash
soundviz input_folder --type image --output output_folder
```

**Note:** For folder processing with the image animator, each audio file must have a corresponding PNG image with the same name (e.g., `song.mp3` paired with `song.png`).

[Image animation example - GIF/Video placeholder]

## License

MIT License
