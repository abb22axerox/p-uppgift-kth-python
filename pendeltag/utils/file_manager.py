# Functions to read and parse input files

import json

def read_file(path):
    with open(path, 'r', encoding='utf-8') as data:
        return json.load(data)

def save_timetable(path, timetable_dict):
    for station in timetable_dict:
        with open(path, 'w') as f:
            json.dump(timetable_dict, f, indent=4)

def clear_file(PATH):
    print('Cleared file!')