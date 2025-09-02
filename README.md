# Raycast Script Commands

A collection of Python-based Raycast script commands for productivity and automation.

## Commands

### Get Todos from Notes

A Raycast script command that extracts todos from Markdown notes and consolidates them into a single file.

#### Features

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
   - Copy `get-todos.py` to your Raycast script commands directory
   - Or use Raycast's "Create Script Command" feature and paste the script content
   - Ensure the script is executable: `chmod +x get-todos.py`

## Requirements

- Python 3.10+
- uv package manager
- macOS (for Raycast integration)

### Dependencies

- **openai** (>=1.102.0) - OpenAI API client library
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