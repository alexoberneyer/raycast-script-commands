#!/usr/bin/env python3
"""Save Clipboard to Audio - Save clipboard text as audio file."""

# Required parameters
# @raycast.schemaVersion 1
# @raycast.title Save Clipboard to Audio
# @raycast.mode compact
# @raycast.argument1 {"type": "dropdown", "placeholder": "TTS Engine", "data": [{"title": "macOS Built-in TTS", "value": "macos"}, {"title": "OpenAI TTS", "value": "openai"}]}
# @raycast.argument2 {"type": "dropdown", "placeholder": "Voice (OpenAI only)", "data": [{"title": "Coral", "value": "coral"}, {"title": "Alloy", "value": "alloy"}, {"title": "Echo", "value": "echo"}, {"title": "Fable", "value": "fable"}, {"title": "Nova", "value": "nova"}, {"title": "Onyx", "value": "onyx"}, {"title": "Shimmer", "value": "shimmer"}, {"title": "Ash", "value": "ash"}, {"title": "Ballad", "value": "ballad"}, {"title": "Sage", "value": "sage"}], "optional": true}

# Optional parameters
# @raycast.icon 💾
# @raycast.description Save clipboard text as audio file using macOS TTS or OpenAI
# @raycast.packageName TTS
# @raycast.needsConfirmation false

import tempfile
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional

import click
from openai import OpenAI
from rich.console import Console
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import settings
from .logging import ScriptLogger, configure_logging
from .utils import get_clipboard_text, print_error, print_success, run_ffmpeg_command, run_say_command

console = Console()


class TTSEngine(Enum):
    """Available TTS engines."""
    MACOS = "macos"
    OPENAI = "openai"


class OpenAIVoice(Enum):
    """Available OpenAI voices."""
    CORAL = "coral"
    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    NOVA = "nova"
    ONYX = "onyx"
    SHIMMER = "shimmer"
    ASH = "ash"
    BALLAD = "ballad"
    SAGE = "sage"


class AudioSaver:
    """Handles saving text as audio files."""

    def __init__(self) -> None:
        """Initialize audio saver."""
        self.openai_client: Optional[OpenAI] = None
        if settings.has_openai_config:
            self.openai_client = OpenAI(api_key=settings.openai_api_key)

    def generate_filename(self) -> Path:
        """Generate a unique filename for the audio file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        desktop_path = Path.home() / "Desktop"
        return desktop_path / f"clipboard_audio_{timestamp}.mp3"

    def save_with_builtin_tts(self, text: str, output_path: Path) -> None:
        """Save text to audio file using macOS built-in TTS, converting to MP3."""
        temp_aiff = output_path.with_suffix("_temp.aiff")
        
        console.print(f"🎵 Saving to audio file with macOS TTS: {output_path}", style="blue")
        
        try:
            # Create AIFF with say command
            run_say_command(text, temp_aiff)
            
            # Convert AIFF to MP3 using ffmpeg
            run_ffmpeg_command(temp_aiff, output_path)
            
            # Clean up temporary file
            temp_aiff.unlink()
            
            print_success("Audio file saved successfully!")
            console.print(f"📁 File location: {output_path}", style="green")
        except Exception as e:
            # Clean up temp file if it exists
            if temp_aiff.exists():
                temp_aiff.unlink()
            print_error(f"Failed to save audio: {e}")
            sys.exit(1)

    @retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    def save_with_openai_tts(self, text: str, output_path: Path, voice: OpenAIVoice) -> None:
        """Save text to audio file using OpenAI TTS API."""
        if not self.openai_client:
            print_error("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
            sys.exit(1)

        console.print(f"🎵 Saving to audio file with OpenAI TTS ({voice.value} voice): {output_path}", style="blue")

        try:
            # Create speech and save directly as MP3
            with self.openai_client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts", 
                voice=voice.value, 
                input=text, 
                response_format="mp3"
            ) as response:
                with output_path.open("wb") as f:
                    for chunk in response.iter_bytes():
                        f.write(chunk)

            print_success("Audio file saved successfully!")
            console.print(f"📁 File location: {output_path}", style="green")
        except Exception as e:
            print_error(f"OpenAI TTS save error: {e}")
            sys.exit(1)

    def save_to_audio(self, text: str, output_path: Path, engine: TTSEngine, voice: OpenAIVoice = OpenAIVoice.CORAL) -> None:
        """Save text to audio file using specified TTS engine."""
        if engine == TTSEngine.OPENAI:
            self.save_with_openai_tts(text, output_path, voice)
        else:
            self.save_with_builtin_tts(text, output_path)


@click.command()
@click.option(
    "--engine",
    type=click.Choice([engine.value for engine in TTSEngine]),
    default=TTSEngine.MACOS.value,
    help="TTS engine to use"
)
@click.option(
    "--voice",
    type=click.Choice([voice.value for voice in OpenAIVoice]),
    default=OpenAIVoice.CORAL.value,
    help="OpenAI voice to use"
)
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file path")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def main(engine: str, voice: str, output: Optional[Path], verbose: bool) -> None:
    """Save clipboard text as audio file using macOS TTS or OpenAI."""
    if verbose:
        settings.log_level = "DEBUG"
    
    configure_logging()
    
    tts_engine = TTSEngine(engine)
    openai_voice = OpenAIVoice(voice)
    
    # Get clipboard text
    text = get_clipboard_text()
    
    console.print(
        f"📝 Text to convert ({len(text)} characters): {text[:100]}{'...' if len(text) > 100 else ''}",
        style="blue"
    )
    
    # Generate output path
    output_path = output or AudioSaver().generate_filename()
    
    with ScriptLogger("save-clipboard-to-audio", engine=engine, voice=voice, output=str(output_path), text_length=len(text), verbose=verbose):
        saver = AudioSaver()
        saver.save_to_audio(text, output_path, tts_engine, openai_voice)


if __name__ == "__main__":
    # Handle Raycast arguments
    if len(sys.argv) >= 2:
        # Raycast mode - engine and optional voice
        engine = sys.argv[1]
        voice = sys.argv[2] if len(sys.argv) > 2 else OpenAIVoice.CORAL.value
        main(["--engine", engine, "--voice", voice])
    else:
        # CLI mode
        main()