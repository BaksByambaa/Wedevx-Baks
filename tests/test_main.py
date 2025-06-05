"""Tests for the main module."""

from cursor_project.main import greet

def test_greet():
    """Test the greet function."""
    assert greet("Alice") == "Hello, Alice! Welcome to Cursor Python Project!"
    assert greet("Bob") == "Hello, Bob! Welcome to Cursor Python Project!" 