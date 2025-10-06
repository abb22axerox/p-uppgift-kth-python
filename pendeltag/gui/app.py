import sys
import tkinter as tk
from tkinter import ttk, messagebox

sys.path.insert(0, '/Users/axelroxenborg/Documents/Programmering/p-uppgift-kth-python/pendeltag')

from utils import file_manager as FM
from utils import compute_save_timetable as CST

TRAIN_CONFIG_PATH = 'pendeltag/input/train_config.json'

class TimetableApp:
    def __init__(self, root, train_config):
        self.root = root
        self.train_config = train_config
        self.root.title(f"Tidtabell för linje: {train_config.get('line_name', '')}")
        self.root.geometry("1400x800")

        # Gör root-fönstret flexibelt
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Skapa flikar
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky='nsew')

        # === Flik: Tidtabell ===
        self.tab_tidtabell = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tidtabell, text='Tidtabell')

        # Grid-konfiguration för fliken: rad 0 = reload-knapp, rad 1 = tabell
        self.tab_tidtabell.grid_rowconfigure(0, weight=0)
        self.tab_tidtabell.grid_rowconfigure(1, weight=1)
        self.tab_tidtabell.grid_columnconfigure(0, weight=1)

        # Container för "Ladda om"-knappen
        self.reload_frame = tk.Frame(self.tab_tidtabell)
        self.reload_frame.grid(row=0, column=0, sticky='e', padx=10, pady=(10, 0))

        reload_button = tk.Button(self.reload_frame, text="Ladda om tidtabell", command=self._reload_timetable)
        reload_button.pack()

        # Frame för trädet (tabellen) - hålls separat så vi inte råkar radera reload-knappen
        self.tree_frame = tk.Frame(self.tab_tidtabell)
        self.tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # Ladda om i UI:et direkt
        self._reload_timetable()

        # === Flik: Inställningar ===
        self.tab_inställningar = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_inställningar, text='Inställningar')
        self._create_inställningar_tab(train_config)

    def _create_tidtabell_tab(self, timetable):
        """Skapar (eller återskapar) Treeview i self.tree_frame baserat på timetable.
        Denna funktion tar ansvar för att rensa tidigare innehåll i self.tree_frame.
        """

        # Rensa tidigare widgets i tree_frame
        for w in self.tree_frame.winfo_children():
            w.destroy()

        if not timetable:
            lbl = tk.Label(self.tree_frame, text="Ingen tidtabell hittades.")
            lbl.pack()
            return

        stations = list(timetable.keys())

        # Skapa Treeview
        self.tree = ttk.Treeview(self.tree_frame, columns=stations, show='headings')

        # Skapa kolumner
        for station in stations:
            self.tree.heading(station, text=station)
            self.tree.column(station, width=120, anchor='center')

        # Gör treeview stretch
        self.tree.pack(fill='both', expand=True)

        # Style
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        self.tree.tag_configure('evenrow', background='white')
        self.tree.tag_configure('oddrow', background='lightblue')

        # Fyll tabellen
        try:
            num_rows = max(len(times) for times in timetable.values())
        except ValueError:
            num_rows = 0

        for i in range(num_rows):
            row = []
            for station in stations:
                if i < len(timetable[station]):
                    t = timetable[station][i]
                    # Förvänta att t har "hour" och "minute"
                    row.append(f"{int(t['hour']):02d}:{int(t['minute']):02d}")
                else:
                    row.append('')
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=row, tags=(tag,))

    def _reload_timetable(self):
        try:
            computed_timetable = CST.compute_timetable(self.train_config)

        except Exception as e:
            messagebox.showerror("Fel vid inläsning", f"Kunde inte läsa tidtabell: {e}")
            return

        # Uppdatera tabellen i tree_frame (rensas i _create_tidtabell_tab)
        try:
            self._create_tidtabell_tab(computed_timetable)

        except Exception as e:
            messagebox.showerror("Fel vid uppdatering", f"Kunde inte uppdatera tabell: {e}")

    def _create_inställningar_tab(self, train_config):
        def create_labeled_entry(parent, label_text, default_value):
            label = tk.Label(parent, text=label_text)
            label.pack(pady=(10, 2))
            entry = tk.Entry(parent)
            entry.insert(0, str(default_value))
            entry.pack()
            return entry

        self.acc_entry = create_labeled_entry(self.tab_inställningar, "Acceleration (m/s²):", train_config.get("acceleration", 0.5))
        self.ret_entry = create_labeled_entry(self.tab_inställningar, "Retardation (m/s²):", train_config.get("retardation", 0.5))
        self.vmax_entry = create_labeled_entry(self.tab_inställningar, "Maxhastighet (m/s):", train_config.get("max_speed", 80))

        self.start_hour_entry = create_labeled_entry(self.tab_inställningar, "Starttid - timme (0–23):", train_config.get("start_time", {}).get("hour", 6))
        self.start_minute_entry = create_labeled_entry(self.tab_inställningar, "Starttid - minut (0–59):", train_config.get("start_time", {}).get("minute", 0))

        # Dagtyp dropdown
        day_label = tk.Label(self.tab_inställningar, text="Dagtyp:")
        day_label.pack(pady=(10, 2))
        self.day_var = tk.StringVar(value=train_config.get("day_type", "vardag"))
        self.day_dropdown = tk.OptionMenu(self.tab_inställningar, self.day_var, "vardag", "helg")
        self.day_dropdown.pack()

        self.wait_entry = create_labeled_entry(self.tab_inställningar, "Väntetid vid slutstation (min):", train_config.get("wait_time_end_station", 5))
        # Visa intervall i minuter i entryn
        self.interval_entry = create_labeled_entry(self.tab_inställningar, "Tågintervall (min):", train_config.get("train_interval", 3600) // 60)

        save_button = tk.Button(self.tab_inställningar, text="Spara inställningar", command=lambda: self.root.after(100, self._save_settings))
        save_button.pack(pady=15)

    def _save_settings(self):
        try:
            # Börja med en kopia av befintlig config
            new_config = self.train_config.copy()

            # Uppdatera de relevanta fälten
            new_config.update({
                "acceleration": float(self.acc_entry.get()),
                "retardation": float(self.ret_entry.get()),
                "max_speed": int(self.vmax_entry.get()),
                "start_time": {
                    "hour": int(self.start_hour_entry.get()),
                    "minute": int(self.start_minute_entry.get())
                },
                "day_type": self.day_var.get(),
                "wait_time_end_station": int(self.wait_entry.get()),
                "train_interval": int(self.interval_entry.get()) * 60
            })


            # Spara konfiguration till fil
            FM.save_settings(TRAIN_CONFIG_PATH, new_config)

            # Uppdatera interna konfigurationen
            self.train_config = new_config

            # Visa popup först
            messagebox.showinfo("Sparat", "Inställningarna har sparats.")

        except ValueError:
            messagebox.showerror("Fel", "Fel: Kontrollera att alla fält innehåller giltiga siffror.")
        except Exception as e:
            messagebox.showerror("Fel vid sparning", f"Kunde inte spara inställningar: {e}")


