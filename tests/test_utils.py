"""Tests for utility functions."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from src.raycast_scripts.utils import format_file_size, get_clipboard_text, set_clipboard_text


class TestFileSizeFormatting:
    """Test file size formatting utility."""

    def test_format_file_size_bytes(self):
        """Test formatting bytes."""
        assert format_file_size(0) == "0.0 B"
        assert format_file_size(512) == "512.0 B"

    def test_format_file_size_kb(self):
        """Test formatting kilobytes."""
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(1536) == "1.5 KB"

    def test_format_file_size_mb(self):
        """Test formatting megabytes."""
        assert format_file_size(1024 * 1024) == "1.0 MB"
        assert format_file_size(1024 * 1024 * 2.5) == "2.5 MB"

    def test_format_file_size_gb(self):
        """Test formatting gigabytes."""
        assert format_file_size(1024 * 1024 * 1024) == "1.0 GB"
        assert format_file_size(1024 * 1024 * 1024 * 1.5) == "1.5 GB"


class TestClipboardFunctions:
    """Test clipboard utility functions."""

    @patch("src.raycast_scripts.utils.pyperclip.paste")
    def test_get_clipboard_text_success(self, mock_paste):
        """Test successful clipboard text retrieval."""
        mock_paste.return_value = "test text"
        result = get_clipboard_text()
        assert result == "test text"

    @patch("src.raycast_scripts.utils.pyperclip.paste")
    def test_get_clipboard_text_empty(self, mock_paste):
        """Test empty clipboard text handling."""
        mock_paste.return_value = ""
        with pytest.raises(SystemExit):
            get_clipboard_text()

    @patch("src.raycast_scripts.utils.pyperclip.paste")
    def test_get_clipboard_text_whitespace(self, mock_paste):
        """Test whitespace-only clipboard text handling."""
        mock_paste.return_value = "   \n\t  "
        with pytest.raises(SystemExit):
            get_clipboard_text()

    @patch("src.raycast_scripts.utils.pyperclip.paste")
    def test_get_clipboard_text_error(self, mock_paste):
        """Test clipboard text retrieval error handling."""
        mock_paste.side_effect = Exception("Clipboard error")
        with pytest.raises(SystemExit):
            get_clipboard_text()

    @patch("src.raycast_scripts.utils.pyperclip.copy")
    def test_set_clipboard_text_success(self, mock_copy):
        """Test successful clipboard text setting."""
        set_clipboard_text("test text")
        mock_copy.assert_called_once_with("test text")

    @patch("src.raycast_scripts.utils.pyperclip.copy")
    def test_set_clipboard_text_error(self, mock_copy):
        """Test clipboard text setting error handling."""
        mock_copy.side_effect = Exception("Clipboard error")
        with pytest.raises(SystemExit):
            set_clipboard_text("test text")