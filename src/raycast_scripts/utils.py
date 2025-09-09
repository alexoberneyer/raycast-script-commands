"""Utility functions for Raycast scripts."""

import subprocess
import sys
from pathlib import Path
from typing import Optional

import pyperclip
from rich.console import Console
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import settings
from .logging import get_logger

logger = get_logger(__name__)
console = Console()


def get_clipboard_text() -> str:
    """Get text from clipboard with error handling."""
    try:
        text = pyperclip.paste()
        if not text or not text.strip():
            console.print("❌ Clipboard is empty or contains no text.", style="red")
            sys.exit(1)
        return text.strip()
    except Exception as e:
        logger.error("Failed to get clipboard content", error=str(e))
        console.print(f"❌ Failed to get clipboard content: {e}", style="red")
        sys.exit(1)


def set_clipboard_text(text: str) -> None:
    """Set text to clipboard with error handling."""
    try:
        pyperclip.copy(text)
        logger.info("Text copied to clipboard", length=len(text))
    except Exception as e:
        logger.error("Failed to set clipboard content", error=str(e))
        console.print(f"❌ Failed to copy text to clipboard: {e}", style="red")
        sys.exit(1)


@retry(
    stop=stop_after_attempt(settings.max_retries),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True,
)
def run_command(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run a command with retry logic."""
    logger.debug("Running command", command=cmd, kwargs=kwargs)
    return subprocess.run(cmd, check=True, **kwargs)


def run_say_command(text: str, output_file: Optional[Path] = None) -> None:
    """Run macOS say command with proper error handling."""
    cmd = ["say"]
    if output_file:
        cmd.extend(["-o", str(output_file)])
    cmd.append(text)
    
    try:
        run_command(cmd, capture_output=True)
        logger.info("TTS completed successfully", output_file=str(output_file) if output_file else None)
    except subprocess.CalledProcessError as e:
        logger.error("TTS command failed", error=str(e), stderr=e.stderr)
        console.print(f"❌ TTS failed: {e}", style="red")
        sys.exit(1)


def run_ffmpeg_command(input_file: Path, output_file: Path, **options) -> None:
    """Run ffmpeg command with proper error handling."""
    cmd = [
        "ffmpeg",
        "-i", str(input_file),
        "-codec:a", "libmp3lame",
        "-b:a", "128k",
        str(output_file),
        "-y",
    ]
    
    try:
        run_command(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        logger.info("FFmpeg conversion completed", input=str(input_file), output=str(output_file))
    except subprocess.CalledProcessError as e:
        logger.error("FFmpeg conversion failed", error=str(e))
        console.print(f"❌ Audio conversion failed: {e}", style="red")
        sys.exit(1)


def ensure_file_exists(file_path: Path) -> None:
    """Ensure file exists, exit if not."""
    if not file_path.exists():
        console.print(f"❌ File does not exist: {file_path}", style="red")
        sys.exit(1)


def ensure_directory_exists(dir_path: Path) -> None:
    """Ensure directory exists, exit if not."""
    if not dir_path.exists():
        console.print(f"❌ Directory does not exist: {dir_path}", style="red")
        sys.exit(1)
    if not dir_path.is_dir():
        console.print(f"❌ Path is not a directory: {dir_path}", style="red")
        sys.exit(1)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def print_success(message: str) -> None:
    """Print success message with styling."""
    console.print(f"✅ {message}", style="green bold")


def print_error(message: str) -> None:
    """Print error message with styling."""
    console.print(f"❌ {message}", style="red bold")


def print_info(message: str) -> None:
    """Print info message with styling."""
    console.print(f"ℹ️ {message}", style="blue")


def print_warning(message: str) -> None:
    """Print warning message with styling."""
    console.print(f"⚠️ {message}", style="yellow")