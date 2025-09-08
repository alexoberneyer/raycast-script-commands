#!/Users/alex/Code/raycast-script-commands/.venv/bin/python
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

import subprocess
import sys
import os
from datetime import datetime
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


def save_to_audio(
    text: str, output_path: str, engine: str = "macos", voice: str = "coral"
):
    """Save text to audio file using specified TTS engine."""
    if engine == "openai":
        save_with_openai_tts(text, output_path, voice)
    else:
        save_with_builtin_tts(text, output_path)


def save_with_builtin_tts(text: str, output_path: str):
    """Save text to audio file using macOS built-in TTS, converting to MP3."""
    try:
        # Generate temporary AIFF file
        temp_aiff = output_path.replace(".mp3", "_temp.aiff")

        print(f"🎵 Saving to audio file with macOS TTS: {output_path}")

        # Create AIFF with say command
        subprocess.run(["say", "-o", temp_aiff, text], check=True, capture_output=True)

        # Convert AIFF to MP3 using ffmpeg
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                temp_aiff,
                "-codec:a",
                "libmp3lame",
                "-b:a",
                "128k",
                output_path,
                "-y",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Clean up temporary file
        os.remove(temp_aiff)

        print("✅ Audio file saved successfully!")
        print(f"📁 File location: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to save audio: {e}")
        # Clean up temp file if it exists
        temp_aiff = output_path.replace(".mp3", "_temp.aiff")
        if os.path.exists(temp_aiff):
            os.remove(temp_aiff)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Audio save error: {e}")
        sys.exit(1)


def save_with_openai_tts(text: str, output_path: str, voice: str = "coral"):
    """Save text to audio file using OpenAI TTS API."""
    try:
        # Load environment variables
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print(
                "❌ OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
            )
            sys.exit(1)

        print(f"🎵 Saving to audio file with OpenAI TTS ({voice} voice): {output_path}")

        client = OpenAI(api_key=api_key)

        # Create speech and save directly as MP3
        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts", voice=voice, input=text, response_format="mp3"
        ) as response:
            with open(output_path, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)

        print("✅ Audio file saved successfully!")
        print(f"📁 File location: {output_path}")

    except Exception as e:
        print(f"❌ OpenAI TTS save error: {e}")
        sys.exit(1)


def generate_filename() -> str:
    """Generate a unique filename for the audio file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    desktop_path = os.path.expanduser("~/Desktop")
    return os.path.join(desktop_path, f"clipboard_audio_{timestamp}.mp3")


def main():
    """Main function to get clipboard text and save it as audio."""
    # Parse command line arguments
    engine = sys.argv[1] if len(sys.argv) > 1 else "macos"
    voice = sys.argv[2] if len(sys.argv) > 2 else "coral"

    text = get_clipboard_text()

    if not text:
        print("📋 Clipboard is empty or contains no text.")
        sys.exit(1)

    print(
        f"📝 Text to convert ({len(text)} characters): {text[:100]}{'...' if len(text) > 100 else ''}"
    )

    output_path = generate_filename()
    save_to_audio(text, output_path, engine, voice)


if __name__ == "__main__":
    main()
