"""Tests for waveform visualizer."""

import numpy as np
from sonicviz.visualization.waveform_visualizer import WaveformVisualizer


def test_waveform_visualizer_initialization(temp_audio_file, temp_output_file):
    """Test WaveformVisualizer initialization."""
    viz = WaveformVisualizer(temp_audio_file, temp_output_file)

    assert viz.audio_file == temp_audio_file
    assert viz.output_file == temp_output_file
    assert viz.history_length == 60


def test_waveform_visualizer_history_length(temp_audio_file, temp_output_file):
    """Test that history_length is set correctly."""
    viz = WaveformVisualizer(temp_audio_file, temp_output_file)
    assert viz.history_length == 60


def test_generate_frame(temp_audio_file, temp_output_file):
    """Test frame generation."""
    viz = WaveformVisualizer(temp_audio_file, temp_output_file)

    # Create mock amplitude data
    amplitudes = [0.5 * np.sin(i / 10) for i in range(60)]
    frame = viz.generate_frame(amplitudes)

    assert frame is not None
    assert isinstance(frame, np.ndarray)
    assert frame.ndim == 3  # Height, Width, Channels
    assert frame.shape[2] == 3  # RGB channels


def test_waveform_full_pipeline(temp_audio_file, temp_output_file):
    """Test complete waveform visualization pipeline."""
    viz = WaveformVisualizer(temp_audio_file, temp_output_file, max_duration=0.5)

    # Load audio
    viz.load_audio()
    assert viz.y is not None

    # Compute amplitude
    viz.compute_amplitude_history()
    assert len(viz.amplitude_history) > 0

    # Generate frames (skip actual video creation)
    viz.generate_frames()
    assert len(viz.frames) > 0


def test_waveform_frame_dimensions(temp_audio_file, temp_output_file):
    """Test that generated frames have consistent dimensions."""
    viz = WaveformVisualizer(temp_audio_file, temp_output_file)

    # Generate multiple frames with different amplitudes
    frame1 = viz.generate_frame([0.2] * 60)
    frame2 = viz.generate_frame([0.8] * 60)

    # All frames should have same dimensions
    assert frame1.shape == frame2.shape
