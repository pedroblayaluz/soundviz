"""Image animator visualizer that changes image size and saturation based on audio intensity."""

from pathlib import Path
import numpy as np
from PIL import Image, ImageEnhance
import soundfile as sf
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from .base import BaseVisualizer
import tempfile
import os


class ImageAnimatorVisualizer(BaseVisualizer):
    """Animates a PNG image based on audio intensity.

    Changes image size and saturation dynamically:
    - Size increases with sound intensity
    - Saturation increases with sound intensity (0 when intensity is low)
    """

    MIN_SCALE = 0.8
    MAX_SCALE = 1.2
    MIN_SATURATION = 0.0
    MAX_SATURATION = 2.0
    INTENSITY_THRESHOLD = 0.05  # Below this, saturation is forced to 0

    def __init__(
        self,
        audio_file: str,
        image_file: str = None,
        output_file: str = "output.mp4",
        max_duration: float = None
    ) -> None:
        """Initialize the image animator visualizer.

        Args:
            audio_file: Path to the input audio file
            image_file: Path to the PNG image file. If None, looks for file with
                       same name as audio_file but with .png extension
            output_file: Path for the output video file
            max_duration: Maximum duration in seconds to process (None for full duration)
        """
        super().__init__(audio_file, output_file, max_duration)
        self.image_file = image_file or self._find_image_file(audio_file)
        self.base_image = None
        self.frame_width = None
        self.frame_height = None

    def _find_image_file(self, audio_file: str) -> str:
        """Find PNG image with same name as audio file.

        Args:
            audio_file: Path to the audio file

        Returns:
            Path to the PNG file

        Raises:
            FileNotFoundError: If PNG file is not found
        """
        audio_path = Path(audio_file)
        image_path = audio_path.with_suffix('.png')

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image file not found: {image_path}. "
                f"Please ensure a PNG file with the same name as the audio file exists."
            )

        return str(image_path)

    def load_audio(self) -> None:
        """Load audio file and image."""
        super().load_audio()
        self._load_image()

    def _load_image(self) -> None:
        """Load and prepare the PNG image, preserving transparency."""
        print(f"Loading image: {self.image_file}")
        self.base_image = Image.open(self.image_file).convert('RGBA')
        self.frame_width, self.frame_height = self.base_image.size
        print(f"Image loaded. Size: {self.frame_width}x{self.frame_height}")

    def _apply_transformations(
        self,
        image: Image.Image,
        intensity: float
    ) -> Image.Image:
        """Apply size and saturation transformations based on intensity.

        Args:
            image: The base image to transform
            intensity: Normalized intensity value (0-1)

        Returns:
            Transformed image
        """
        # Calculate scale factor (size)
        scale = self.MIN_SCALE + (self.MAX_SCALE - self.MIN_SCALE) * intensity

        # Calculate saturation factor (0 when below threshold)
        if intensity < self.INTENSITY_THRESHOLD:
            saturation = self.MIN_SATURATION
        else:
            # Map intensity to saturation, starting from threshold
            normalized_intensity = (intensity - self.INTENSITY_THRESHOLD) / (
                1.0 - self.INTENSITY_THRESHOLD
            )
            saturation = self.MIN_SATURATION + (
                self.MAX_SATURATION - self.MIN_SATURATION
            ) * normalized_intensity

        # Apply size transformation
        new_width = int(self.frame_width * scale)
        new_height = int(self.frame_height * scale)
        resized = image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )

        # Apply saturation transformation
        enhancer = ImageEnhance.Color(resized)
        saturated = enhancer.enhance(saturation)

        return saturated

    def _center_on_canvas(self, image: Image.Image) -> Image.Image:
        """Center the image on a canvas of original size.

        Uses magenta (#FF00FF) as background for easy chroma key removal in video editors.
        Preserves image transparency via alpha compositing.

        Args:
            image: Image to center (RGBA format)

        Returns:
            Image centered on canvas with magenta background
        """
        # Magenta background for easy chroma key removal
        canvas = Image.new('RGBA', (self.frame_width, self.frame_height), (255, 0, 255, 255))
        x_offset = (self.frame_width - image.width) // 2
        y_offset = (self.frame_height - image.height) // 2
        # Use alpha_composite to preserve transparency
        canvas.paste(image, (x_offset, y_offset), image)
        # Convert back to RGB for video encoding
        return canvas.convert('RGB')

    def generate_frames(self) -> None:
        """Generate all frames by transforming the image based on amplitude."""
        print("Generating frames...")
        for frame_idx, intensity in enumerate(self.amplitude_history):
            # Apply transformations
            transformed = self._apply_transformations(self.base_image, intensity)

            # Center on canvas
            framed = self._center_on_canvas(transformed)

            # Convert to numpy array for moviepy
            frame_array = np.array(framed)
            self.frames.append(frame_array)

            if (frame_idx + 1) % 100 == 0:
                print(f"  Generated {frame_idx + 1}/{len(self.amplitude_history)} frames")

    def create_video(self) -> None:
        """Create the output video file with audio."""
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
                audio=audio_file_to_use,
                codec='libx264',
                audio_codec='aac'
            )
            print("Done!")
        finally:
            # Clean up temporary file if created
            if temp_audio and os.path.exists(temp_audio):
                try:
                    os.remove(temp_audio)
                except OSError:
                    pass
