import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import random

# --- MODULE 1 : STRUCTURE DES DONNÉES ---
class Vehicule:
    def __init__(self, d, anecdote="Véhicule décodé via l'API NHTSA."):
        self.marque = d.get("Make", "Inconnue")
        self.modele = d.get("Model", "Inconnu")
        self.annee = d.get("Model Year", "N/A")
        self.pays = d.get("Plant Country", "Inconnu")
        self.cylindree = d.get("Displacement (L)", "N/A")
        self.chevaux = d.get("Engine HP", "N/A")
        self.carburant = d.get("Fuel Type - Primary", "Inconnu")
        self.anecdote = anecdote

    def to_dict(self):
        return {
            "Marque": self.marque,
            "Modèle": self.modele,
            "Année": self.annee,
            "Pays": self.pays,
            "Cylindrée": f"{self.cylindree}L",
            "Puissance": f"{self.chevaux} HP",
            "Carburant": self.carburant,
            "Note": self.anecdote
        }


def recuperer_infos_api(vin):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        res = {item['Variable']: item['Value'] for item in data.get('Results', []) if item['Value']}
        if res.get("Error Code") != "0":
            return None, res.get('Error Text', 'VIN invalide')
        return res, None
    except Exception as e:
        return None, f"Erreur réseau : {e}"


musee_legendes = [
    {
        "data": {"Make": "Ferrari", "Model": "F40", "Model Year": "1987", "Plant Country": "Italie", "Displacement (L)": "2.9", "Engine HP": "478", "Fuel Type - Primary": "Essence"},
        "anecdote": "La dernière voiture validée par Enzo Ferrari de son vivant."
    },
    {
        "data": {"Make": "DeLorean", "Model": "DMC-12", "Model Year": "1981", "Plant Country": "Irlande du Nord", "Displacement (L)": "2.8", "Engine HP": "130", "Fuel Type - Primary": "Essence"},
        "anecdote": "Célèbre pour son rôle de machine à voyager dans le temps au cinéma."
    },
    {
        "data": {"Make": "Shelby", "Model": "AC Cobra", "Model Year": "1965", "Plant Country": "UK/USA", "Displacement (L)": "7.0", "Engine HP": "425", "Fuel Type - Primary": "Essence"},
        "anecdote": "Un châssis anglais léger avec un énorme V8 américain."
    },
    {
        "data": {"Make": "Tesla", "Model": "Roadster", "Model Year": "2008", "Plant Country": "USA", "Displacement (L)": "0.0", "Engine HP": "248", "Fuel Type - Primary": "Électrique"},
        "anecdote": "Le premier modèle de Tesla, basé sur un châssis de Lotus Elise."
    }
]

# --- INTERFACE GRAPHIQUE ---
class VinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expert VIN & Musée Automobile")
        self.root.geometry("800x650")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(True, True)

        self.garage_virtuel = []

        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        self.create_widgets()

    def configure_styles(self):
        # Configuration des styles personnalisés
        self.style.configure("Title.TLabel", 
                           font=("Segoe UI", 20, "bold"), 
                           foreground="#e94560",
                           background="#1a1a2e")

        self.style.configure("Subtitle.TLabel", 
                           font=("Segoe UI", 11), 
                           foreground="#a0a0a0",
                           background="#1a1a2e")

        self.style.configure("Info.TLabel", 
                           font=("Segoe UI", 10), 
                           foreground="#ffffff",
                           background="#16213e")

        self.style.configure("Action.TButton",
                           font=("Segoe UI", 11, "bold"),
                           padding=(20, 10))

        self.style.configure("TNotebook", background="#1a1a2e")
        self.style.configure("TNotebook.Tab", 
                           font=("Segoe UI", 10, "bold"),
                           padding=(15, 8))

        self.style.configure("TFrame", background="#1a1a2e")
        self.style.configure("Card.TFrame", background="#16213e")

    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self.root, style="TFrame")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        title = ttk.Label(header_frame, text="Expert VIN & Musée Automobile", style="Title.TLabel")
        title.pack()

        subtitle = ttk.Label(header_frame, text="Décodez un VIN ou découvrez des véhicules légendaires", style="Subtitle.TLabel")
        subtitle.pack(pady=(5, 0))

        # Notebook (onglets)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # Onglet 1 : Décodeur VIN
        self.tab_decoder = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.tab_decoder, text="Décodeur VIN")
        self.create_decoder_tab()

        # Onglet 2 : Musée
        self.tab_musee = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.tab_musee, text="Musée")
        self.create_musee_tab()

        # Onglet 3 : Garage
        self.tab_garage = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.tab_garage, text="Mon Garage")
        self.create_garage_tab()

    def create_decoder_tab(self):
        # Frame principal
        main_frame = ttk.Frame(self.tab_decoder, style="TFrame")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Section saisie VIN
        input_frame = ttk.Frame(main_frame, style="Card.TFrame")
        input_frame.pack(fill="x", pady=(0, 20))

        inner_input = tk.Frame(input_frame, bg="#16213e")
        inner_input.pack(padx=20, pady=20)

        vin_label = tk.Label(inner_input, text="Numéro VIN (17 caractères) :", 
                            font=("Segoe UI", 11), fg="#ffffff", bg="#16213e")
        vin_label.pack(anchor="w")

        self.vin_entry = tk.Entry(inner_input, font=("Consolas", 14), width=30,
                                 bg="#0f3460", fg="#ffffff", insertbackground="#e94560",
                                 relief="flat", bd=5)
        self.vin_entry.pack(pady=(5, 10), ipady=8)
        self.vin_entry.bind("<Return>", lambda e: self.decoder_vin())

        # Compteur de caractères
        self.char_count = tk.Label(inner_input, text="0/17 caractères", 
                                  font=("Segoe UI", 9), fg="#a0a0a0", bg="#16213e")
        self.char_count.pack(anchor="e")
        self.vin_entry.bind("<KeyRelease>", self.update_char_count)

        decode_btn = tk.Button(inner_input, text="🔍 Décoder le VIN", 
                              font=("Segoe UI", 11, "bold"),
                              bg="#e94560", fg="white", relief="flat",
                              cursor="hand2", padx=30, pady=10,
                              command=self.decoder_vin)
        decode_btn.pack(pady=(10, 0))

        # Zone de résultat
        result_label = tk.Label(main_frame, text="Fiche Technique", 
                               font=("Segoe UI", 12, "bold"), fg="#e94560", bg="#1a1a2e")
        result_label.pack(anchor="w", pady=(10, 5))

        self.result_frame = tk.Frame(main_frame, bg="#16213e", relief="flat")
        self.result_frame.pack(fill="both", expand=True)

        self.result_text = scrolledtext.ScrolledText(self.result_frame, 
                                                     font=("Consolas", 11),
                                                     bg="#16213e", fg="#ffffff",
                                                     relief="flat", wrap="word",
                                                     state="disabled")
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)

    def create_musee_tab(self):
        main_frame = ttk.Frame(self.tab_musee, style="TFrame")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Description
        desc_label = tk.Label(main_frame, 
                             text="Découvrez les véhicules légendaires de l'histoire automobile !",
                             font=("Segoe UI", 12), fg="#a0a0a0", bg="#1a1a2e")
        desc_label.pack(pady=(0, 20))

        # Bouton découvrir
        discover_btn = tk.Button(main_frame, text="✨ Découvrir une Légende", 
                                font=("Segoe UI", 14, "bold"),
                                bg="#e94560", fg="white", relief="flat",
                                cursor="hand2", padx=40, pady=15,
                                command=self.visiter_musee)
        discover_btn.pack(pady=10)

        # Zone d'affichage légende
        self.legend_frame = tk.Frame(main_frame, bg="#16213e", relief="flat")
        self.legend_frame.pack(fill="both", expand=True, pady=(20, 0))

        self.legend_display = scrolledtext.ScrolledText(self.legend_frame,
                                                        font=("Consolas", 11),
                                                        bg="#16213e", fg="#ffffff",
                                                        relief="flat", wrap="word",
                                                        state="disabled")
        self.legend_display.pack(fill="both", expand=True, padx=10, pady=10)

    def create_garage_tab(self):
        main_frame = ttk.Frame(self.tab_garage, style="TFrame")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header garage
        header = tk.Frame(main_frame, bg="#1a1a2e")
        header.pack(fill="x", pady=(0, 10))

        self.garage_count = tk.Label(header, text="🚘 Mon Garage (0 véhicules)",
                                    font=("Segoe UI", 14, "bold"), fg="#e94560", bg="#1a1a2e")
        self.garage_count.pack(side="left")

        clear_btn = tk.Button(header, text="🗑️ Vider", 
                             font=("Segoe UI", 9),
                             bg="#0f3460", fg="white", relief="flat",
                             cursor="hand2", padx=15, pady=5,
                             command=self.vider_garage)
        clear_btn.pack(side="right")

        # Liste des véhicules
        list_frame = tk.Frame(main_frame, bg="#16213e")
        list_frame.pack(fill="both", expand=True)

        # Treeview pour afficher les véhicules
        columns = ("Marque", "Modèle", "Année", "Pays", "Puissance")
        self.garage_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.garage_tree.heading(col, text=col)
            self.garage_tree.column(col, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.garage_tree.yview)
        self.garage_tree.configure(yscrollcommand=scrollbar.set)

        self.garage_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))

        # Bind double-clic pour voir les détails
        self.garage_tree.bind("<Double-1>", self.voir_details_vehicule)

    def update_char_count(self, event=None):
        count = len(self.vin_entry.get())
        color = "#4ecca3" if count == 17 else "#e94560" if count > 17 else "#a0a0a0"
        self.char_count.config(text=f"{count}/17 caractères", fg=color)

    def decoder_vin(self):
        vin = self.vin_entry.get().upper().strip()

        if len(vin) != 17:
            messagebox.showerror("Erreur", f"Le VIN doit contenir 17 caractères.\nActuellement : {len(vin)} caractères")
            return

        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Recherche en cours...\n")
        self.result_text.config(state="disabled")
        self.root.update()

        infos, error = recuperer_infos_api(vin)

        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)

        if infos:
            vehicule = Vehicule(infos)
            self.garage_virtuel.append(vehicule)
            self.update_garage_display()

            self.result_text.insert(tk.END, "═" * 50 + "\n")
            self.result_text.insert(tk.END, f"  VÉHICULE TROUVÉ : {vehicule.marque} {vehicule.modele}\n")
            self.result_text.insert(tk.END, "═" * 50 + "\n\n")

            for key, value in vehicule.to_dict().items():
                self.result_text.insert(tk.END, f"  ▸ {key:<12} : {value}\n")

            self.result_text.insert(tk.END, "\n" + "─" * 50 + "\n")
            self.result_text.insert(tk.END, "  Véhicule ajouté à votre garage !\n")
        else:
            self.result_text.insert(tk.END, f"Erreur : {error}\n")

        self.result_text.config(state="disabled")

    def visiter_musee(self):
        item = random.choice(musee_legendes)
        vehicule = Vehicule(item["data"], item["anecdote"])
        self.garage_virtuel.append(vehicule)
        self.update_garage_display()

        self.legend_display.config(state="normal")
        self.legend_display.delete(1.0, tk.END)

        self.legend_display.insert(tk.END, "✨" * 25 + "\n")
        self.legend_display.insert(tk.END, f"\n  LÉGENDE DÉCOUVERTE !\n\n")
        self.legend_display.insert(tk.END, f"  {vehicule.marque} {vehicule.modele} ({vehicule.annee})\n")
        self.legend_display.insert(tk.END, "─" * 50 + "\n\n")

        for key, value in vehicule.to_dict().items():
            self.legend_display.insert(tk.END, f"  ▸ {key:<12} : {value}\n")

        self.legend_display.insert(tk.END, "\n" + "✨" * 25 + "\n")
        self.legend_display.insert(tk.END, "\n  Véhicule ajouté à votre garage !\n")

        self.legend_display.config(state="disabled")

    def update_garage_display(self):
        # Mise à jour du compteur
        self.garage_count.config(text=f"Mon Garage ({len(self.garage_virtuel)} véhicules)")

        # Mise à jour du treeview
        for item in self.garage_tree.get_children():
            self.garage_tree.delete(item)

        for vehicule in self.garage_virtuel:
            self.garage_tree.insert("", "end", values=(
                vehicule.marque,
                vehicule.modele,
                vehicule.annee,
                vehicule.pays,
                f"{vehicule.chevaux} HP"
            ))

    def voir_details_vehicule(self, event):
        selection = self.garage_tree.selection()
        if selection:
            idx = self.garage_tree.index(selection[0])
            vehicule = self.garage_virtuel[idx]

            details = f"""
═══════════════════════════════════════════
  {vehicule.marque} {vehicule.modele}
═══════════════════════════════════════════

  ▸ Année      : {vehicule.annee}
  ▸ Pays       : {vehicule.pays}
  ▸ Cylindrée  : {vehicule.cylindree}L
  ▸ Puissance  : {vehicule.chevaux} HP
  ▸ Carburant  : {vehicule.carburant}

  Note :
  {vehicule.anecdote}
═══════════════════════════════════════════
"""
            messagebox.showinfo(f"{vehicule.marque} {vehicule.modele}", details)

    def vider_garage(self):
        if self.garage_virtuel:
            if messagebox.askyesno("Confirmation", "Voulez-vous vraiment vider votre garage ?"):
                self.garage_virtuel.clear()
                self.update_garage_display()
        else:
            messagebox.showinfo("Info", "Le garage est déjà vide !")

# --- LANCEMENT DE L'APPLICATION ---
if __name__ == "__main__":
    root = tk.Tk()
    app = VinApp(root)
    root.mainloop()
 