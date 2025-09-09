# Raycast Script Commands

A collection of Python-based Raycast script commands for productivity and automation, now with enhanced error handling, logging, and performance optimizations.

## 🚀 What's New in v0.2.0

- **Enhanced Error Handling**: Comprehensive error handling with retry logic and detailed logging
- **Structured Logging**: Rich console output with structured logging using `structlog`
- **Type Safety**: Full type hints throughout the codebase with MyPy support
- **Configuration Management**: Centralized configuration with Pydantic settings
- **Performance Optimizations**: Connection pooling, caching, and optimized API calls
- **Testing Suite**: Comprehensive unit tests with pytest
- **Development Tools**: Pre-commit hooks, linting, and formatting automation
- **Better CLI**: Enhanced command-line interface with Click

## Commands

### Get Todos from Notes

A Raycast script command that extracts todos from Markdown notes and consolidates them into a single file.

### Polish Clipboard Text

Two variants of a text polishing script that improve and enhance text from your clipboard:

1. **polish-clipboard-text.py** - Uses OpenAI models (requires API key)
2. **polish-clipboard-text-ollama.py** - Uses local Ollama models (no API key needed)

### JIRA Ticket Information

A Raycast script command that fetches comprehensive information from JIRA tickets.

### Speak Clipboard

Text-to-speech scripts with both macOS built-in TTS and OpenAI TTS support:

1. **speak-clipboard.py** - Converts clipboard text to speech using macOS `say` command or OpenAI TTS API
2. **save-clipboard-to-audio.py** - Saves clipboard text as MP3 audio file using macOS TTS or OpenAI TTS API

#### Polish Text Features

- Three polishing modes: Standard Professional, Microsoft Teams Emojis, Regular Emojis
- Maintains original language, meaning, and tone
- Fixes grammar, spelling, and punctuation
- Adds appropriate emojis based on selected mode
- Copies polished text back to clipboard
- Ollama version supports local models: Llama 3.1, Qwen 3, Phi 4, Gemma 3 12B

#### Speak Clipboard Features

**speak-clipboard.py:**
- **Dual TTS Support**: Choose between macOS built-in TTS (`say` command) or OpenAI TTS API
- **Voice Selection**: 10 OpenAI voices available (coral, alloy, echo, fable, nova, onyx, shimmer, ash, ballad, sage)
- Preview of text content before speech generation
- Streaming audio playback for OpenAI TTS
- Comprehensive error handling

**save-clipboard-to-audio.py:**
- **Dual TTS Support**: Save audio files using macOS TTS or OpenAI TTS API
- **Direct MP3 Output**: OpenAI TTS saves directly to MP3, macOS TTS converts via `ffmpeg`
- **Voice Selection**: Same 10 OpenAI voices for file generation
- Timestamped filenames saved to Desktop
- Automatic cleanup of temporary files
- 128k bitrate MP3 compression for macOS TTS

#### JIRA Ticket Features

**jira-ticket-info.py:**
- Fetches ticket title, description, status, and metadata
- Retrieves all comments sorted chronologically (oldest first)
- Shows comment author's first name and timestamp
- Optional AI-powered ticket and comment summarization
- Supports JIRA Cloud and Server instances
- Clear status feedback with emojis

#### Get Todos Features

- Scans all Markdown files (`.md`) in a specified directory
- Extracts unchecked todo items (`* [ ]`)
- Organizes todos by folder and filename
- Saves consolidated todos to `open_todos.md`
- Provides clear status feedback with emojis
- Robust error handling for file access issues

#### Usage

1. **As Raycast Command:**
   - Install the script in Raycast
   - Search for "Get Todos from Notes"
   - Provide the path to your notes folder when prompted

2. **As Standalone Script:**
   ```bash
   python get-todos.py /path/to/your/notes
   ```

#### Output Format

The script creates an `open_todos.md` file with todos organized like this:

```markdown
# Folder Name
## filename.md
* [ ] First todo item
* [ ] Second todo item

## another-file.md
* [ ] Another todo

# Another Folder
## different-file.md
* [ ] More todos
```

## Setup

### Quick Start

1. **Install dependencies:**
   ```bash
   make install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

3. **Install in Raycast:**
   - Copy scripts from `scripts/` directory to your Raycast script commands directory
   - Or use Raycast's "Create Script Command" feature and paste the script content
   - Ensure scripts are executable: `chmod +x scripts/*.py`

### Development Setup

1. **Install development dependencies:**
   ```bash
   make dev-setup
   ```

2. **Run tests:**
   ```bash
   make test
   ```

3. **Format code:**
   ```bash
   make format
   ```

4. **Run linting:**
   ```bash
   make lint
   ```

### Configuration

The application uses a centralized configuration system with the following options:

**Environment Variables (.env file):**
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
MODEL=gpt-4o-mini

# Ollama Configuration  
OLLAMA_MODEL=llama3.1:latest
OLLAMA_BASE_URL=http://localhost:11434

# JIRA Configuration
JIRA_SERVER=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=your_jira_api_token_here

# Application Configuration
LOG_LEVEL=INFO
MAX_RETRIES=3
TIMEOUT=30
```

**API Keys Setup:**
- **OpenAI**: Get your API key from https://platform.openai.com/api-keys
- **JIRA**: Get your API token from your Atlassian account settings

## Requirements

- Python 3.10+
- uv package manager
- macOS (for Raycast integration)
- ffmpeg (for MP3 audio conversion)

### Dependencies

**Core Dependencies:**
- **jira** (>=3.10.5) - JIRA Python SDK for API integration
- **openai** (>=1.102.0) - OpenAI API client library
- **ollama** (>=0.5.3) - Ollama Python client for local models
- **pyperclip** (>=1.9.0) - Cross-platform clipboard utilities
- **python-dotenv** (>=1.1.1) - Environment variable management

**New Dependencies:**
- **pydantic** (>=2.0.0) - Data validation and settings management
- **click** (>=8.0.0) - Command-line interface framework
- **rich** (>=13.0.0) - Rich text and beautiful formatting
- **httpx** (>=0.25.0) - Modern HTTP client
- **tenacity** (>=8.0.0) - Retry library for robust API calls
- **structlog** (>=23.0.0) - Structured logging

**Development Dependencies:**
- **pytest** (>=7.0.0) - Testing framework
- **ruff** (>=0.12.10) - Fast Python linter and code formatter
- **mypy** (>=1.5.0) - Static type checker
- **pre-commit** (>=3.0.0) - Git hooks framework

## Development

### Available Commands

```bash
make help              # Show all available commands
make install           # Install dependencies
make install-dev       # Install development dependencies
make test              # Run tests
make test-coverage     # Run tests with coverage report
make lint              # Run linting (ruff + mypy)
make format            # Format code (black + isort + ruff)
make clean             # Clean build artifacts
make dev-setup         # Set up development environment
```

### Code Quality

The project uses several tools to maintain code quality:

- **Ruff**: Fast Python linter and formatter
- **MyPy**: Static type checking
- **Black**: Code formatting
- **isort**: Import sorting
- **Pre-commit**: Git hooks for automated checks

### Testing

Run the test suite:
```bash
make test
```

Run tests with coverage:
```bash
make test-coverage
```

### Project Structure

```
raycast-script-commands/
├── src/raycast_scripts/          # Main source code
│   ├── __init__.py
│   ├── config.py                 # Configuration management
│   ├── logging.py                # Structured logging
│   ├── utils.py                  # Utility functions
│   ├── get_todos.py              # Todo extraction
│   ├── polish_clipboard_text.py  # OpenAI text polishing
│   ├── polish_clipboard_text_ollama.py  # Ollama text polishing
│   ├── speak_clipboard.py        # Text-to-speech
│   ├── save_clipboard_to_audio.py # Audio file generation
│   └── jira_ticket_info.py       # JIRA integration
├── scripts/                      # Raycast script entry points
├── tests/                        # Test suite
├── pyproject.toml               # Project configuration
├── Makefile                     # Development commands
└── README.md                    # This file
```