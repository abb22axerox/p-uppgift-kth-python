# Handle configured data and timetable

from utils import calculator as C

from classes import timetable as TT
from classes import train as TR

def compute_timetable(data):
    conf_a = data['acceleration']
    conf_r = data['retardation']
    conf_vmax = data['max_speed']
    conf_start_time = data['start_time']
    conf_day_type = data['day_type']
    stations = data['stops']
    distance_deltas = C.calculate_distance_deltas(stations)
    conf_wait_time = data['wait_time_end_station']

    train = TR.Train(conf_vmax, conf_a, conf_r)

    table = TT.Timetable(stations, train, conf_day_type)
    table.create_timetable(conf_start_time, distance_deltas, conf_wait_time)
    exported_time_table = table.timetable

    return exported_time_table