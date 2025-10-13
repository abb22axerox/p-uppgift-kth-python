# Tidtabell-klass med huvudlogik

import sys
sys.path.insert(0, '/Users/axelroxenborg/Documents/Programmering/p-uppgift-kth-python/pendeltag')

from utils import calculator as C

SECONDS_PER_DAY = 24 * 60 * 60

class Timetable:
    def __init__(self, stations, train, day_type):
        self.stations = stations
        self.train = train
        self.day_type = day_type
        self.timetable = dict()

    def create_timetable(self, start_time, distance_deltas, wait_time, train_interval, vardag_train_amount):
        # Hjälpfunktoner för tidkonvertering
        def time_to_seconds(t):
            return int(t["hour"]) * 3600 + int(t["minute"]) * 60

        def seconds_to_time(sec):
            hour = (sec // 3600) % 24
            minute = (sec % 3600) // 60
            return {"hour": hour, "minute": minute}
        
        def format_times(times, start_time):
            start_seconds = int(start_time["hour"]) * 3600 + int(start_time["minute"]) * 60
            formatted_times = []

            for sec in times:
                total = start_seconds + sec
                hour = int((total // 3600) % 24)
                minute = int((total % 3600) // 60)
                formatted_times.append({"hour": hour, "minute": minute})

            return formatted_times

        timetable_dict = {}

        # Förbered tomma listor för varje station i tidtabellen
        for station in self.stations:
            timetable_dict[station["name"]] = []

        # Konvertera väntetid till sekunder
        wait_time = wait_time * 60

        # Initialisera starttid i sekunder
        absolute_start_sec = time_to_seconds(start_time)
        current_stations = self.stations.copy()
        current_distance_deltas = distance_deltas.copy()
        is_reversed = False
        running_helg = True

        # Helg-schema
        if self.day_type == 'helg':
            while running_helg:
                # Beräkna avgångstider för hela resan (som offsets i sekunder)
                journey_offsets = C.calculate_departure_for_stations(current_distance_deltas,
                                                                      self.train.vmax,
                                                                      self.train.a,
                                                                      self.train.r)
                
                # Räkna ut den absoluta tiden för sista avgången i den här resan
                last_departure = absolute_start_sec + journey_offsets[-1]

                # Formatera resa och lägg in avgångstider i tidtabellen
                journey_departure = format_times(journey_offsets, seconds_to_time(absolute_start_sec))
                
                # Lägg till avgångstider i tidtabellen om de är före midnatt
                if absolute_start_sec < SECONDS_PER_DAY:
                    for i, station in enumerate(current_stations):
                        timetable_dict[station["name"]].append({
                            "hour": journey_departure[i]["hour"],
                            "minute": journey_departure[i]["minute"],
                            "train_id": 1
                        })
                else:
                    # Om starttiden är efter midnatt, ta bort sista resan till ändstationen
                    if is_reversed:
                        for times in timetable_dict.values():
                            del times[-1]
                    running_helg = False
                    break
                
                # Uppdatera starttiden med resans varaktighet plus väntetid
                absolute_start_sec = last_departure + wait_time

                # Vänd normalt riktningen för nästa resa
                current_stations.reverse()
                current_distance_deltas.reverse()
                is_reversed = not is_reversed
        
        # Vardagsschema
        elif self.day_type == 'vardag':
            # Förbered listor för flera tåg
            absolute_start_secs = [time_to_seconds(start_time) + i * train_interval for i in range(vardag_train_amount)] # Starttider för varje tåg
            train_stations = [self.stations.copy() for _ in range(vardag_train_amount)] # Stationsordning för varje tåg
            train_distance_deltas = [distance_deltas.copy() for _ in range(vardag_train_amount)] # Distansdeltas för varje tåg
            train_is_reversed = [False] * vardag_train_amount # Riktning för varje tåg
            running_vardag = [True] * vardag_train_amount # Om tåget fortfarande kör

            while any(running_vardag):
                for idx in range(vardag_train_amount):
                    # Hoppa över tåg som inte längre kör
                    if not running_vardag[idx]:
                        continue

                    # Beräkna avgångstider för hela resan (som offsets i sekunder)
                    journey_offsets = C.calculate_departure_for_stations(
                        train_distance_deltas[idx],
                        self.train.vmax,
                        self.train.a,
                        self.train.r
                    )

                    # Räkna ut den absoluta tiden för sista avgången i den här resan
                    last_departure = absolute_start_secs[idx] + journey_offsets[-1]

                    # Formatera resa och lägg in avgångstider i tidtabellen
                    journey_departure = format_times(journey_offsets, seconds_to_time(absolute_start_secs[idx]))

                    # Lägg till avgångar i tidtabellen om starttid är före midnatt
                    if absolute_start_secs[idx] < SECONDS_PER_DAY:
                        for i, station in enumerate(train_stations[idx]):
                            timetable_dict[station["name"]].append({
                                "hour": journey_departure[i]["hour"],
                                "minute": journey_departure[i]["minute"],
                                "train_id": idx + 1
                            })
                    else:
                        # Om starttiden är efter midnatt, ta bort sista resan till ändstationen
                        if train_is_reversed[idx]:
                            for times in timetable_dict.values():
                                if times:
                                    del times[-1]
                        running_vardag[idx] = False
                        continue

                    # Uppdatera starttid med resans varaktighet + väntetid
                    absolute_start_secs[idx] = last_departure + wait_time

                    # Vänd tåget för nästa resa
                    train_stations[idx].reverse()
                    train_distance_deltas[idx].reverse()
                    train_is_reversed[idx] = not train_is_reversed[idx]

        # Spara den färdiga tidtabellen i objektet
        self.timetable = timetable_dict