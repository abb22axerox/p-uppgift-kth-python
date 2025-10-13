# Funktion för att använda tidtabell-klassen och skapa tidtabell

from utils import calculator as C

from classes import timetable as TT
from classes import train as TR

def compute_timetable(data):
    # Extrahera konfigurationsdata
    conf_a = data['acceleration']
    conf_r = data['retardation']
    conf_vmax = data['max_speed']
    conf_start_time = data['start_time']
    conf_day_type = data['day_type']
    stations = data['stops']
    distance_deltas = C.calculate_distance_deltas(stations)
    conf_wait_time = data['wait_time_end_station']
    conf_train_interval = data['train_interval']
    conf_vardag_train_amount = data['vardag_train_amount']

    # Skapa tåg- och tidtabellsobjekt
    train = TR.Train(conf_vmax, conf_a, conf_r)
    table = TT.Timetable(stations, train, conf_day_type)
    
    # Generera tidtabell
    table.create_timetable(conf_start_time, distance_deltas, conf_wait_time, conf_train_interval, conf_vardag_train_amount)
    exported_time_table = table.timetable

    return exported_time_table