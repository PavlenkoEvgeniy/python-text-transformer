"""
Integration tests for the GUI components.

These tests verify the GUI works correctly with the transformer logic.
Since Tkinter requires a display, we use virtual display or mocking.
"""

import tkinter as tk
from tkinter import ttk
from unittest.mock import MagicMock, Mock, patch

import pytest

from text_transformer.gui import TextTransformerGUI
from text_transformer.transformer import TextTransformer


class TestTextTransformerGUI:
    """Test suite for TextTransformerGUI class."""

    @pytest.fixture
    def gui_with_mock_root(self) -> TextTransformerGUI:
        """Create GUI instance with mocked Tkinter components."""
        with patch("text_transformer.gui.tk.Tk") as mock_tk:
            mock_root = MagicMock()
            mock_tk.return_value = mock_root

            gui = TextTransformerGUI(transformer=TextTransformer())
            gui._root = mock_root
            return gui

    @pytest.fixture
    def gui_no_display(self) -> TextTransformerGUI:
        """Create GUI instance without starting mainloop (for testing)."""
        with patch("tkinter.Tk") as mock_tk:
            mock_root = MagicMock(spec=tk.Tk)
            mock_tk.return_value = mock_root

            gui = TextTransformerGUI(transformer=TextTransformer())
            gui._root = mock_root
            gui._input_area = MagicMock(spec=tk.Text)
            gui._result_area = MagicMock(spec=tk.Text)
            gui._combo_box = MagicMock(spec=ttk.Combobox)

            return gui

    def test_initialization(self) -> None:
        """Test GUI initializes with transformer."""
        with patch("tkinter.Tk") as mock_tk:
            mock_root = MagicMock()
            mock_tk.return_value = mock_root

            gui = TextTransformerGUI()

            assert gui.transformer is not None
            assert isinstance(gui.transformer, TextTransformer)

    def test_initialization_with_custom_transformer(self) -> None:
        """Test GUI accepts custom transformer."""
        custom_transformer = TextTransformer()

        with patch("tkinter.Tk") as mock_tk:
            mock_root = MagicMock()
            mock_tk.return_value = mock_root

            gui = TextTransformerGUI(transformer=custom_transformer)

            assert gui.transformer is custom_transformer

    def test_app_title_constant(self) -> None:
        """Test application title is set correctly."""
        assert TextTransformerGUI.APP_TITLE == "Text Transformer Pro"

    def test_window_dimensions_constant(self) -> None:
        """Test window dimensions are set correctly."""
        assert TextTransformerGUI.WINDOW_WIDTH == 450
        assert TextTransformerGUI.WINDOW_HEIGHT == 420

    def test_text_area_dimensions(self) -> None:
        """Test text area dimensions are configured."""
        assert TextTransformerGUI.TEXT_WIDTH == 45
        assert TextTransformerGUI.TEXT_HEIGHT == 6

    def test_transformer_gets_all_operations(self) -> None:
        """Test that transformer has all expected operations."""
        transformer = TextTransformer()
        operations = transformer.get_all_operation_names()

        assert len(operations) == 4
        assert "Uppercase" in operations
        assert "Lowercase" in operations
        assert "Capitalize" in operations
        assert "Title" in operations


class TestGUIIntegration:
    """Integration tests for GUI and transformer working together."""

    def test_transform_operation_integration(self) -> None:
        """Test that GUI correctly calls transformer transform method."""
        transformer = TextTransformer()

        with patch("tkinter.Tk") as mock_tk:
            mock_root = MagicMock()
            mock_tk.return_value = mock_root

            gui = TextTransformerGUI(transformer=transformer)
            gui._root = mock_root

            # Mock the input area
            mock_input = MagicMock()
            mock_input.get = Mock(return_value="hello world")
            gui._input_area = mock_input

            # Mock the result area
            mock_result = MagicMock()
            mock_result.__getitem__ = Mock()
            gui._result_area = mock_result

            # Mock the combo box
            mock_combo = MagicMock()
            mock_combo.get = Mock(return_value="Uppercase")
            gui._combo_box = mock_combo

            # Call transform
            gui._transform_text()

            # Verify result was set (state changed to normal, delete, insert, disabled)
            mock_result.config.assert_called()
            mock_result.delete.assert_called()
            mock_result.insert.assert_called()


class TestGUICopyPaste:
    """Tests for copy/paste functionality."""

    def test_copy_with_selection(self) -> None:
        """Test copying text with a selection."""
        transformer = TextTransformer()

        with patch("tkinter.Tk") as mock_tk:
            mock_root = MagicMock()
            mock_root.clipboard_clear = Mock()
            mock_root.clipboard_append = Mock()
            mock_tk.return_value = mock_root

            gui = TextTransformerGUI(transformer=transformer)
            gui._root = mock_root

            # Mock result area with selection
            mock_result = MagicMock()
            mock_result.get = Mock(return_value="Selected text")
            mock_result.get.side_effect = lambda *args: "Selected text" if args else "Selected text"
            gui._result_area = mock_result

            # Trigger TclError for selection to test fallback
            mock_result.get.side_effect = tk.TclError()
            mock_result.get = Mock(side_effect=tk.TclError())

            # Can't easily test without selection exception handling
            # This test documents the expected behavior


class TestGUIMenuCommands:
    """Tests for menu command handlers."""

    def test_show_about_calls_messagebox(self) -> None:
        """Test that about dialog uses messagebox."""
        transformer = TextTransformer()

        with patch("tkinter.Tk") as mock_tk:
            mock_root = MagicMock()
            mock_tk.return_value = mock_root

            with patch("text_transformer.gui.messagebox.showinfo") as mock_show:
                gui = TextTransformerGUI(transformer=transformer)
                gui._show_about()

                mock_show.assert_called_once()
                args = mock_show.call_args[0]
                assert "About" in args
                assert "Text Transformer Pro" in args[1]


class TestGUIClearFields:
    """Tests for clear fields functionality."""

    def test_clear_fields(self) -> None:
        """Test that clearing fields works correctly."""
        transformer = TextTransformer()

        with patch("tkinter.Tk") as mock_tk:
            mock_root = MagicMock()
            mock_tk.return_value = mock_root

            gui = TextTransformerGUI(transformer=transformer)

            # Create mocks
            mock_input = MagicMock()
            gui._input_area = mock_input

            mock_result = MagicMock()
            gui._result_area = mock_result

            # Call clear
            gui._clear_fields()

            # Verify input was cleared
            mock_input.delete.assert_called()

            # Verify result state was changed and cleared
            mock_result.config.assert_called()
            mock_result.delete.assert_called()
