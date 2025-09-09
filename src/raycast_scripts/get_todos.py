#!/usr/bin/env python3
"""Get Todos from Notes - Extract and consolidate todos from Markdown files."""

# Required parameters
# @raycast.schemaVersion 1
# @raycast.title Get Todos from Notes
# @raycast.mode compact

# Optional parameters
# @raycast.icon 📝
# @raycast.packageName Notes
# @raycast.argument1 { "type": "text", "placeholder": "Path to notes folder" }

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Optional

import click
from rich.console import Console

from .config import settings
from .logging import ScriptLogger, configure_logging
from .utils import ensure_directory_exists, print_error, print_info, print_success

console = Console()

MARKDOWN_EXTENSION = ".md"
TODO_IDENTIFIER = "* [ ]"
FILENAME_TODOS = f"open_todos{MARKDOWN_EXTENSION}"


@dataclass
class TodosFromNote:
    """Represents todos extracted from a single note file."""
    folder: str
    filename: str
    todos: List[str]


class TodoExtractor:
    """Handles extraction and processing of todos from Markdown files."""

    def __init__(self, notes_path: Path) -> None:
        """Initialize with notes directory path."""
        self.notes_path = Path(notes_path)
        ensure_directory_exists(self.notes_path)

    def walk_through_notes(self) -> Iterator[Path]:
        """Walk through notes directory and yield Markdown files."""
        for file_path in self.notes_path.rglob(f"*{MARKDOWN_EXTENSION}"):
            if file_path.name != FILENAME_TODOS:
                yield file_path

    def get_todos_from_note(self, note_path: Path) -> Optional[TodosFromNote]:
        """Extract todos from a single note file."""
        try:
            with note_path.open("r", encoding="utf-8") as note_file:
                lines = note_file.readlines()

            todos = [line.strip() for line in lines if TODO_IDENTIFIER in line]
            if todos:
                folder = note_path.parent.name
                return TodosFromNote(folder=folder, filename=note_path.name, todos=todos)
        except (OSError, UnicodeDecodeError) as e:
            console.print(f"❌ Error reading {note_path}: {e}", style="red")
            return None

    def get_all_todos(self) -> List[TodosFromNote]:
        """Extract todos from all notes in the directory."""
        todos = []
        for note_path in self.walk_through_notes():
            if todo_data := self.get_todos_from_note(note_path):
                todos.append(todo_data)
        return todos

    def format_todos(self, todos: List[TodosFromNote]) -> List[str]:
        """Format todos for output."""
        if not todos:
            return []

        # Group by folder
        folders = sorted({todo.folder for todo in todos})
        formatted_todos = []

        for folder in folders:
            formatted_todos.append(f"# {folder}\n")
            files_in_folder = [todo for todo in todos if todo.folder == folder]
            
            for todo_file in files_in_folder:
                formatted_todos.append(f"## {todo_file.filename}\n")
                formatted_todos.extend([todo + "\n" for todo in todo_file.todos])
                formatted_todos.append("\n")
            formatted_todos.append("\n")

        return formatted_todos

    def save_todos(self, todos: List[TodosFromNote]) -> None:
        """Save formatted todos to file."""
        if not todos:
            print_info("No todos found in the specified path")
            return

        output_file = self.notes_path / FILENAME_TODOS
        formatted_todos = self.format_todos(todos)

        try:
            with output_file.open("w", encoding="utf-8") as todo_file:
                todo_file.writelines(formatted_todos)
            
            print_success(f"Saved {len(todos)} todo sections to {output_file}")
        except OSError as e:
            print_error(f"Error saving todos to {output_file}: {e}")
            sys.exit(1)


@click.command()
@click.argument("notes_path", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def main(notes_path: Path, verbose: bool) -> None:
    """Extract and consolidate todos from Markdown notes."""
    if verbose:
        settings.log_level = "DEBUG"
    
    configure_logging()
    
    with ScriptLogger("get-todos", notes_path=str(notes_path), verbose=verbose):
        extractor = TodoExtractor(notes_path)
        todos = extractor.get_all_todos()
        extractor.save_todos(todos)


if __name__ == "__main__":
    # Handle Raycast arguments
    if len(sys.argv) == 2 and not sys.argv[1].startswith("--"):
        # Raycast mode - single argument
        main([sys.argv[1]])
    else:
        # CLI mode
        main()