#!/usr/bin/env python3
"""Get JIRA Ticket Info - Fetch comprehensive JIRA ticket information."""

# Required parameters
# @raycast.schemaVersion 1
# @raycast.title Get JIRA Ticket Info
# @raycast.mode fullOutput

# Optional parameters
# @raycast.icon 🎫
# @raycast.description Fetch JIRA ticket details including title, description, and comments
# @raycast.packageName JIRA Integration
# @raycast.needsConfirmation false
# @raycast.argument1 {"type": "text", "placeholder": "Enter JIRA ticket ID (e.g., PROJ-123)"}
# @raycast.argument2 {"type": "dropdown", "placeholder": "Include AI summary?", "data": [{"title": "No summary", "value": "none"}, {"title": "Include AI summary", "value": "summary"}]}

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from raycast_scripts.jira_ticket_info import main

if __name__ == "__main__":
    # Handle Raycast arguments
    if len(sys.argv) >= 3:
        # Raycast mode - ticket ID and summary flag
        ticket_id = sys.argv[1]
        include_summary = sys.argv[2] == "summary"
        main([ticket_id, "--summary" if include_summary else "--no-summary"])
    else:
        # CLI mode
        main()