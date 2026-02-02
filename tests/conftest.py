"""Pytest configuration and fixtures."""

import pytest
import numpy as np
import soundfile as sf
import tempfile
from pathlib import Path


@pytest.fixture
def temp_audio_file():
    """Create a temporary WAV file for testing."""
    # Create a simple sine wave audio file
    sr = 22050  # Sample rate
    duration = 2  # seconds
    freq = 440  # Hz (A4 note)
    t = np.linspace(0, duration, int(sr * duration), False)
    audio_data = 0.3 * np.sin(2 * np.pi * freq * t)

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        temp_path = f.name

    sf.write(temp_path, audio_data, sr)
    yield temp_path

    # Cleanup
    Path(temp_path).unlink()


@pytest.fixture
def temp_image_file():
    """Create a temporary PNG image for testing."""
    try:
        from PIL import Image
    except ImportError:
        pytest.skip("PIL not available")

    img = Image.new('RGB', (100, 100), color=(73, 109, 137))

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        temp_path = f.name

    img.save(temp_path)
    yield temp_path

    # Cleanup
    Path(temp_path).unlink()


@pytest.fixture
def temp_output_file():
    """Create a temporary output path for video files."""
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
        temp_path = f.name

    yield temp_path

    # Cleanup
    Path(temp_path).unlink(missing_ok=True)
