# Functions to read and parse input files

import json

PATH = 'pendeltag/input/train_config.json'

def read_train_config():
    with open(PATH, 'r', encoding='utf-8') as data:
        return json.load(data)