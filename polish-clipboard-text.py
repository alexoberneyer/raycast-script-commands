#!/Users/alex/Code/raycast-script-commands/.venv/bin/python

# Required parameters
# @raycast.schemaVersion 1
# @raycast.title Polish Clipboard Text
# @raycast.mode compact

# Optional parameters
# @raycast.icon ✨
# @raycast.description Polish and improve text from clipboard using AI
# @raycast.packageName Text Processing
# @raycast.needsConfirmation false

import os
import sys
import pyperclip
from openai import OpenAI
from dotenv import load_dotenv


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Check for OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(
            "❌ OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
        )
        sys.exit(1)

    try:
        # Get clipboard content
        clipboard_content = pyperclip.paste()

        if not clipboard_content or not clipboard_content.strip():
            print("❌ Clipboard is empty or contains no text.")
            sys.exit(1)

        print("✨ Polishing text...")

        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)

        # Create input for text polishing
        input_text = f"""Please polish and improve the following text. Make it more clear, professional, and well-structured while maintaining the original language, meaning and tone. Fix any grammar, spelling, or punctuation issues:

{clipboard_content}"""

        # Call OpenAI API using GPT-5 responses API
        response = client.responses.create(
            model="gpt-5",
            input=input_text,
            text={"verbosity": "low"},
        )

        # Extract polished text
        polished_text = response.output_text.strip()

        # Copy polished text back to clipboard
        pyperclip.copy(polished_text)

        print("✅ Text polished and copied to clipboard!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
