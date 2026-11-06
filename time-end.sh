#!/bin/zsh

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Time End
# @raycast.mode silent

# Optional parameters:
# @raycast.icon ⏹️
# @raycast.packageName Time

# Documentation:
# @raycast.description End the running timewarrior timer
# @raycast.author alexoberneyer
# @raycast.authorURL https://github.com/alexoberneyer

timew=/opt/homebrew/bin/timew

out=$("$timew" stop </dev/null 2>&1)
code=$?

if [[ "$out" == "There is no active time tracking."* ]]; then
  echo "Nothing running"
  exit 0
fi
if (( code != 0 )); then
  print -r -- "${out%%$'\n'*}"
  exit $code
fi

print -r -- "$out" | /usr/bin/awk '
  /^Recorded / { sub(/^Recorded /, ""); rec = $0 }
  $1 == "Total" { tot = $2; sub(/:[0-9]+$/, "", tot) }
  END { gsub(/"/, "", rec); print rec " stopped after " tot }'
