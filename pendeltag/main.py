# Huvudfilen

import tkinter as tk
from utils import file_manager as FM
from gui import app as APP

TRAIN_CONFIG_PATH = 'pendeltag/input/train_config.json'

if __name__ == "__main__":
    try:
        train_config = FM.read_file(TRAIN_CONFIG_PATH)
    except Exception as e:
        print(f"Kunde inte läsa train_config: {e}")

    root = tk.Tk()
    app = APP.TimetableApp(root, train_config)
    root.mainloop()