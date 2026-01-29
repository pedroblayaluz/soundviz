import sys
import argparse
from pathlib import Path
from .processing import BatchProcessor


class VisualizerApp:
    """Command-line application for audio visualization."""

    def __init__(self) -> None:
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(
            description="Convert audio files to video visualizations",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Process single file with waveform visualizer (default)
  python cli.py audio.mp3
  python cli.py audio.mp3 -o output.mp4

  # Process single file with image animator
  python cli.py audio.mp3 -t image
  python cli.py audio.mp3 -t image -o output.mp4

  # Process folder with waveform visualizer
  python cli.py /path/to/audio/folder
  python cli.py /path/to/audio/folder -o /path/to/output/folder

  # Process folder with image animator
  python cli.py /path/to/audio/folder -t image
  python cli.py /path/to/audio/folder -t image -o /path/to/output/folder
            """
        )
        parser.add_argument("input", help="Input audio file or folder")
        parser.add_argument(
            "-o", "--output",
            help="Output file (for single file mode) or folder (for batch mode)"
        )
        parser.add_argument(
            "-t", "--type",
            default="waveform",
            choices=["waveform", "image"],
            help="Visualizer type (default: waveform)"
        )
        parser.add_argument(
            "-d", "--duration",
            type=float,
            default=None,
            help="Maximum duration in seconds (useful for testing)"
        )
        return parser

    def run(self, args: list = None) -> None:
        """Main entry point for the application."""
        parsed_args = self.parser.parse_args(args)
        input_path = Path(parsed_args.input)
        processor = BatchProcessor(visualizer_type=parsed_args.type, max_duration=parsed_args.duration)

        if input_path.is_file():
            processor.process_single_file(input_path, parsed_args.output)
        elif input_path.is_dir():
            processor.process_folder(input_path, parsed_args.output)
        else:
            print(f"Error: {input_path} is not a valid file or directory")
            sys.exit(1)


def main() -> None:
    """Entry point for the CLI application."""
    app = VisualizerApp()
    app.run()


if __name__ == "__main__":
    main()
