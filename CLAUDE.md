# CLAUDE.md

Personal Raycast script commands, plain shell. See `README.md` for what each one does.

- Raycast runs scripts with a bare `PATH` (`/usr/bin:/bin:/usr/sbin:/sbin`) and no TTY. Call every other binary by its full path, home-relative where possible (`$HOME/.local/bin/claude`).
- The repo is public. No absolute paths under `/Users/`, no secrets.
- Every script needs the Raycast metadata header. Copy it from an existing script.
- Test a script the way Raycast runs it: `env -i HOME="$HOME" PATH=/usr/bin:/bin:/usr/sbin:/sbin ./script.sh`.
