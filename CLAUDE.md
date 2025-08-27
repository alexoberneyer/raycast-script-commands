# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project for Raycast script commands, managed using uv (an extremely fast Python package manager). The project is currently in early setup phase with minimal dependencies.

## Project Structure

- `pyproject.toml` - Project configuration and dependencies
- `uv.lock` - Lock file for reproducible dependency installations
- `README.md` - Empty project readme
- `.venv/` - Virtual environment (auto-managed by uv)

## Development Commands

### Environment Setup
```bash
uv sync                    # Install dependencies and sync environment
```

### Code Quality
```bash
uv run ruff check          # Run linting checks
uv run ruff check --fix    # Run linting with auto-fixes
uv run ruff format         # Format code
```

### Running Python Code
```bash
uv run <command>           # Run any command in the project environment
uv run python <script>     # Run a Python script
uv run -m <module>         # Run a Python module
```

### Dependency Management
```bash
uv add <package>           # Add a new dependency
uv remove <package>        # Remove a dependency
uv lock                    # Update lock file
```

## Dependencies

The project currently uses:
- **ruff** (>=0.12.10) - Fast Python linter and code formatter

## Development Notes

- This project uses uv for dependency management instead of pip/conda
- The project targets Python >=3.10
- Code formatting and linting are handled by ruff
- No test framework is currently configured
- The project appears to be in initial setup phase with no actual script commands implemented yet