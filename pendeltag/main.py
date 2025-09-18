# The main program entry point

from utils import file_reader as FR
from utils import calculator as C
from utils import time_utils as TU

# Timetable class (core logic)
class Timetable:
    def __init__(self, stations, distance_deltas, train, start_time, day_type):
        self.stations = stations
        self.train = train
        self.day_type = day_type
        self.timetable = dict()

        departure_times = C.calculate_departure_for_stations(distance_deltas, train.vmax, train.a, train.r)
        formatted_departure_times= TU.format_times(departure_times, start_time)

        print(formatted_departure_times)

# Train class
class Train:
    def __init__(self, vmax, a, r):
        self.vmax = vmax
        self.a = a
        self.r = r

    def travel_time(self, s):
        return C.calculate_travel_time(s, self.vmax, self.a, self.r)
    
    def __str__(self):
        return f'VMAX: {self.vmax}, ACCELERATION: {self.a}, RETARDATION: {self.r}'

data = FR.read_train_config()
stations = data['stops']
distance_deltas = C.calculate_distance_deltas(stations)
conf_vmax = data['max_speed']
conf_a = data['acceleration']
conf_r = data['retardation']
conf_start_time = data['start_time']
conf_day_type = data['day_type']

train = Train(conf_vmax, conf_a, conf_r)

table = Timetable(stations, distance_deltas, train, conf_start_time, conf_day_type)






# # Station class
# class Station:
#     def __init__(self, distance_deltas, index):
#         current_station_name = stations[index]['name']

#         if index == len(stations) - 1:
#             self.name = f'Slutstation: {current_station_name}'
#             self.distance_to_next = 0
#             return
        
#         current_distance_delta = distance_deltas[index]

#         if index == 0:
#             self.name = f'Startstation: {current_station_name}'
#             self.distance_to_next = current_distance_delta
#         else:
#             self.name = current_station_name
#             self.distance_to_next = current_distance_delta