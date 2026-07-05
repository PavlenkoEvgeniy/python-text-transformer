import tkinter as tk
from tkinter import messagebox, ttk


def transform_text():
    # Getting text from a Text widget requires '1.0' (line 1, char 0) to tk.END
    # 'end-1c' deletes the extra trailing newline that Tkinter automatically adds
    input_val = input_area.get("1.0", "end-1c")
    operation = combo_box.get()

    if operation == "Uppercase":
        result = input_val.upper()
    elif operation == "Lowercase":
        result = input_val.lower()
    elif operation == "Capitalize":
        result = input_val.capitalize()
    elif operation == "Title":
        result = input_val.title()
    else:
        result = ""

    # Enable the text box, clear previous content, insert new content, then disable it
    result_area.config(state="normal")
    result_area.delete("1.0", tk.END)
    result_area.insert(tk.END, result)
    result_area.config(state="disabled")


def clear_fields():
    """Clears both the input and result text areas."""
    input_area.delete("1.0", tk.END)
    result_area.config(state="normal")
    result_area.delete("1.0", tk.END)
    result_area.config(state="disabled")


def show_about():
    about_text = (
        "Text Transformer Pro\n"
        "License: Freeware\n\n"
        "Copyright 2026\n"
        "Author: Pavlenko Evgeny\n"
        "Email: pavlenkoevgeniy85@gmail.com"
    )
    messagebox.showinfo("About", about_text)


# --- Context Menu Functions ---
def copy_text():
    """Copies selected text, or the whole result if no selection exists."""
    try:
        selected_text = result_area.get(tk.SEL_FIRST, tk.SEL_LAST)
    except tk.TclError:
        selected_text = result_area.get("1.0", "end-1c")

    if selected_text:
        root.clipboard_clear()
        root.clipboard_append(selected_text)


def paste_text():
    """Pastes text from the clipboard into the input area at the cursor position."""
    try:
        clipboard_content = root.clipboard_get()
        # If text is selected in input_area, delete it first to replace it
        try:
            input_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass  # No selection, just insert at cursor

        input_area.insert(tk.INSERT, clipboard_content)
    except tk.TclError:
        pass  # Clipboard is empty or doesn't contain text


def show_result_menu(event):
    """Displays the result context menu at the mouse click coordinates."""
    result_menu.tk_popup(event.x_root, event.y_root)


def show_input_menu(event):
    """Displays the input context menu at the mouse click coordinates."""
    input_menu.tk_popup(event.x_root, event.y_root)


# GUI Setup
root = tk.Tk()
root.title("Text Transformer Pro")
root.geometry("450x420")

# Menu Bar Setup
menu_bar = tk.Menu(root)
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menu_bar)

# --- Create Right-Click Context Menus ---
# Result context menu (Copy only)
result_menu = tk.Menu(root, tearoff=0)
result_menu.add_command(label="Copy", command=copy_text)

# Input context menu (Paste only)
input_menu = tk.Menu(root, tearoff=0)
input_menu.add_command(label="Paste", command=paste_text)

# Input Section
tk.Label(root, text="Enter your text (Right-click to paste):", font=("Arial", 10, "bold")).pack(
    pady=(10, 0)
)
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

input_area = tk.Text(input_frame, width=45, height=6, wrap=tk.WORD)
input_scroll = ttk.Scrollbar(
    input_frame, orient="vertical", command=input_area.yview
)
input_area.configure(yscrollcommand=input_scroll.set)

input_area.pack(side="left", fill="both", expand=True)
input_scroll.pack(side="right", fill="y")

# Selection Section
tk.Label(root, text="Operation:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
combo_box = ttk.Combobox(
    root, values=["Uppercase", "Lowercase", "Capitalize", "Title"], state="readonly"
)
combo_box.set("Uppercase")
combo_box.pack(pady=5)

# Buttons Section
btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)

submit_btn = tk.Button(
    btn_frame,
    text="Transform",
    command=transform_text,
    bg="#4CAF50",
    fg="white",
    width=12,
)
submit_btn.pack(side="left", padx=5)

clear_btn = tk.Button(
    btn_frame,
    text="Clear",
    command=clear_fields,
    bg="#f44336",
    fg="white",
    width=12,
)
clear_btn.pack(side="left", padx=5)

# Result Section
tk.Label(root, text="Result (Right-click to copy):", font=("Arial", 10, "bold")).pack()
result_frame = tk.Frame(root)
result_frame.pack(pady=5)

result_area = tk.Text(
    result_frame, width=45, height=6, wrap=tk.WORD, fg="blue", bg="#f0f0f0"
)
result_scroll = ttk.Scrollbar(
    result_frame, orient="vertical", command=result_area.yview
)
result_area.configure(yscrollcommand=result_scroll.set)

result_area.config(state="disabled")
result_area.pack(side="left", fill="both", expand=True)
result_scroll.pack(side="right", fill="y")

# --- Bindings for Right-Click Context Menus ---
# Input Area Bindings (Paste Menu)
input_area.bind("<Button-3>", show_input_menu)  # Windows / Linux right-click
input_area.bind("<Button-2>", show_input_menu)  # macOS right-click

# Result Area Bindings (Copy Menu)
result_area.bind("<Button-3>", show_result_menu)
result_area.bind("<Button-2>", show_result_menu)

root.mainloop()