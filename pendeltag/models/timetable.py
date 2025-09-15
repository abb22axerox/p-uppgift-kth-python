# Timetable class (core logic)

class Timetable:
    def __init__(self, stations, train, start_time, day_type):
        self.stations = stations
        self.train = train
        self.start_time = start_time
        self.day_type = day_type
        self.timetable = dict()