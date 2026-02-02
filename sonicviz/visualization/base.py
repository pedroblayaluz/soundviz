"""Abstract base class for audio visualizers."""

from abc import ABC, abstractmethod
import numpy as np
import soundfile as sf


class BaseVisualizer(ABC):
    """Abstract base class for audio visualizations."""

    def __init__(self, audio_file: str, output_file: str = "output.mp4", max_duration: float = None) -> None:
        """Initialize the visualizer with input and output paths.

        Args:
            audio_file: Path to the input audio file
            output_file: Path for the output video file
            max_duration: Maximum duration in seconds to process (None for full duration)
        """
        self.audio_file = audio_file
        self.output_file = output_file
        self.max_duration = max_duration
        self.window = 2048
        self.hop_length = self.window // 4
        self.frames = []
        self.y = None
        self.sr = None
        self.amplitude_history = None

    def load_audio(self) -> None:
        """Load audio file and prepare it for processing."""
        self.y, self.sr = sf.read(self.audio_file)
        if len(self.y.shape) > 1:
            # Convert stereo to mono by averaging both channels
            self.y = np.mean(self.y, axis=1)
        
        # Trim to max_duration if specified
        if self.max_duration is not None:
            max_samples = int(self.sr * self.max_duration)
            self.y = self.y[:max_samples]
        
        duration = len(self.y) / self.sr
        print(f"Audio loaded. Duration: {duration:.2f}s, Sample rate: {self.sr} Hz")

    def compute_amplitude_history(self) -> None:
        """Pre-compute amplitude for all frames."""
        print("Computing amplitude history...")
        self.amplitude_history = []
        for i in range(0, len(self.y) - self.window, self.hop_length):
            slice_data = self.y[i:i + self.window]
            amplitude = np.sqrt(np.mean(slice_data ** 2))
            self.amplitude_history.append(amplitude)

        if len(self.amplitude_history) == 0:
            raise ValueError("No amplitude data computed from audio file")

        max_amplitude = max(self.amplitude_history)
        if max_amplitude > 0:
            self.amplitude_history = [a / max_amplitude for a in self.amplitude_history]

    @abstractmethod
    def generate_frames(self) -> None:
        """Generate all frames for the visualization.

        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def create_video(self) -> None:
        """Create the output video file.

        Must be implemented by subclasses.
        """
        pass

    def run(self) -> None:
        """Execute the complete visualization pipeline."""
        self.load_audio()
        self.compute_amplitude_history()
        self.generate_frames()
        self.create_video()
