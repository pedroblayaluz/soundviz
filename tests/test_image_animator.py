"""Tests for image animator visualizer."""

from sonicviz.visualization.image_animator import ImageAnimatorVisualizer


def test_image_animator_initialization(temp_audio_file, temp_image_file, temp_output_file):
    """Test ImageAnimatorVisualizer initialization."""
    viz = ImageAnimatorVisualizer(
        temp_audio_file,
        image_file=temp_image_file,
        output_file=temp_output_file
    )

    assert viz.audio_file == temp_audio_file
    assert viz.image_file == temp_image_file
    assert viz.output_file == temp_output_file


def test_image_animator_constants():
    """Test that ImageAnimatorVisualizer has expected constants."""
    assert ImageAnimatorVisualizer.MIN_SCALE == 0.8
    assert ImageAnimatorVisualizer.MAX_SCALE == 1.2
    assert ImageAnimatorVisualizer.MIN_SATURATION == 0.0
    assert ImageAnimatorVisualizer.MAX_SATURATION == 2.0
    assert ImageAnimatorVisualizer.INTENSITY_THRESHOLD == 0.05


def test_image_animator_load_image(temp_audio_file, temp_image_file, temp_output_file):
    """Test image loading."""
    viz = ImageAnimatorVisualizer(
        temp_audio_file,
        image_file=temp_image_file,
        output_file=temp_output_file
    )

    viz._load_image()

    assert viz.base_image is not None
    assert viz.frame_width is not None
    assert viz.frame_height is not None


def test_image_animator_full_pipeline(temp_audio_file, temp_image_file, temp_output_file):
    """Test complete image animation pipeline."""
    viz = ImageAnimatorVisualizer(
        temp_audio_file,
        image_file=temp_image_file,
        output_file=temp_output_file,
        max_duration=0.5
    )

    # Load audio
    viz.load_audio()
    assert viz.y is not None

    # Load image
    viz._load_image()
    assert viz.base_image is not None

    # Compute amplitude
    viz.compute_amplitude_history()
    assert len(viz.amplitude_history) > 0

    # Generate frames (skip actual video creation)
    viz.generate_frames()
    assert len(viz.frames) > 0


def test_image_animator_frame_generation(temp_audio_file, temp_image_file, temp_output_file):
    """Test that frames are generated with correct shape."""
    viz = ImageAnimatorVisualizer(
        temp_audio_file,
        image_file=temp_image_file,
        output_file=temp_output_file,
        max_duration=0.3
    )

    viz.load_audio()
    viz._load_image()
    viz.compute_amplitude_history()
    viz.generate_frames()

    # All frames should have same dimensions
    if len(viz.frames) > 1:
        first_frame = viz.frames[0]
        for frame in viz.frames[1:]:
            assert frame.shape == first_frame.shape
