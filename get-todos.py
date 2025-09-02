#!/usr/bin/env python3

# Required parameters
# @raycast.schemaVersion 1
# @raycast.title Get Todos from Notes
# @raycast.mode compact

# Optional parameters
# @raycast.icon 📝
# @raycast.packageName Notes
# @raycast.argument1 { "type": "text", "placeholder": "Path to notes folder" }

import os
import sys
from dataclasses import dataclass
from typing import Iterator, List, Optional

MARKDOWN_EXTENSION = ".md"
TODO_IDENTIFIER = "* [ ]"
FILENAME_TODOS = f"open_todos{MARKDOWN_EXTENSION}"


@dataclass
class TodosFromNote:
    folder: str
    filename: str
    todos: list


def walk_through_notes(path: str) -> Iterator[str]:
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(MARKDOWN_EXTENSION) and filename != FILENAME_TODOS:
                yield os.path.join(dirpath, filename)


def get_todos_from_note(note_path: str) -> Optional[TodosFromNote]:
    try:
        absolute_folder, filename = os.path.split(note_path)
        folder = os.path.split(absolute_folder)[1]
        with open(note_path, "r", encoding="utf-8") as note_file:
            lines = note_file.readlines()
        if todos_in_file := [line.strip() for line in lines if TODO_IDENTIFIER in line]:
            return TodosFromNote(folder=folder, filename=filename, todos=todos_in_file)
    except (OSError, UnicodeDecodeError) as e:
        print(f"Error reading {note_path}: {e}", file=sys.stderr)
        return None


def get_todos_from_path(path: str) -> list:
    return [
        todos_from_one_note
        for note_path in walk_through_notes(path)
        if (todos_from_one_note := get_todos_from_note(note_path))
    ]


def format_single_todo(line: str) -> str:
    return line.split("; folder: ")[0] + "\n"


def format_todos(todos: List[TodosFromNote]) -> list:
    folders = list({todo.folder for todo in todos})
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


def save_todos_in_one_file(path: str, todos: list) -> None:
    try:
        path_todo_file = os.path.join(path, FILENAME_TODOS)
        formatted_todos = format_todos(todos)
        with open(path_todo_file, "w", encoding="utf-8") as todo_file:
            todo_file.writelines(formatted_todos)
        print(f"✅ Saved {len(todos)} todo sections to {path_todo_file}")
    except OSError as e:
        print(f"❌ Error saving todos to {path}: {e}", file=sys.stderr)
        sys.exit(1)


def save_todos_from_notes_in_one_file(path: str) -> None:
    if not os.path.exists(path):
        print(f"❌ Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(path):
        print(f"❌ Path is not a directory: {path}", file=sys.stderr)
        sys.exit(1)

    todos = get_todos_from_path(path)
    if not todos:
        print("ℹ️ No todos found in the specified path")
        return

    save_todos_in_one_file(path, todos)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Please provide the path to your notes folder", file=sys.stderr)
        sys.exit(1)

    notes_path = sys.argv[1]
    save_todos_from_notes_in_one_file(notes_path)
