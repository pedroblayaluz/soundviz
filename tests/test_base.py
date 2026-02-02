"""Tests for base visualizer."""

import numpy as np
from sonicviz.visualization.base import BaseVisualizer


class ConcreteVisualizer(BaseVisualizer):
    """Concrete implementation of BaseVisualizer for testing."""

    def generate_frames(self):
        """Stub implementation."""
        self.frames = [np.zeros((100, 100, 3), dtype=np.uint8)]

    def create_video(self):
        """Stub implementation."""
        pass


def test_base_visualizer_initialization(temp_audio_file, temp_output_file):
    """Test BaseVisualizer initialization."""
    viz = ConcreteVisualizer(temp_audio_file, temp_output_file)

    assert viz.audio_file == temp_audio_file
    assert viz.output_file == temp_output_file
    assert viz.max_duration is None
    assert viz.frames == []


def test_base_visualizer_with_max_duration(temp_audio_file, temp_output_file):
    """Test BaseVisualizer with max_duration."""
    max_duration = 1.0
    viz = ConcreteVisualizer(temp_audio_file, temp_output_file, max_duration=max_duration)

    assert viz.max_duration == max_duration


def test_load_audio(temp_audio_file):
    """Test audio loading."""
    viz = ConcreteVisualizer(temp_audio_file)
    viz.load_audio()

    assert viz.y is not None
    assert viz.sr is not None
    assert len(viz.y) > 0
    assert viz.sr > 0


def test_load_audio_with_max_duration(temp_audio_file):
    """Test audio loading with max_duration."""
    max_duration = 1.0
    viz = ConcreteVisualizer(temp_audio_file, max_duration=max_duration)
    viz.load_audio()

    # Check that audio is trimmed
    expected_max_samples = int(viz.sr * max_duration)
    assert len(viz.y) <= expected_max_samples + 1


def test_compute_amplitude_history(temp_audio_file):
    """Test amplitude history computation."""
    viz = ConcreteVisualizer(temp_audio_file)
    viz.load_audio()
    viz.compute_amplitude_history()

    assert viz.amplitude_history is not None
    assert len(viz.amplitude_history) > 0
    # All amplitudes should be normalized to 0-1
    assert all(0 <= a <= 1 for a in viz.amplitude_history)


def test_mono_audio_conversion(temp_audio_file):
    """Test that stereo audio is converted to mono."""
    viz = ConcreteVisualizer(temp_audio_file)
    viz.load_audio()

    # Audio should be 1D after loading
    assert len(viz.y.shape) == 1
