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

# Station class
class Station:
    def __init__(self, name, distance):
      self.name = name
      self.distance = distance
   
    def distance_from_start(self):
        data = FR.read_train_config()
        stops = list()
        for stop in data['stops']:
            stops.append(stop['distance'])
        return stops

# Train class
class Train:
    def __init__(self, vmax, a, r):
        self.vmax = vmax
        self.a = a
        self.r = r

    def travel_time(self, s):
        return C.calculate_travel_time(s, self.vmax, self.a, self.r)



s = Station("Example", 0)
distances = s.distance_from_start()
print(distances)