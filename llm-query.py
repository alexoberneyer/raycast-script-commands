#!/Users/alex/Code/raycast-script-commands/.venv/bin/python

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title LLM Query
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 🤖
# @raycast.argument1 { "type": "text", "placeholder": "Prompt", "optional": false }
# @raycast.argument2 { "type": "dropdown", "placeholder": "Model", "optional": true, "data": [{"title": "gpt-5", "value": "gpt-5"}, {"title": "gpt-5-codex", "value": "openai/gpt-5-codex"}, {"title": "grok", "value": "grok-4-latest"}, {"title": "gemini-pro", "value": "gemini/gemini-2.5-pro"}, {"title": "sonnet-45", "value": "anthropic/claude-sonnet-4-5"}, {"title": "opus-41", "value": "anthropic/claude-opus-4-1-20250805"}] }

# Documentation:
# @raycast.description Query LLM models using the llm CLI tool
# @raycast.author alexoberneyer
# @raycast.authorURL https://github.com/alexoberneyer

import os
import subprocess
import sys
import pyperclip
from dotenv import load_dotenv


def main():
    # Load environment variables
    load_dotenv()

    prompt = sys.argv[1] if len(sys.argv) > 1 else None
    model = sys.argv[2] if len(sys.argv) > 2 else None

    if not prompt:
        print("❌ Prompt is required")
        sys.exit(1)

    # Get LLM path from environment or use default
    llm_path = os.getenv("LLM_PATH", "/Users/alex/.local/bin/llm")

    try:
        # Build the command - use path from env
        cmd = [llm_path]
        if model:
            cmd.extend(["-m", model])
        cmd.append(prompt)

        # Execute the llm command
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Get the output and save to clipboard
        output = result.stdout.strip()
        pyperclip.copy(output)

        # Output the result
        print(output)
        print("📋 Copied to clipboard")

    except subprocess.CalledProcessError as e:
        print(f"❌ LLM command failed: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print(
            "❌ llm CLI tool not found. Please install it: https://llm.datasette.io/en/stable/"
        )
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
