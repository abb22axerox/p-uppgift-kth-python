# Functions to read and parse input files

import json
import shutil

def read_file(path):
    with open(path, 'r', encoding='utf-8') as data:
        return json.load(data)
    
def save_settings(path, new_conf):
    # Läs in befintlig config
    with open(path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Skriv över enbart de inställningar som användaren får ändra
    config["acceleration"] = new_conf["acceleration"]
    config["retardation"] = new_conf["retardation"]
    config["max_speed"] = new_conf["max_speed"]
    config["start_time"] = new_conf["start_time"]
    config["day_type"] = new_conf["day_type"]
    config["wait_time_end_station"] = new_conf["wait_time_end_station"]
    config["train_interval"] = new_conf["train_interval"]

    # Skapa säkerhetskopia innan vi skriver
    shutil.copy(path, path + ".bak")

    # Spara uppdaterad config
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)