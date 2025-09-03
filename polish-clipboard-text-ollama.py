#!/Users/alex/Code/raycast-script-commands/.venv/bin/python

# Required parameters
# @raycast.schemaVersion 1
# @raycast.title Polish Clipboard Text (Ollama)
# @raycast.mode compact

# Optional parameters
# @raycast.icon ✨
# @raycast.description Polish and improve text from clipboard using local Ollama models
# @raycast.packageName Text Processing
# @raycast.needsConfirmation false
# @raycast.argument1 {"type": "dropdown", "placeholder": "Select polishing mode", "data": [{"title": "Standard Professional", "value": "1"}, {"title": "Microsoft Teams Emojis", "value": "2"}, {"title": "Regular Emojis", "value": "3"}]}

import os
import sys
import pyperclip
import ollama
from dotenv import load_dotenv


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get model from environment variable
    model = os.environ.get("OLLAMA_MODEL", "llama3.1:latest")

    # Get mode selection from Raycast argument (default to standard professional)
    choice = sys.argv[1] if len(sys.argv) > 1 else "1"
    if choice not in ["1", "2", "3"]:
        choice = "1"

    try:
        # Get clipboard content
        clipboard_content = pyperclip.paste()

        if not clipboard_content or not clipboard_content.strip():
            print("❌ Clipboard is empty or contains no text.")
            sys.exit(1)

        print("✨ Polishing text with local Ollama model...")

        # Create input for text polishing based on selected mode
        if choice == "1":
            prompt = f"""Polish and improve the following text. Make it more clear, professional, and well-structured while maintaining the original language, meaning and tone. Fix any grammar, spelling, or punctuation issues. Return only the polished text without any introduction or explanation:

{clipboard_content}"""
        elif choice == "2":
            prompt = f"""Polish and improve the following text. Make it more clear, professional, and well-structured while maintaining the original language, meaning and tone. Fix any grammar, spelling, or punctuation issues. Additionally, enhance the text by adding appropriate Microsoft Teams emojis from this list where suitable:
- (smile) for positive/happy content
- (y) for approval/thumbsup
- (rocket) for progress/launch/success
- (wink) for light humor
- (thinkingface) for consideration/reflection  
- (rofl) for very funny content
- (lol) for funny content

Return only the polished text without any introduction or explanation:

{clipboard_content}"""
        else:  # choice == "3"
            prompt = f"""Polish and improve the following text. Make it more clear, professional, and well-structured while maintaining the original language, meaning and tone. Fix any grammar, spelling, or punctuation issues. Additionally, enhance the text by adding appropriate emojis where suitable:
- 😃 for positive/happy content
- 👍 for approval/thumbsup
- 🚀 for progress/launch/success
- 😉 for light humor
- 🤔 for consideration/reflection
- 🤣 for very funny content
- 😂 for funny content

Return only the polished text without any introduction or explanation:

{clipboard_content}"""

        # Call Ollama API
        response = ollama.chat(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )

        # Extract polished text
        polished_text = response['message']['content'].strip()

        # Copy polished text back to clipboard
        pyperclip.copy(polished_text)

        print(f"✅ Text polished with {model} and copied to clipboard!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()