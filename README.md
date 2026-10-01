# Raycast Script Commands

Personal [Raycast script commands](https://github.com/raycast/script-commands). Plain shell, no dependencies to install.

## Commands

### Polish Clipboard (Claude)

`polish-clipboard-claude.sh` polishes the text on the clipboard and writes it back. It runs the `writing:polish-text` skill in a headless Claude Code session, so the prompt lives in the skill, not here.

Needs `claude` installed at `~/.local/bin/claude` and logged in. Takes about 10 seconds. A toast says "Polished" or "Not polished, clipboard unchanged".

### Workspaces

`aerospace-workspaces.sh` lists every [AeroSpace](https://github.com/nikitabobko/AeroSpace) workspace and the windows open in each. Needs AeroSpace from Homebrew at `/opt/homebrew/bin/aerospace`.

## Setup

1. In Raycast, add this folder as a script directory.
2. Keep the scripts executable: `chmod +x *.sh`.

Raycast runs scripts with a bare `PATH`, so every binary is called by its full path.
