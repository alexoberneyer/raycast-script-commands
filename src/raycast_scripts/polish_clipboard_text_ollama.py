#!/usr/bin/env python3
"""Polish Clipboard Text (Ollama) - Improve text using local Ollama models."""

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

import sys
from enum import Enum
from typing import Dict, Optional

import click
import ollama
from rich.console import Console
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import settings
from .logging import ScriptLogger, configure_logging
from .utils import get_clipboard_text, print_error, print_success, set_clipboard_text

console = Console()


class PolishingMode(Enum):
    """Available text polishing modes."""
    STANDARD = "1"
    TEAMS_EMOJIS = "2"
    REGULAR_EMOJIS = "3"


class OllamaTextPolisher:
    """Handles text polishing using local Ollama models."""

    def __init__(self) -> None:
        """Initialize with Ollama client."""
        self.model = settings.ollama_model
        self.base_url = settings.ollama_base_url

    def _get_prompt_template(self, mode: PolishingMode) -> str:
        """Get prompt template for the specified mode."""
        templates = {
            PolishingMode.STANDARD: """Polish and improve the following text. Make it more clear, professional, and well-structured while maintaining the original language, meaning and tone. Fix any grammar, spelling, or punctuation issues. Return only the polished text without any introduction or explanation:

{text}""",
            
            PolishingMode.TEAMS_EMOJIS: """Polish and improve the following text. Make it more clear, professional, and well-structured while maintaining the original language, meaning and tone. Fix any grammar, spelling, or punctuation issues. Additionally, enhance the text by adding appropriate Microsoft Teams emojis from this list where suitable:
- (smile) for positive/happy content
- (y) for approval/thumbsup
- (rocket) for progress/launch/success
- (wink) for light humor
- (thinkingface) for consideration/reflection  
- (rofl) for very funny content
- (lol) for funny content

Return only the polished text without any introduction or explanation:

{text}""",
            
            PolishingMode.REGULAR_EMOJIS: """Polish and improve the following text. Make it more clear, professional, and well-structured while maintaining the original language, meaning and tone. Fix any grammar, spelling, or punctuation issues. Additionally, enhance the text by adding appropriate emojis where suitable:
- 😃 for positive/happy content
- 👍 for approval/thumbsup
- 🚀 for progress/launch/success
- 😉 for light humor
- 🤔 for consideration/reflection
- 🤣 for very funny content
- 😂 for funny content

Return only the polished text without any introduction or explanation:

{text}"""
        }
        return templates[mode]

    @retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    def polish_text(self, text: str, mode: PolishingMode) -> str:
        """Polish text using Ollama API with retry logic."""
        prompt = self._get_prompt_template(mode).format(text=text)
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"base_url": self.base_url}
            )
            return response["message"]["content"].strip()
        except Exception as e:
            console.print(f"❌ Ollama API error: {e}", style="red")
            raise

    def process_clipboard(self, mode: PolishingMode) -> None:
        """Process clipboard text with the specified mode."""
        # Get clipboard content
        clipboard_content = get_clipboard_text()
        
        console.print(f"✨ Polishing text with local Ollama model ({self.model})...", style="blue")
        
        # Polish the text
        polished_text = self.polish_text(clipboard_content, mode)
        
        # Copy back to clipboard
        set_clipboard_text(polished_text)
        
        print_success(f"Text polished with {self.model} and copied to clipboard!")


@click.command()
@click.option(
    "--mode",
    type=click.Choice([mode.value for mode in PolishingMode]),
    default=PolishingMode.STANDARD.value,
    help="Polishing mode to use"
)
@click.option("--model", help="Ollama model to use (overrides config)")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def main(mode: str, model: Optional[str], verbose: bool) -> None:
    """Polish and improve text from clipboard using local Ollama models."""
    if verbose:
        settings.log_level = "DEBUG"
    
    if model:
        settings.ollama_model = model
    
    configure_logging()
    
    polishing_mode = PolishingMode(mode)
    
    with ScriptLogger("polish-clipboard-text-ollama", mode=mode, model=settings.ollama_model, verbose=verbose):
        polisher = OllamaTextPolisher()
        polisher.process_clipboard(polishing_mode)


if __name__ == "__main__":
    # Handle Raycast arguments
    if len(sys.argv) == 2 and sys.argv[1] in ["1", "2", "3"]:
        # Raycast mode - single argument
        main(["--mode", sys.argv[1]])
    else:
        # CLI mode
        main()