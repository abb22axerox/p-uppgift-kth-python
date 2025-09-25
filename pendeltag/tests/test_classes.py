import sys
sys.path.insert(0, '/Users/axelroxenborg/Documents/Programmering/p-uppgift-kth-python/pendeltag')

TIMETABLE_PATH = 'pendeltag/output/timetable.json'

from utils import file_manager as FM

print(FM.read_file(TIMETABLE_PATH))