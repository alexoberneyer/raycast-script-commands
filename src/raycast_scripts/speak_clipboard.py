#!/usr/bin/env python3
"""Speak Clipboard - Convert clipboard text to speech."""

# Required parameters
# @raycast.schemaVersion 1
# @raycast.title Speak Clipboard
# @raycast.mode compact
# @raycast.argument1 {"type": "dropdown", "placeholder": "TTS Engine", "data": [{"title": "macOS Built-in TTS", "value": "macos"}, {"title": "OpenAI TTS", "value": "openai"}]}
# @raycast.argument2 {"type": "dropdown", "placeholder": "Voice (OpenAI only)", "data": [{"title": "Coral", "value": "coral"}, {"title": "Alloy", "value": "alloy"}, {"title": "Echo", "value": "echo"}, {"title": "Fable", "value": "fable"}, {"title": "Nova", "value": "nova"}, {"title": "Onyx", "value": "onyx"}, {"title": "Shimmer", "value": "shimmer"}, {"title": "Ash", "value": "ash"}, {"title": "Ballad", "value": "ballad"}, {"title": "Sage", "value": "sage"}], "optional": true}

# Optional parameters
# @raycast.icon 🗣️
# @raycast.description Convert clipboard text to speech using macOS TTS or OpenAI
# @raycast.packageName TTS
# @raycast.needsConfirmation false

import tempfile
from enum import Enum
from pathlib import Path
from typing import Optional

import click
from openai import OpenAI
from rich.console import Console
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import settings
from .logging import ScriptLogger, configure_logging
from .utils import get_clipboard_text, print_error, print_success, run_say_command

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


class TextToSpeech:
    """Handles text-to-speech conversion."""

    def __init__(self) -> None:
        """Initialize TTS handler."""
        self.openai_client: Optional[OpenAI] = None
        if settings.has_openai_config:
            self.openai_client = OpenAI(api_key=settings.openai_api_key)

    def use_builtin_tts(self, text: str) -> None:
        """Use macOS built-in text-to-speech."""
        console.print("🗣️ Using macOS TTS...", style="blue")
        run_say_command(text)
        print_success("Speech completed!")

    @retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    def use_openai_tts(self, text: str, voice: OpenAIVoice) -> None:
        """Use OpenAI text-to-speech API."""
        if not self.openai_client:
            print_error("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
            sys.exit(1)

        console.print(f"🤖 Using OpenAI TTS with {voice.value} voice...", style="blue")

        try:
            # Create speech with streaming to play immediately
            with self.openai_client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts", 
                voice=voice.value, 
                input=text, 
                response_format="wav"
            ) as response:
                # Save to temporary file and play with afplay
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    temp_path = temp_file.name
                    for chunk in response.iter_bytes():
                        temp_file.write(chunk)

                # Play the audio file
                from .utils import run_command
                run_command(["afplay", temp_path], capture_output=True)

                # Clean up temp file
                Path(temp_path).unlink()

            print_success("Speech completed!")
        except Exception as e:
            print_error(f"OpenAI TTS error: {e}")
            sys.exit(1)

    def speak(self, text: str, engine: TTSEngine, voice: OpenAIVoice = OpenAIVoice.CORAL) -> None:
        """Convert text to speech using specified engine."""
        if engine == TTSEngine.OPENAI:
            self.use_openai_tts(text, voice)
        else:
            self.use_builtin_tts(text)


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
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def main(engine: str, voice: str, verbose: bool) -> None:
    """Convert clipboard text to speech using macOS TTS or OpenAI."""
    if verbose:
        settings.log_level = "DEBUG"
    
    configure_logging()
    
    tts_engine = TTSEngine(engine)
    openai_voice = OpenAIVoice(voice)
    
    # Get clipboard text
    text = get_clipboard_text()
    
    console.print(
        f"📝 Text to speak ({len(text)} characters): {text[:100]}{'...' if len(text) > 100 else ''}",
        style="blue"
    )
    
    with ScriptLogger("speak-clipboard", engine=engine, voice=voice, text_length=len(text), verbose=verbose):
        tts = TextToSpeech()
        tts.speak(text, tts_engine, openai_voice)


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