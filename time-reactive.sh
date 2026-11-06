#!/bin/zsh

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Time Reactive
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 📨
# @raycast.packageName Time

# Documentation:
# @raycast.description Start a timewarrior timer for Teams, mail and interruptions
# @raycast.author alexoberneyer
# @raycast.authorURL https://github.com/alexoberneyer

exec "${0:A:h}/time-start.sh" reactive
