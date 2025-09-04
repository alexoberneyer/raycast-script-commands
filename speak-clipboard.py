#!/Users/alex/Code/raycast-script-commands/.venv/bin/python
# Required parameters
# @raycast.schemaVersion 1
# @raycast.title Speak Clipboard
# @raycast.mode compact

# Optional parameters
# @raycast.icon 🗣️
# @raycast.description Convert clipboard text to speech using macOS TTS
# @raycast.packageName TTS
# @raycast.needsConfirmation false

import subprocess
import sys
from dotenv import load_dotenv

load_dotenv()


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


def speak(text: str):
    """Convert text to speech using macOS built-in TTS."""
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


def main():
    """Main function to get clipboard text and speak it."""
    text = get_clipboard_text()

    if not text:
        print("📋 Clipboard is empty or contains no text.")
        sys.exit(1)

    print(
        f"📝 Text to speak ({len(text)} characters): {text[:100]}{'...' if len(text) > 100 else ''}"
    )
    speak(text)


if __name__ == "__main__":
    main()
