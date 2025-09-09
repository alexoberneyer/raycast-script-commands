"""Tests for get-todos functionality."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from src.raycast_scripts.get_todos import TodoExtractor, TodosFromNote


class TestTodoExtractor:
    """Test TodoExtractor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.extractor = TodoExtractor(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_walk_through_notes(self):
        """Test walking through notes directory."""
        # Create test files
        (self.temp_dir / "test1.md").write_text("# Test 1\n* [ ] Todo 1\n* [ ] Todo 2")
        (self.temp_dir / "test2.md").write_text("# Test 2\n* [ ] Todo 3")
        (self.temp_dir / "open_todos.md").write_text("# Existing todos")
        (self.temp_dir / "not_md.txt").write_text("Not a markdown file")

        # Test walking
        files = list(self.extractor.walk_through_notes())
        assert len(files) == 2
        assert all(f.suffix == ".md" for f in files)
        assert not any(f.name == "open_todos.md" for f in files)

    def test_get_todos_from_note_success(self):
        """Test successful todo extraction from a note."""
        test_file = self.temp_dir / "test.md"
        test_file.write_text("# Test\n* [ ] Todo 1\n* [ ] Todo 2\n* [x] Done todo")

        result = self.extractor.get_todos_from_note(test_file)
        
        assert result is not None
        assert result.folder == self.temp_dir.name
        assert result.filename == "test.md"
        assert len(result.todos) == 2
        assert "* [ ] Todo 1" in result.todos
        assert "* [ ] Todo 2" in result.todos

    def test_get_todos_from_note_no_todos(self):
        """Test note with no todos."""
        test_file = self.temp_dir / "test.md"
        test_file.write_text("# Test\nNo todos here")

        result = self.extractor.get_todos_from_note(test_file)
        assert result is None

    def test_get_todos_from_nonexistent_file(self):
        """Test handling of nonexistent file."""
        test_file = self.temp_dir / "nonexistent.md"
        result = self.extractor.get_todos_from_note(test_file)
        assert result is None

    def test_format_todos(self):
        """Test todo formatting."""
        todos = [
            TodosFromNote(folder="folder1", filename="file1.md", todos=["* [ ] Todo 1", "* [ ] Todo 2"]),
            TodosFromNote(folder="folder1", filename="file2.md", todos=["* [ ] Todo 3"]),
            TodosFromNote(folder="folder2", filename="file3.md", todos=["* [ ] Todo 4"]),
        ]

        formatted = self.extractor.format_todos(todos)
        
        assert "# folder1\n" in formatted
        assert "# folder2\n" in formatted
        assert "## file1.md\n" in formatted
        assert "## file2.md\n" in formatted
        assert "## file3.md\n" in formatted
        assert "* [ ] Todo 1\n" in formatted
        assert "* [ ] Todo 2\n" in formatted
        assert "* [ ] Todo 3\n" in formatted
        assert "* [ ] Todo 4\n" in formatted

    def test_format_todos_empty(self):
        """Test formatting empty todos list."""
        formatted = self.extractor.format_todos([])
        assert formatted == []

    def test_save_todos(self):
        """Test saving todos to file."""
        todos = [
            TodosFromNote(folder="folder1", filename="file1.md", todos=["* [ ] Todo 1"]),
        ]

        self.extractor.save_todos(todos)
        
        output_file = self.temp_dir / "open_todos.md"
        assert output_file.exists()
        content = output_file.read_text()
        assert "# folder1\n" in content
        assert "## file1.md\n" in content
        assert "* [ ] Todo 1\n" in content

    def test_save_todos_empty(self):
        """Test saving empty todos list."""
        with patch("src.raycast_scripts.get_todos.print_info") as mock_print:
            self.extractor.save_todos([])
            mock_print.assert_called_once_with("No todos found in the specified path")