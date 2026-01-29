# SoundViz

Convert audio files to visual effects driven by audio properties. Transform WAV and MP3 files into synchronized video visualizations.

## Features

- 🎵 Converts audio files (WAV, MP3) to visual video representations
- 📊 Analyzes audio properties (frequency, amplitude, etc.)
- 🎬 Generates videos synchronized with audio
- 🔧 Modular architecture for easy extension
- 📦 Installable as a Python package

## Installation

### From Source
```bash
git clone <repository-url>
cd soundviz
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

### Requirements
- Python 3.10+
- FFmpeg (for audio/video processing)

### macOS
```bash
brew install ffmpeg
```

### Ubuntu/Debian
```bash
sudo apt-get install ffmpeg
```

### Windows
Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use:
```bash
choco install ffmpeg
```

## Usage

### Command Line
```bash
soundviz --input audio.wav --output visualization.mp4
```

### As a Library
```python
from soundviz import Visualizer

visualizer = Visualizer(input_path="audio.mp3")
visualizer.process()
visualizer.save("output.mp4")
```

## Project Structure

```
soundviz/
├── cli.py              # Command-line interface
├── processing/         # Audio analysis and processing
│   └── batch.py        # Batch processing utilities
└── visualization/      # Video generation
    └── visualizer.py   # Main visualization engine
```

## Development

### Install with Development Dependencies
```bash
pip install -e ".[dev]"
```

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
flake8 sonicviz/
black sonicviz/
```

## Supported Formats

- **Audio**: WAV, MP3
- **Video Output**: MP4

## Contributing

Contributions welcome! Please ensure:
- Code follows PEP 8 style (checked via flake8)
- All tests pass
- New features include tests

## License

MIT License - see LICENSE file for details

## Author

Pedro Blaya Luz
- Use lower fps (24) for development, increase to 60 for final output

## License

Free to use and modify for personal/commercial projects.
