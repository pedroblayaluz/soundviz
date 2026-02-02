"""Integration tests with real video output."""

from pathlib import Path
from sonicviz.visualization.image_animator import ImageAnimatorVisualizer
from sonicviz.visualization.waveform_visualizer import WaveformVisualizer


def test_image_animator_real_video(tmp_path):
    """Test image animator with real video generation."""
    test_dir = Path(__file__).parent / "resources"
    audio_file = test_dir / "input.wav"
    image_file = test_dir / "input.png"
    output_file = tmp_path / "output_image.mp4"

    if not audio_file.exists() or not image_file.exists():
        return

    viz = ImageAnimatorVisualizer(
        str(audio_file),
        image_file=str(image_file),
        output_file=str(output_file),
        max_duration=2.0
    )

    viz.load_audio()
    viz._load_image()
    viz.compute_amplitude_history()
    viz.generate_frames()
    viz.create_video()

    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_waveform_real_video(tmp_path):
    """Test waveform visualizer with real video generation."""
    test_dir = Path(__file__).parent / "resources"
    audio_file = test_dir / "input.wav"
    output_file = tmp_path / "output_waveform.mp4"

    if not audio_file.exists():
        return

    viz = WaveformVisualizer(
        str(audio_file),
        output_file=str(output_file),
        max_duration=2.0
    )

    viz.load_audio()
    viz.compute_amplitude_history()
    viz.generate_frames()
    viz.create_video()

    assert output_file.exists()
    assert output_file.stat().st_size > 0
