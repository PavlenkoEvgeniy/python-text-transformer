"""
GUI module for Text Transformer Pro.

This module handles all GUI-related code, keeping it separate from
the core business logic.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING

from text_transformer.transformer import TextTransformer

if TYPE_CHECKING:
    from text_transformer.transformer import TextTransformerProtocol


class TextTransformerGUI:
    """
    GUI application for the Text Transformer Pro.

    This class manages all GUI components and coordinates with the
    TextTransformer for business logic.

    Attributes:
        transformer: The text transformation engine.
    """

    # Application constants
    APP_TITLE = "Text Transformer Pro"
    WINDOW_WIDTH = 450
    WINDOW_HEIGHT = 420

    # Styling constants
    LABEL_FONT = ("Arial", 10, "bold")
    BUTTON_WIDTH = 12
    TEXT_WIDTH = 45
    TEXT_HEIGHT = 6

    # Colors
    TRANSFORM_BUTTON_COLOR = "#4CAF50"
    TRANSFORM_BUTTON_FG = "white"
    CLEAR_BUTTON_COLOR = "#f44336"
    CLEAR_BUTTON_FG = "white"
    RESULT_TEXT_FG = "blue"
    RESULT_TEXT_BG = "#f0f0f0"

    def __init__(self, transformer: "TextTransformerProtocol | None" = None) -> None:
        """
        Initialize the GUI application.

        Args:
            transformer: Optional text transformer instance. If not provided,
                        a new TextTransformer will be created.
        """
        self.transformer = transformer if transformer else TextTransformer()
        self._root: tk.Tk | None = None
        self._input_area: tk.Text | None = None
        self._result_area: tk.Text | None = None
        self._combo_box: ttk.Combobox | None = None
        self._result_menu: tk.Menu | None = None
        self._input_menu: tk.Menu | None = None

    def run(self) -> None:
        """Start the GUI application main loop."""
        self._create_root_window()
        self._create_menu_bar()
        self._create_context_menus()
        self._create_input_section()
        self._create_operation_section()
        self._create_buttons_section()
        self._create_result_section()
        self._bind_events()

        if self._root:
            self._root.mainloop()

    def _create_root_window(self) -> None:
        """Create and configure the main application window."""
        self._root = tk.Tk()
        self._root.title(self.APP_TITLE)
        self._root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")

    def _create_menu_bar(self) -> None:
        """Create the application menu bar."""
        if not self._root:
            return

        menu_bar = tk.Menu(self._root)
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        self._root.config(menu=menu_bar)

    def _create_context_menus(self) -> None:
        """Create right-click context menus for input and result areas."""
        if not self._root:
            return

        # Result context menu (Copy only)
        self._result_menu = tk.Menu(self._root, tearoff=0)
        self._result_menu.add_command(label="Copy", command=self._copy_text)

        # Input context menu (Paste only)
        self._input_menu = tk.Menu(self._root, tearoff=0)
        self._input_menu.add_command(label="Paste", command=self._paste_text)

    def _create_input_section(self) -> None:
        """Create the input text area section."""
        if not self._root:
            return

        tk.Label(
            self._root,
            text="Enter your text (Right-click to paste):",
            font=self.LABEL_FONT
        ).pack(pady=(10, 0))

        input_frame = tk.Frame(self._root)
        input_frame.pack(pady=5)

        self._input_area = tk.Text(
            input_frame,
            width=self.TEXT_WIDTH,
            height=self.TEXT_HEIGHT,
            wrap=tk.WORD
        )
        input_scroll = ttk.Scrollbar(
            input_frame,
            orient="vertical",
            command=self._input_area.yview
        )
        self._input_area.configure(yscrollcommand=input_scroll.set)

        self._input_area.pack(side="left", fill="both", expand=True)
        input_scroll.pack(side="right", fill="y")

    def _create_operation_section(self) -> None:
        """Create the operation selection dropdown section."""
        if not self._root:
            return

        tk.Label(
            self._root,
            text="Operation:",
            font=self.LABEL_FONT
        ).pack(pady=(10, 0))

        self._combo_box = ttk.Combobox(
            self._root,
            values=self.transformer.get_all_operation_names(),
            state="readonly"
        )
        self._combo_box.set(self.transformer.get_all_operation_names()[0])
        self._combo_box.pack(pady=5)

    def _create_buttons_section(self) -> None:
        """Create the action buttons section."""
        if not self._root:
            return

        btn_frame = tk.Frame(self._root)
        btn_frame.pack(pady=15)

        submit_btn = tk.Button(
            btn_frame,
            text="Transform",
            command=self._transform_text,
            bg=self.TRANSFORM_BUTTON_COLOR,
            fg=self.TRANSFORM_BUTTON_FG,
            width=self.BUTTON_WIDTH
        )
        submit_btn.pack(side="left", padx=5)

        clear_btn = tk.Button(
            btn_frame,
            text="Clear",
            command=self._clear_fields,
            bg=self.CLEAR_BUTTON_COLOR,
            fg=self.CLEAR_BUTTON_FG,
            width=self.BUTTON_WIDTH
        )
        clear_btn.pack(side="left", padx=5)

    def _create_result_section(self) -> None:
        """Create the result display section."""
        if not self._root:
            return

        tk.Label(
            self._root,
            text="Result (Right-click to copy):",
            font=self.LABEL_FONT
        ).pack()

        result_frame = tk.Frame(self._root)
        result_frame.pack(pady=5)

        self._result_area = tk.Text(
            result_frame,
            width=self.TEXT_WIDTH,
            height=self.TEXT_HEIGHT,
            wrap=tk.WORD,
            fg=self.RESULT_TEXT_FG,
            bg=self.RESULT_TEXT_BG
        )
        result_scroll = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self._result_area.yview
        )
        self._result_area.configure(yscrollcommand=result_scroll.set)

        self._result_area.config(state="disabled")
        self._result_area.pack(side="left", fill="both", expand=True)
        result_scroll.pack(side="right", fill="y")

    def _bind_events(self) -> None:
        """Bind event handlers to UI elements."""
        if not self._input_area or not self._result_area:
            return

        # Input Area Bindings (Paste Menu)
        self._input_area.bind("<Button-3>", self._show_input_menu)  # Windows / Linux
        self._input_area.bind("<Button-2>", self._show_input_menu)  # macOS

        # Result Area Bindings (Copy Menu)
        self._result_area.bind("<Button-3>", self._show_result_menu)
        self._result_area.bind("<Button-2>", self._show_result_menu)

    # --- Action Handlers ---

    def _transform_text(self) -> None:
        """Handle the transform button click."""
        if not self._input_area or not self._result_area or not self._combo_box:
            return

        # Get text from input area (1.0 = line 1, char 0; end-1c removes trailing newline)
        input_val = self._input_area.get("1.0", "end-1c")
        operation_name = self._combo_box.get()

        # Get the transformation type enum
        operation = self.transformer.get_operation_from_name(operation_name)

        if operation:
            result = self.transformer.transform(input_val, operation)
        else:
            result = ""

        # Update result area (must enable first, then disable after)
        self._result_area.config(state="normal")
        self._result_area.delete("1.0", tk.END)
        self._result_area.insert(tk.END, result)
        self._result_area.config(state="disabled")

    def _clear_fields(self) -> None:
        """Clear both input and result text areas."""
        if not self._input_area or not self._result_area:
            return

        self._input_area.delete("1.0", tk.END)
        self._result_area.config(state="normal")
        self._result_area.delete("1.0", tk.END)
        self._result_area.config(state="disabled")

    def _show_about(self) -> None:
        """Display the about dialog."""
        about_text = (
            "Text Transformer Pro\n"
            "License: Freeware\n\n"
            "Copyright 2026\n"
            "Author: Pavlenko Evgeny\n"
            "Email: pavlenkoevgeniy85@gmail.com"
        )
        messagebox.showinfo("About", about_text)

    def _copy_text(self) -> None:
        """Copy selected text or entire result to clipboard."""
        if not self._result_area or not self._root:
            return

        try:
            selected_text = self._result_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            selected_text = self._result_area.get("1.0", "end-1c")

        if selected_text:
            self._root.clipboard_clear()
            self._root.clipboard_append(selected_text)

    def _paste_text(self) -> None:
        """Paste text from clipboard into input area."""
        if not self._input_area or not self._root:
            return

        try:
            clipboard_content = self._root.clipboard_get()
            # If text is selected, delete it first
            try:
                self._input_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
            except tk.TclError:
                pass  # No selection

            self._input_area.insert(tk.INSERT, clipboard_content)
        except tk.TclError:
            pass  # Clipboard is empty or doesn't contain text

    def _show_result_menu(self, event: tk.Event) -> None:
        """Display the result context menu."""
        if self._result_menu:
            self._result_menu.tk_popup(event.x_root, event.y_root)

    def _show_input_menu(self, event: tk.Event) -> None:
        """Display the input context menu."""
        if self._input_menu:
            self._input_menu.tk_popup(event.x_root, event.y_root)


def main() -> None:
    """Entry point for running the application."""
    app = TextTransformerGUI()
    app.run()


if __name__ == "__main__":
    main()
