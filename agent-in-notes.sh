#!/bin/zsh

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Agent in Notes
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🧠
# @raycast.packageName Agents
# @raycast.argument1 { "type": "dropdown", "placeholder": "Agent", "data": [{"title": "Claude", "value": "claude"}, {"title": "Codex", "value": "codex"}, {"title": "pi", "value": "pi"}, {"title": "omp", "value": "omp"}] }

# Documentation:
# @raycast.description Open a Claude, Codex, pi or omp session in ~/Code/notes in a new Ghostty window
# @raycast.author alexoberneyer
# @raycast.authorURL https://github.com/alexoberneyer

# A login interactive zsh loads the profile, so each agent is found on the
# user's PATH. exec zsh keeps the window open after the agent quits.
/usr/bin/open -na Ghostty.app --args \
  --working-directory="$HOME/Code/notes" \
  -e /bin/zsh -lic "$1; exec zsh"
