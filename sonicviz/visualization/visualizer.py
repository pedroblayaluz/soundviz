import numpy as np
import matplotlib.pyplot as plt
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import soundfile as sf


class AudioVisualizer:
    """Converts audio files to video visualizations with waveform animations."""

    def __init__(self, audio_file: str, output_file: str = "output.mp4") -> None:
        """Initialize the visualizer with input and output paths.

        Args:
            audio_file: Path to the input audio file
            output_file: Path for the output video file
        """
        self.audio_file = audio_file
        self.output_file = output_file
        self.window = 2048
        self.hop_length = self.window // 4
        self.history_length = 60
        self.frames = []
        self.y = None
        self.sr = None
        self.amplitude_history = None

    def load_audio(self) -> None:
        """Load audio file and prepare it for processing."""
        self.y, self.sr = sf.read(self.audio_file)
        if len(self.y.shape) > 1:
            self.y = self.y[:, 0]
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

        max_amplitude = max(self.amplitude_history)
        self.amplitude_history = [a / max_amplitude for a in self.amplitude_history]

    def generate_frame(self, current_amplitudes: list) -> np.ndarray:
        """Generate a single frame from amplitude data.

        Args:
            current_amplitudes: List of amplitude values to visualize

        Returns:
            Numpy array representing the frame
        """
        fig, ax = plt.subplots(figsize=(15, 1), dpi=100)
        x = np.arange(len(current_amplitudes))
        ax.plot(x, current_amplitudes, color='white', linewidth=2)

        ax.set_ylim(0, 1.1)
        ax.set_xlim(0, self.history_length - 1)
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
        ax.axis('off')
        fig.tight_layout(pad=0)
        fig.canvas.draw()

        width, height = fig.canvas.get_width_height()
        frame = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
        frame = frame.reshape((height, width, 4))[:, :, 1:]  # Skip alpha channel
        plt.close(fig)

        return frame

    def generate_frames(self) -> None:
        """Generate all frames for the visualization."""
        print("Generating frames...")
        for frame_idx in range(len(self.amplitude_history)):
            start_idx = max(0, frame_idx - self.history_length)
            current_amplitudes = list(
                self.amplitude_history[start_idx:frame_idx + 1]
            )

            if len(current_amplitudes) < self.history_length:
                padding = [0] * (self.history_length - len(current_amplitudes))
                current_amplitudes = padding + current_amplitudes

            frame = self.generate_frame(current_amplitudes)
            self.frames.append(frame)

    def create_video(self) -> None:
        """Create the output video file."""
        print("Creating video...")
        fps = self.sr / self.hop_length
        clip = ImageSequenceClip(self.frames, fps=fps)
        clip.write_videofile(self.output_file, audio=self.audio_file)
        print("Done!")

    def run(self) -> None:
        """Execute the complete visualization pipeline."""
        self.load_audio()
        self.compute_amplitude_history()
        self.generate_frames()
        self.create_video()
