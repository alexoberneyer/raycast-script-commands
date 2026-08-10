#!/bin/zsh

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Workspaces
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 🪟
# @raycast.packageName AeroSpace

# Documentation:
# @raycast.description Show every AeroSpace workspace and the windows open in each
# @raycast.author alexoberneyer
# @raycast.authorURL https://github.com/alexoberneyer

# Mirrors the `ws` function in ~/.zshrc. Raycast runs this in a non-interactive
# shell, so the logic is inlined and the binary is called by absolute path
# rather than reusing the shell function.
#
# Workspace names mirror the layout documented in
# ~/.config/aerospace/aerospace.toml — keep them in sync.

AEROSPACE=/opt/homebrew/bin/aerospace
names=(Web Code Comms "Docs & AI")

focused=$($AEROSPACE list-workspaces --focused) || exit 1

for w in $($AEROSPACE list-workspaces --all); do
  [[ $w == $focused ]] && mark="›" || mark=" "
  print "$mark $w  ${names[$w]:-}"
  $AEROSPACE list-windows --workspace "$w" --format '%{app-name}|%{window-title}' \
    | awk -F'|' '{printf "     %-16s %.55s\n", $1, $2}'
done
