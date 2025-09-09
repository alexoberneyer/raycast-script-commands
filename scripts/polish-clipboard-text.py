#!/usr/bin/env python3
"""Polish Clipboard Text - Improve text using OpenAI models."""

# Required parameters
# @raycast.schemaVersion 1
# @raycast.title Polish Clipboard Text
# @raycast.mode compact

# Optional parameters
# @raycast.icon ✨
# @raycast.description Polish and improve text from clipboard using AI
# @raycast.packageName Text Processing
# @raycast.needsConfirmation false
# @raycast.argument1 {"type": "dropdown", "placeholder": "Select polishing mode", "data": [{"title": "Standard Professional", "value": "1"}, {"title": "Microsoft Teams Emojis", "value": "2"}, {"title": "Regular Emojis", "value": "3"}]}

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from raycast_scripts.polish_clipboard_text import main

if __name__ == "__main__":
    # Handle Raycast arguments
    if len(sys.argv) == 2 and sys.argv[1] in ["1", "2", "3"]:
        # Raycast mode - single argument
        main(["--mode", sys.argv[1]])
    else:
        # CLI mode
        main()