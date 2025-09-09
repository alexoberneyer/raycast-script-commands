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

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from raycast_scripts.speak_clipboard import main

if __name__ == "__main__":
    # Handle Raycast arguments
    if len(sys.argv) >= 2:
        # Raycast mode - engine and optional voice
        engine = sys.argv[1]
        voice = sys.argv[2] if len(sys.argv) > 2 else "coral"
        main(["--engine", engine, "--voice", voice])
    else:
        # CLI mode
        main()