#!/bin/sh
''''exec "$(dirname "$0")/.venv/bin/python" "$0" "$@" #'''
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

import subprocess
import sys
import os
import tempfile
from openai import OpenAI
from dotenv import load_dotenv


def get_clipboard_text() -> str:
    """Get text from clipboard using pbpaste."""
    try:
        result = subprocess.run(["pbpaste"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to get clipboard content: {e}")
        return ""
    except Exception as e:
        print(f"❌ Unexpected error getting clipboard: {e}")
        return ""


def speak(text: str, engine: str = "macos", voice: str = "coral"):
    """Convert text to speech using specified engine."""
    if engine == "openai":
        use_openai_tts(text, voice)
    else:
        use_builtin_tts(text)


def use_builtin_tts(text: str):
    """macOS built-in text-to-speech."""
    try:
        print("🗣️ Using macOS TTS...")
        subprocess.run(["say", text], check=True, capture_output=True)
        print("✅ Speech completed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ TTS failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ TTS error: {e}")
        sys.exit(1)


def use_openai_tts(text: str, voice: str = "coral"):
    """OpenAI text-to-speech API."""
    try:
        # Load environment variables
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print(
                "❌ OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
            )
            sys.exit(1)

        print(f"🤖 Using OpenAI TTS with {voice} voice...")

        client = OpenAI(api_key=api_key)

        # Create speech with streaming to play immediately
        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts", voice=voice, input=text, response_format="wav"
        ) as response:
            # Save to temporary file and play with afplay
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
                for chunk in response.iter_bytes():
                    temp_file.write(chunk)

            # Play the audio file
            subprocess.run(["afplay", temp_path], check=True, capture_output=True)

            # Clean up temp file
            os.unlink(temp_path)

        print("✅ Speech completed!")

    except Exception as e:
        print(f"❌ OpenAI TTS error: {e}")
        sys.exit(1)


def main():
    """Main function to get clipboard text and speak it."""
    # Parse command line arguments
    engine = sys.argv[1] if len(sys.argv) > 1 else "macos"
    voice = sys.argv[2] if len(sys.argv) > 2 else "coral"

    text = get_clipboard_text()

    if not text:
        print("📋 Clipboard is empty or contains no text.")
        sys.exit(1)

    print(
        f"📝 Text to speak ({len(text)} characters): {text[:100]}{'...' if len(text) > 100 else ''}"
    )
    speak(text, engine, voice)


if __name__ == "__main__":
    main()
