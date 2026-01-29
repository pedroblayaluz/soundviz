"""Batch processing of audio files for visualization."""

import sys
from pathlib import Path
from ..visualization import AudioVisualizer


class BatchProcessor:
    """Handles batch processing of audio files to video visualizations."""

    AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aiff"}

    def process_single_file(
        self, audio_file: Path, output_file: str = None
    ) -> None:
        """Process a single audio file.

        Args:
            audio_file: Path to the audio file
            output_file: Output video file path (defaults to audio_name_output.mp4)
        """
        if output_file is None:
            output_file = f"{audio_file.stem}_output.mp4"

        print(f"Processing single file: {audio_file}")
        try:
            visualizer = AudioVisualizer(str(audio_file), str(output_file))
            visualizer.run()
            print(f"✓ Successfully saved to: {output_file}")
        except Exception as e:
            print(f"✗ Error processing {audio_file.name}: {e}")
            sys.exit(1)

    def process_folder(
        self, input_folder: Path, output_folder: str = None
    ) -> None:
        """Process all audio files in a folder.

        Args:
            input_folder: Path to folder containing audio files
            output_folder: Output folder path (defaults to input_folder_output)
        """
        if output_folder is None:
            output_folder = Path(
                input_folder.parent
            ) / f"{input_folder.name}_output"
        else:
            output_folder = Path(output_folder)

        # Create output folder if it doesn't exist
        output_folder.mkdir(parents=True, exist_ok=True)
        print(f"Processing folder: {input_folder}")
        print(f"Output folder: {output_folder}\n")

        # Find all audio files
        audio_files = [
            f for f in input_folder.rglob("*")
            if f.suffix.lower() in self.AUDIO_EXTENSIONS
        ]

        if not audio_files:
            print(f"No audio files found in {input_folder}")
            sys.exit(1)

        print(f"Found {len(audio_files)} audio file(s)\n")

        # Process each audio file
        successful = 0
        failed = 0

        for idx, audio_file in enumerate(audio_files, 1):
            try:
                print(f"[{idx}/{len(audio_files)}] Processing: {audio_file.name}")
                output_file = output_folder / f"{audio_file.stem}.mp4"
                visualizer = AudioVisualizer(str(audio_file), str(output_file))
                visualizer.run()
                print(f"✓ Completed: {output_file}\n")
                successful += 1
            except Exception as e:
                print(f"✗ Error processing {audio_file.name}: {e}\n")
                failed += 1

        # Print summary
        self._print_summary(successful, len(audio_files), failed, output_folder)

    @staticmethod
    def _print_summary(
        successful: int, total: int, failed: int, output_folder: Path
    ) -> None:
        """Print batch processing summary.

        Args:
            successful: Number of successfully processed files
            total: Total number of files processed
            failed: Number of failed files
            output_folder: Path to the output folder
        """
        print("Batch processing complete!")
        print(f"  Successful: {successful}/{total}")
        if failed > 0:
            print(f"  Failed: {failed}/{total}")
        print(f"  Output folder: {output_folder}")
