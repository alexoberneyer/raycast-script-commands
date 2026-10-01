#!/bin/zsh

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Polish Clipboard (Claude)
# @raycast.mode silent

# Optional parameters:
# @raycast.icon ✍️
# @raycast.packageName Writing

# Documentation:
# @raycast.description Polish the clipboard text with the writing:polish-text skill in a headless Claude session
# @raycast.author alexoberneyer
# @raycast.authorURL https://github.com/alexoberneyer

# The skill holds the prompt and runs pbcopy itself. Claude's stdout is
# discarded because it can carry a greeting from the global CLAUDE.md.
# Claude finds its login through USER, which a bare environment may lack.
export USER="${USER:-$(id -un)}"
cd "${TMPDIR:-/tmp}" || exit 1

before=$(pbpaste)
"$HOME/.local/bin/claude" -p "/writing:polish-text" \
  --allowedTools "Bash(pbpaste:*)" "Bash(pbcopy:*)" </dev/null >/dev/null 2>&1

if [[ "$(pbpaste)" != "$before" ]]; then
  echo "Polished"
else
  echo "Not polished, clipboard unchanged"
fi
