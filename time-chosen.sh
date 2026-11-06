#!/bin/zsh

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Time Chosen
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🎯
# @raycast.packageName Time
# @raycast.argument1 { "type": "text", "placeholder": "Title", "optional": true }

# Documentation:
# @raycast.description Start a timewarrior timer for planned work, with an optional title
# @raycast.author alexoberneyer
# @raycast.authorURL https://github.com/alexoberneyer

exec "${0:A:h}/time-start.sh" chosen "$1"
