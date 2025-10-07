## 📁 Projektstruktur

pendeltag/
│
├── 📁 gui/ # Gränssnitt för GUI (användargränssnitt)
│ └── app.py # Huvudfil för GUI-logik
│
├── 📁 classes/ # Datamodeller och klasser
│ ├── timetable.py # Klass för tidtabeller
│ └── train.py # Klass för tåg och dess logik
│
├── 📁 input/ # Inmatningsdata och konfiguration
│ └── train_config.json # JSON-konfigurationsfil för tåginformation
│
├── 📁 utils/ # Hjälpfunktioner och verktyg
│ ├── calculator.py # Allmänna beräkningsfunktioner
│ ├── compute_save_timetable.py # Beräkning och sparning av tidtabeller
│ ├── file_manager.py # Funktioner för filhantering
│ └── time_utils.py # Verktyg för tidsberäkningar
│
├── main.py # Applikationens startpunkt
└── README.md # Dokumentation för projektet