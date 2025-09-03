# Raycast Script Commands

A collection of Python-based Raycast script commands for productivity and automation.

## Commands

### Get Todos from Notes

A Raycast script command that extracts todos from Markdown notes and consolidates them into a single file.

### Polish Clipboard Text

Two variants of a text polishing script that improve and enhance text from your clipboard:

1. **polish-clipboard-text.py** - Uses OpenAI models (requires API key)
2. **polish-clipboard-text-ollama.py** - Uses local Ollama models (no API key needed)

#### Features

- Three polishing modes: Standard Professional, Microsoft Teams Emojis, Regular Emojis
- Maintains original language, meaning, and tone
- Fixes grammar, spelling, and punctuation
- Adds appropriate emojis based on selected mode
- Copies polished text back to clipboard
- Ollama version supports local models: Llama 3.1, Qwen 3, Phi 4, Gemma 3 12B

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

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Install in Raycast:**
   - Copy scripts to your Raycast script commands directory
   - Or use Raycast's "Create Script Command" feature and paste the script content
   - Ensure scripts are executable: `chmod +x *.py`

## Requirements

- Python 3.10+
- uv package manager
- macOS (for Raycast integration)

### Dependencies

- **openai** (>=1.102.0) - OpenAI API client library
- **ollama** (>=0.5.3) - Ollama Python client for local models
- **pyperclip** (>=1.9.0) - Cross-platform clipboard utilities  
- **python-dotenv** (>=1.1.1) - Environment variable management
- **ruff** (>=0.12.10) - Fast Python linter and code formatter

## Development

Run linting and formatting:
```bash
uv run ruff check          # Check for issues
uv run ruff check --fix    # Auto-fix issues
uv run ruff format         # Format code
```