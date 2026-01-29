import sys
import argparse
from pathlib import Path
from .processing import BatchProcessor


class VisualizerApp:
    """Command-line application for audio visualization."""

    def __init__(self) -> None:
        self.parser = self._create_parser()
        self.processor = BatchProcessor()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(
            description="Convert audio files to video visualizations",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Process single file
  python cli.py audio.mp3
  python cli.py audio.mp3 -o output.mp4

  # Process folder
  python cli.py /path/to/audio/folder
  python cli.py /path/to/audio/folder -o /path/to/output/folder
            """
        )
        parser.add_argument("input", help="Input audio file or folder")
        parser.add_argument(
            "-o", "--output",
            help="Output file (for single file mode) or folder (for batch mode)"
        )
        return parser

    def run(self, args: list = None) -> None:
        """Main entry point for the application."""
        parsed_args = self.parser.parse_args(args)
        input_path = Path(parsed_args.input)

        if input_path.is_file():
            self.processor.process_single_file(input_path, parsed_args.output)
        elif input_path.is_dir():
            self.processor.process_folder(input_path, parsed_args.output)
        else:
            print(f"Error: {input_path} is not a valid file or directory")
            sys.exit(1)


def main() -> None:
    """Entry point for the CLI application."""
    app = VisualizerApp()
    app.run()


if __name__ == "__main__":
    main()
