# The main program entry point

import tkinter as tk
from utils import file_manager as FM
from utils import compute_save_timetable as CST
from gui import app as APP

TRAIN_CONFIG_PATH = 'pendeltag/input/train_config.json'
TIMETABLE_PATH = 'pendeltag/output/timetable.json'

if __name__ == "__main__":
    data = FM.read_file(TRAIN_CONFIG_PATH)

    exported_timetable = CST.compute_timetable(data)
    FM.save_timetable(TIMETABLE_PATH, exported_timetable)
    train_config = FM.read_file(TRAIN_CONFIG_PATH)

    loaded_timetable = FM.read_file(TIMETABLE_PATH)

    root = tk.Tk()
    app = APP.TimetableApp(root, train_config, loaded_timetable)
    root.mainloop()