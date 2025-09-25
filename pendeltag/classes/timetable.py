import sys
sys.path.insert(0, '/Users/axelroxenborg/Documents/Programmering/p-uppgift-kth-python/pendeltag')

from utils import calculator as C
from utils import time_utils as TU

# Timetable class (core logic)
class Timetable:
    def __init__(self, stations, train, day_type):
        self.stations = stations
        self.train = train
        self.day_type = day_type
        self.timetable = dict()

    def create_timetable(self, start_time, distance_deltas, wait_time):
        # Helper functions to convert between time dict and seconds (24-hour format)
        def time_to_seconds(t):
            return int(t["hour"]) * 3600 + int(t["minute"]) * 60

        def seconds_to_time(sec):
            hour = (sec // 3600) % 24
            minute = (sec % 3600) // 60
            return {"hour": hour, "minute": minute}
        timetable_dict = {}

        # Prepare timetable_dict so each station name holds a list of departure times
        for station in self.stations:
            timetable_dict[station["name"]] = []

        wait_time = wait_time * 60

        # Initialize absolute_start_sec from the config start_time
        absolute_start_sec = time_to_seconds(start_time)
        current_stations = self.stations.copy()
        current_distance_deltas = distance_deltas.copy()
        last_departure_abs = 0

        if self.day_type == 'helg':
            while last_departure_abs < 60 * 60 * 24:
                journey_offsets = C.calculate_departure_for_stations(current_distance_deltas, self.train.vmax, self.train.a, self.train.r)
                journey_departure = TU.format_times(journey_offsets, seconds_to_time(absolute_start_sec))

                for i, station in enumerate(current_stations):
                    timetable_dict[station["name"]].append(journey_departure[i])

                last_departure_abs = absolute_start_sec + journey_offsets[-1]

                if last_departure_abs >= 60 * 60 * 24:
                    break

                absolute_start_sec = last_departure_abs + wait_time

                current_stations.reverse()
                current_distance_deltas.reverse()
        
        elif self.day_type == 'vardag':
            train_amount = 3
            base_interval = 5 * 60  # 5 minutes (in seconds)

            # Create independent starting times for each train.
            train_start_secs = [time_to_seconds(start_time) + i * base_interval for i in range(train_amount)]
            
            # Each train keeps its own station order and distance deltas. (list of lists)
            train_stations = [self.stations.copy() for _ in range(train_amount)]
            train_distance_deltas = [distance_deltas.copy() for _ in range(train_amount)]
            
            # Running flag for each train (continue simulating until its outbound is after midnight)
            running = [True] * train_amount

            print('vardag simulation for 3 trains')
            
            # Run the simulation until all trains have finished their schedules.
            while any(running):
                for idx in range(train_amount):
                    if not running[idx]:
                        continue

                    # Calculate journey offsets for the current state of train idx.
                    journey_offsets = C.calculate_departure_for_stations(train_distance_deltas[idx], self.train.vmax, self.train.a, self.train.r)
                    # Format the journey departure times using that train's absolute start time.
                    journey_departure = TU.format_times(journey_offsets, seconds_to_time(train_start_secs[idx]))
                    
                    # Append each departure time to the timetable dictionary.
                    for j, station in enumerate(train_stations[idx]):
                        timetable_dict[station["name"]].append(journey_departure[j])
                    
                    # Calculate the absolute time of the final departure of this journey.
                    last_dep = train_start_secs[idx] + journey_offsets[-1]
                    
                    # If the current journey is outbound (assume Kåvik is the last station)...
                    if train_stations[idx][-1]["name"] == "Kåvik":
                        # If the last departure is after midnight, stop scheduling for this train.
                        if last_dep >= 60 * 60 * 24:
                            running[idx] = False
                            continue
                        else:
                            # Outbound journey: add wait time before next journey.
                            train_start_secs[idx] = last_dep + wait_time
                    else:
                        # Inbound journey: Do not add extra wait time on turnaround.
                        train_start_secs[idx] = last_dep
                    
                    # Reverse the order to simulate turnaround.
                    train_stations[idx].reverse()
                    train_distance_deltas[idx].reverse()
        
        # Save to self
        self.timetable = timetable_dict