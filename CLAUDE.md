# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project for Raycast script commands, managed using uv (an extremely fast Python package manager). The project contains Python-based Raycast script commands for productivity automation, including todo extraction from Markdown notes, clipboard text polishing using both OpenAI and local Ollama models, text-to-speech conversion using macOS TTS, and JIRA ticket information retrieval.

## Project Structure

- `pyproject.toml` - Project configuration and dependencies
- `uv.lock` - Lock file for reproducible dependency installations
- `README.md` - Project documentation with setup and usage instructions
- `get-todos.py` - Raycast script command for extracting todos from Markdown notes
- `polish-clipboard-text.py` - Raycast script for polishing clipboard text using OpenAI
- `polish-clipboard-text-ollama.py` - Raycast script for polishing clipboard text using local Ollama models
- `speak-clipboard.py` - Raycast script for converting clipboard text to speech using macOS TTS
- `save-clipboard-to-audio.py` - Raycast script for saving clipboard text as MP3 audio files
- `jira-ticket-info.py` - Raycast script for fetching JIRA ticket information and comments
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
- **jira** (>=3.10.5) - JIRA Python SDK for API integration
- **openai** (>=1.102.0) - OpenAI API client library
- **ollama** (>=0.5.3) - Ollama Python client for local models
- **pyperclip** (>=1.9.0) - Cross-platform clipboard utilities
- **python-dotenv** (>=1.1.1) - Environment variable management
- **ruff** (>=0.12.10) - Fast Python linter and code formatter

## Development Notes

- This project uses uv for dependency management instead of pip/conda
- The project targets Python >=3.10
- Code formatting and linting are handled by ruff
- No test framework is currently configured
- All scripts should be executable and include proper Raycast metadata headers
- Scripts should handle command-line arguments for standalone usage
- Use proper error handling with clear status messages and emojis for user feedback

## Raycast Script Commands

### get-todos.py
- **Purpose**: Extracts unchecked todo items from Markdown notes and consolidates them
- **Input**: Path to notes folder (as command-line argument or Raycast input)
- **Output**: Creates `open_todos.md` with organized todos by folder/file
- **Usage**: Can be run standalone or as Raycast command
- **Features**: UTF-8 encoding, error handling, emoji status messages

### polish-clipboard-text.py
- **Purpose**: Polishes and improves clipboard text using OpenAI models
- **Input**: Text from clipboard, polishing mode selection
- **Output**: Improved text copied back to clipboard
- **Usage**: Raycast command with dropdown selections for mode
- **Features**: Three polishing modes, OpenAI API integration, emoji enhancement options

### polish-clipboard-text-ollama.py
- **Purpose**: Polishes and improves clipboard text using local Ollama models
- **Input**: Text from clipboard, polishing mode and model selection
- **Output**: Improved text copied back to clipboard
- **Usage**: Raycast command with dropdown selections for mode and model
- **Features**: Three polishing modes, local model support (Llama 3.1, Qwen 3, Phi 4, Gemma 3 12B), no API key required

### speak-clipboard.py
- **Purpose**: Converts clipboard text to speech using macOS built-in TTS
- **Input**: Text from clipboard (automatically retrieved)
- **Output**: Audio playback of synthesized speech
- **Usage**: Raycast command with compact mode for user feedback
- **Features**: 
  - Uses macOS built-in TTS (`say` command)
  - Simple and reliable text-to-speech conversion
  - Graceful error handling
  - Preview of text content before speech generation

### save-clipboard-to-audio.py
- **Purpose**: Saves clipboard text as MP3 audio files using macOS TTS
- **Input**: Text from clipboard (automatically retrieved)
- **Output**: MP3 audio file saved to Desktop with timestamped filename
- **Usage**: Raycast command with compact mode for user feedback
- **Features**:
  - Uses macOS built-in TTS (`say` command) with `ffmpeg` conversion
  - Saves compressed MP3 files (128k bitrate) to Desktop
  - Timestamped filenames (e.g., `clipboard_audio_20250904_163755.mp3`)
  - Automatic cleanup of temporary AIFF files
  - Error handling and clear status messages
  - Requires `ffmpeg` for MP3 conversion

### jira-ticket-info.py
- **Purpose**: Fetches comprehensive JIRA ticket information including title, description, and all comments
- **Input**: JIRA ticket ID (e.g., "PROJ-123") and optional AI summary flag
- **Output**: Formatted ticket details with chronologically sorted comments and optional AI summary
- **Usage**: Raycast command with text input for ticket ID and dropdown for summary option
- **Features**:
  - Retrieves ticket title, description, status, assignee, reporter, and timestamps
  - Shows all comments sorted chronologically (oldest first) with author's first name
  - Optional OpenAI-powered summarization of ticket and comments using GPT-4o-mini
  - Supports both JIRA Cloud and Server instances
  - Comprehensive error handling with clear status messages
  - Requires JIRA_SERVER, JIRA_EMAIL, and JIRA_API_TOKEN environment variables
  - Optional OPENAI_API_KEY for AI summary feature