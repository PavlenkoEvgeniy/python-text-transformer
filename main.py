"""
Legacy entry point for backward compatibility.

This file is kept for users who previously ran `python main.py`.
For new installations, prefer:
    python -m text_transformer.gui
or after installing:
    text-transformer
"""

from text_transformer.gui import main

if __name__ == "__main__":
    main()
