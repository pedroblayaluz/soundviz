import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from .base import BaseVisualizer
import tempfile
import os


class WaveformVisualizer(BaseVisualizer):
    """Converts audio files to animated waveform visualizations."""

    def __init__(self, audio_file: str, output_file: str = "output.mp4", max_duration: float = None) -> None:
        """Initialize the visualizer with input and output paths.

        Args:
            audio_file: Path to the input audio file
            output_file: Path for the output video file
            max_duration: Maximum duration in seconds to process (None for full duration)
        """
        super().__init__(audio_file, output_file, max_duration)
        self.history_length = 60

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
        
        # If max_duration was specified, save trimmed audio to temporary file
        audio_file_to_use = self.audio_file
        temp_audio = None
        
        if self.max_duration is not None:
            # Create temporary audio file with trimmed content
            temp_fd, temp_audio = tempfile.mkstemp(suffix='.wav')
            os.close(temp_fd)
            try:
                sf.write(temp_audio, self.y, self.sr)
                audio_file_to_use = temp_audio
            except Exception as e:
                print(f"Warning: Could not write temp audio file: {e}")
                audio_file_to_use = self.audio_file
        
        try:
            clip.write_videofile(
                self.output_file,
                audio=audio_file_to_use
            )
            print("Done!")
        finally:
            # Clean up temporary file if created
            if temp_audio and os.path.exists(temp_audio):
                try:
                    os.remove(temp_audio)
                except:
                    pass
