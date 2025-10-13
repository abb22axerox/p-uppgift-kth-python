
# Tidtabell för pendeltågslinje
<img width="1440" height="904" alt="Skärmavbild 2025-10-07 kl  19 49 34" src="https://github.com/user-attachments/assets/ea4d8d24-b630-4447-9507-90aa2c466339" />
<img width="223" height="586" alt="Skärmavbild 2025-10-07 kl  19 50 07" src="https://github.com/user-attachments/assets/11b7f4a3-3c6c-4caa-9d57-ab6eec72097e" />

---

Detta projekt är ett GUI-baserat Pythonprogram som genererar och visar tidtabeller för pendeltåg baserat på konfigurationsdata. Här är en specifikation av hur programmet fungerar och är uppbyggt.

---

## Programflöde

1. `main.py` körs som huvudprogram.
2. Konfigurationsfilen `train_config.json` läses in.
3. Ett tkinter-GUI (`TimetableApp`) startas.
4. Tidtabellen beräknas via `compute_save_timetable.py`:
   - `Train`-objektet skapas.
   - `Timetable`-objekt skapas och fylls med avgångstider.
5. Tidtabellen visas i en tabell i GUI:t.
6. Användaren kan uppdatera inställningar och spara dessa.
7. Tidtabellen uppdateras vid behov.

---

## Klasser & Metoder

### `Train` (i `classes/train.py`)
**Beskrivning:** Representerar ett tåg med dess fysikaliska egenskaper.

- **Instansvariabler:**
  - `vmax` – Maxhastighet i m/s
  - `a` – Acceleration i m/s²
  - `r` – Retardation i m/s²

- **Konstruktor:**
  ```python
  def __init__(self, vmax, a, r)
  ```

- **Metoder:**
  - `travel_time(s)` – Returnerar restid för en sträcka `s` i meter.

---

### `Timetable` (i `classes/timetable.py`)
**Beskrivning:** Ansvarar för att generera tidtabeller för given dagtyp, stationer och tåg.

- **Instansvariabler:**
  - `stations` – Lista av stationer (dict med namn och avstånd)
  - `train` – Ett `Train`-objekt
  - `day_type` – `"vardag"` eller `"helg"`
  - `timetable` – Dict som innehåller listor med tider per station

- **Konstruktor:**
  ```python
  def __init__(self, stations, train, day_type)
  ```

- **Metoder:**
  - `create_timetable(start_time, distance_deltas, wait_time, train_interval)`
    - Skapar tidtabellen beroende på dagtyp.
    - Hanterar både enkel och multipla tågscheman.

---

## Funktioner & Hjälpmoduler

### `calculator.py`
- `calculate_travel_time(s, vmax, a, r)` – Beräknar restid med acceleration och retardation.
- `calculate_distance_deltas(stations)` – Tar fram sträckor mellan stationer.
- `calculate_time_deltas(...)` – Returnerar restider mellan stopp.
- `calculate_departure_for_stations(...)` – Returnerar tider för varje station.

### `file_manager.py`
- `read_file(path)` – Läser JSON-fil.
- `save_settings(path, new_conf)` – Sparar konfigurationsfil med backup.

### `compute_save_timetable.py`
- `compute_timetable(data)` – Koordinerar hela beräkningen av tidtabellen.
  - Skapar `Train`
  - Skapar `Timetable`
  - Returnerar färdig tidtabell

---

## GUI – `TimetableApp` (i `gui/app.py`)

### Huvudkomponenter:
- Två flikar: **Tidtabell** & **Inställningar**
- TreeView-widget för att visa avgångar
- Knapp för att uppdatera tidtabellen
- Formulär för att ändra:
  - acceleration, retardation, maxhastighet
  - starttid, dagtyp, väntetid, tågintervall

### Viktiga metoder:
- `_reload_timetable()` – Laddar ny tidtabell från config
- `_create_tidtabell_tab(timetable)` – Renderar tabellen
- `_create_inställningar_tab()` – Skapar formuläret
- `_save_settings()` – Sparar nya värden till fil

---

## Projektstruktur

```
pendeltag/
│
├── gui/ # Gränssnitt för GUI (användargränssnitt)
│ └── app.py # Huvudfil för GUI-logik
│
├── classes/ # Datamodeller och klasser
│ ├── timetable.py # Klass för tidtabeller
│ └── train.py # Klass för tåg och dess logik
│
├── input/ # Inmatningsdata och konfiguration
│ └── train_config.json # JSON-konfigurationsfil för tåginformation
│
├── utils/ # Hjälpfunktioner och verktyg
│ ├── calculator.py # Allmänna beräkningsfunktioner
│ ├── compute_save_timetable.py # Beräkning och sparning av tidtabeller
│ └── file_manager.py # Funktioner för filhantering
│
├── main.py # Applikationens startpunkt
└── README.md # Dokumentation för projektet
```
