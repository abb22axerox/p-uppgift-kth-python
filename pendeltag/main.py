# The main program entry point

from utils import file_reader as FR
from utils import calculator as C

# Timetable class (core logic)
class Timetable:
    def __init__(self, stations, train, start_time, day_type):
        self.stations = stations
        self.train = train
        self.start_time = start_time
        self.day_type = day_type
        self.timetable = dict()
    
    # def compute_part_times():
    #     C.calculate_travel_time()

# Station class
class Station:
    def __init__(self, distance_deltas, index):
        current_station_name = stations[index]['name']

        if index == len(stations) - 1:
            self.name = f'Slutstation: {current_station_name}'
            self.distance_to_next = 0
            return
        
        current_distance_delta = distance_deltas[index]

        if index == 0:
            self.name = f'Startstation: {current_station_name}'
            self.distance_to_next = current_distance_delta
        else:
            self.name = current_station_name
            self.distance_to_next = current_distance_delta

# Train class
class Train:
    def __init__(self, vmax, a, r):
        self.vmax = vmax
        self.a = a
        self.r = r

    def travel_time(self, s):
        return C.calculate_travel_time(s, self.vmax, self.a, self.r)

stations = FR.read_train_config()['stops']
distance_deltas = C.calculate_distance_deltas(stations)

s = Station(distance_deltas, 1)


print(f'Distansen från {s.name} till nästa station är {s.distance_to_next}km')