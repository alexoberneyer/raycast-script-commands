# Polish Clipboard Text

A Raycast script command that uses OpenAI's API to polish and improve text from your clipboard.

## Features

- Reads text from clipboard
- Uses OpenAI's GPT-4o-mini model to improve grammar, spelling, and clarity
- Maintains original meaning and tone
- Copies polished text back to clipboard
- Provides clear status feedback

## Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Set up OpenAI API key:**
   - Get your API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)
   - Set the environment variable:
     ```bash
     export OPENAI_API_KEY="your-api-key-here"
     ```
   - Or add it to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.)

3. **Install in Raycast:**
   - Copy the script to your Raycast script commands directory
   - Or use Raycast's "Create Script Command" feature and paste the script content

## Usage

1. Copy any text to your clipboard
2. Run the command from Raycast (search for "Polish Clipboard Text")
3. The polished text will replace the original content in your clipboard

## Requirements

- Python 3.10+
- OpenAI API key
- Internet connection
- macOS (for clipboard functionality)

## Error Handling

The script will show clear error messages for:
- Missing OpenAI API key
- Empty clipboard
- API errors or network issues