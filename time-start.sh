#!/bin/zsh

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Time Start
# @raycast.mode silent

# Optional parameters:
# @raycast.icon ⏱️
# @raycast.packageName Time
# @raycast.argument1 { "type": "dropdown", "placeholder": "Tag", "data": [{"title": "admin", "value": "admin"}, {"title": "learn", "value": "learn"}] }
# @raycast.argument2 { "type": "text", "placeholder": "Title", "optional": true }

# Documentation:
# @raycast.description Start a timewarrior timer with a tag and an optional title. Stops the one running.
# @raycast.author alexoberneyer
# @raycast.authorURL https://github.com/alexoberneyer

# Time Chosen and Time Reactive call this script, so the summary line is
# built in one place. timewarrior stops the running timer by itself.
timew=/opt/homebrew/bin/timew

if [[ -n "$2" ]]; then
  out=$("$timew" start "$1" "$2" </dev/null 2>&1)
else
  out=$("$timew" start "$1" </dev/null 2>&1)
fi
code=$?

if (( code != 0 )); then
  print -r -- "${out%%$'\n'*}"
  exit $code
fi

# "Recorded <tags>" and its "Total h:mm:ss" describe the stopped timer.
# "Tracking <tags>" is the new one. Quotes around multi-word titles go.
print -r -- "$out" | /usr/bin/awk '
  /^Recorded / { sub(/^Recorded /, ""); rec = $0; inrec = 1; next }
  /^Tracking / { sub(/^Tracking /, ""); trk = $0; inrec = 0; next }
  inrec && $1 == "Total" { tot = $2; sub(/:[0-9]+$/, "", tot) }
  END {
    gsub(/"/, "", rec); gsub(/"/, "", trk)
    line = trk
    if (rec != "") line = line " · " rec " stopped after " tot
    print line
  }'
