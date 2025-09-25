# The main program entry point

from utils import file_manager as FM
from utils import compute_save_timetable as CST

TRAIN_CONFIG_PATH = 'pendeltag/input/train_config.json'
TIMETABLE_PATH = 'pendeltag/output/timetable.json'

data = FM.read_file(TRAIN_CONFIG_PATH)

exported_time_table = CST.compute_timetable(data)
FM.save_timetable(TIMETABLE_PATH, exported_time_table)