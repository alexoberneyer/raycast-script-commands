# Raycast Script Commands

Personal [Raycast script commands](https://github.com/raycast/script-commands). Plain shell, no dependencies to install.

## Commands

### Agent in Notes

`agent-in-notes.sh` opens a new [Ghostty](https://ghostty.org) window in `~/Code/notes` and starts the agent picked from the dropdown: Claude, Codex, pi or omp. The window stays open as a shell after the agent quits.

Needs Ghostty and the agents on the login shell's `PATH`.

### Polish Clipboard (Claude)

`polish-clipboard-claude.sh` polishes the text on the clipboard and writes it back. It runs the `writing:polish-text` skill in a headless Claude Code session, so the prompt lives in the skill, not here.

Needs `claude` installed at `~/.local/bin/claude` and logged in. Takes about 10 seconds. A toast says "Polished" or "Not polished, clipboard unchanged".

### Time

Four commands for [timewarrior](https://timewarrior.net). Starting a timer stops the one running.

| Script | Does |
|---|---|
| `time-chosen.sh` | Starts `chosen`, for planned work. Optional title. |
| `time-reactive.sh` | Starts `reactive`, for Teams, mail and interruptions. No prompt. |
| `time-start.sh` | Starts `admin` or `learn` from a dropdown. Optional title. The other two call it. |
| `time-end.sh` | Ends the running timer. |

Each shows one line, such as `reactive · chosen deck review stopped after 1:13`. Run them from Raycast search: `tc`, `tr`, `ts`, `te`.

Needs timewarrior from Homebrew at `/opt/homebrew/bin/timew`. Run `timew :yes` once in a terminal first, or its setup prompt fails without a TTY.

### Workspaces

`aerospace-workspaces.sh` lists every [AeroSpace](https://github.com/nikitabobko/AeroSpace) workspace and the windows open in each. Needs AeroSpace from Homebrew at `/opt/homebrew/bin/aerospace`.

## Setup

1. In Raycast, add this folder as a script directory.
2. Keep the scripts executable: `chmod +x *.sh`.

Raycast runs scripts with a bare `PATH`, so every binary is called by its full path.
