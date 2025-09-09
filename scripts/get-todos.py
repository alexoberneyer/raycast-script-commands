#!/usr/bin/env python3
"""Get Todos from Notes - Extract and consolidate todos from Markdown files."""

# Required parameters
# @raycast.schemaVersion 1
# @raycast.title Get Todos from Notes
# @raycast.mode compact

# Optional parameters
# @raycast.icon 📝
# @raycast.packageName Notes
# @raycast.argument1 { "type": "text", "placeholder": "Path to notes folder" }

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from raycast_scripts.get_todos import main

if __name__ == "__main__":
    # Handle Raycast arguments
    if len(sys.argv) == 2 and not sys.argv[1].startswith("--"):
        # Raycast mode - single argument
        main([sys.argv[1]])
    else:
        # CLI mode
        main()