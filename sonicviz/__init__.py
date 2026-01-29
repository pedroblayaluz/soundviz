"""SonicViz - Audio-driven visual effects and transformations."""

__version__ = "0.1.0"
__author__ = "Pedro Blaya Luz"

from .visualization import AudioVisualizer
from .processing import BatchProcessor

__all__ = ["AudioVisualizer", "BatchProcessor"]
