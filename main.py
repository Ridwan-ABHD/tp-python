import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# On importe notre module "moteur"
from models import Vehicule, recuperer_infos_api, piocher_legende, calculer_statistiques


class VinApp:
    """Application principale de décodage VIN et Musée Automobile."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Expert VIN & Musée Automobile")
        self.root.geometry("800x700")
        
        # Thème clair : fond blanc/gris clair
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(True, True)
        
        # LISTE pour stocker l'historique des véhicules du garage
        self.garage_virtuel = []
        
        # Configuration du style
        self.configurer_style()
        
        # Création de l'interface
        self.creer_interface()
    
    def configurer_style(self):
        """Configure le style général de l'application (thème clair)."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Style des onglets
        self.style.configure("TNotebook", background="#f0f0f0")
        self.style.configure("TNotebook.Tab", 
                            font=("Arial", 10, "bold"),
                            padding=(15, 8))
        
        # Style des frames
        self.style.configure("TFrame", background="#f0f0f0")
    
    def creer_interface(self):
        """Crée tous les widgets de l'interface."""
        
        # --- EN-TÊTE ---
        header = tk.Frame(self.root, bg="#f0f0f0")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        titre = tk.Label(header, 
                        text="🚗 Expert VIN & Musée Automobile",
                        font=("Arial", 18, "bold"),
                        fg="#333333",
                        bg="#f0f0f0")
        titre.pack()
        
        sous_titre = tk.Label(header,
                             text="Décodez un VIN ou découvrez des véhicules légendaires",
                             font=("Arial", 10),
                             fg="#666666",
                             bg="#f0f0f0")
        sous_titre.pack(pady=(5, 0))
        
        # --- ONGLETS ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Onglet 1 : Décodeur VIN
        self.tab_decoder = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_decoder, text="🔍 Décodeur VIN")
        self.creer_onglet_decodeur()
        
        # Onglet 2 : Musée
        self.tab_musee = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_musee, text="🏛️ Musée")
        self.creer_onglet_musee()
        
        # Onglet 3 : Garage
        self.tab_garage = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_garage, text="🚘 Mon Garage")
        self.creer_onglet_garage()
        
        # --- PIED DE PAGE ---
        footer = tk.Frame(self.root, bg="#f0f0f0")
        footer.pack(fill="x", padx=20, pady=10)
        
        btn_quitter = tk.Button(footer,
                               text="Quitter",
                               font=("Arial", 10),
                               bg="#dc3545",  # Rouge
                               fg="white",
                               padx=20,
                               pady=5,
                               cursor="hand2",
                               command=self.root.quit)
        btn_quitter.pack(side="right")
    
    # ONGLET DÉCODEUR VIN
    
    
    def creer_onglet_decodeur(self):
        """Crée l'onglet pour décoder un VIN."""
        
        main_frame = tk.Frame(self.tab_decoder, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # --- Section saisie du VIN ---
        saisie_frame = tk.LabelFrame(main_frame, 
                                     text="Entrez votre numéro VIN",
                                     font=("Arial", 10, "bold"),
                                     bg="#f0f0f0",
                                     fg="#333333")
        saisie_frame.pack(fill="x", pady=(0, 15))
        
        inner_frame = tk.Frame(saisie_frame, bg="#f0f0f0")
        inner_frame.pack(padx=15, pady=15)
        
        # Label explicatif
        label_vin = tk.Label(inner_frame,
                            text="Numéro VIN (17 caractères) :",
                            font=("Arial", 10),
                            bg="#f0f0f0",
                            fg="#333333")
        label_vin.pack(anchor="w")
        
        # Champ de saisie
        self.vin_entry = tk.Entry(inner_frame,
                                 font=("Consolas", 14),
                                 width=25,
                                 bg="white",
                                 fg="#333333")
        self.vin_entry.pack(pady=(5, 5), ipady=5)
        
        # On lie la touche Entrée au décodage
        self.vin_entry.bind("<Return>", lambda e: self.decoder_vin())
        
        # Compteur de caractères
        self.compteur_label = tk.Label(inner_frame,
                                       text="0/17 caractères",
                                       font=("Arial", 9),
                                       bg="#f0f0f0",
                                       fg="#666666")
        self.compteur_label.pack(anchor="e")
        
        # On met à jour le compteur à chaque frappe
        self.vin_entry.bind("<KeyRelease>", self.maj_compteur)
        
        # Bouton Décoder (bleu)
        btn_decoder = tk.Button(inner_frame,
                               text="🔍 Décoder le VIN",
                               font=("Arial", 11, "bold"),
                               bg="#007bff",  # Bleu
                               fg="white",
                               padx=25,
                               pady=8,
                               cursor="hand2",
                               command=self.decoder_vin)
        btn_decoder.pack(pady=(10, 0))
        
        # --- Zone de résultat ---
        resultat_label = tk.Label(main_frame,
                                 text="📋 Fiche Technique",
                                 font=("Arial", 11, "bold"),
                                 bg="#f0f0f0",
                                 fg="#333333")
        resultat_label.pack(anchor="w", pady=(10, 5))
        
        # Zone de texte pour afficher les résultats
        self.resultat_text = scrolledtext.ScrolledText(main_frame,
                                                       font=("Consolas", 10),
                                                       bg="white",
                                                       fg="#333333",
                                                       height=12,
                                                       state="disabled")
        self.resultat_text.pack(fill="both", expand=True)
    
    def maj_compteur(self, event=None):
        """Met à jour le compteur de caractères du VIN."""
        nb_chars = len(self.vin_entry.get())
        
        # On change la couleur selon le nombre de caractères
        if nb_chars == 17:
            couleur = "#28a745"  # Vert = parfait
        elif nb_chars > 17:
            couleur = "#dc3545"  # Rouge = trop long
        else:
            couleur = "#666666"  # Gris = pas encore complet
        
        self.compteur_label.config(text=f"{nb_chars}/17 caractères", fg=couleur)
    
    def decoder_vin(self):
        """Décode le VIN saisi et affiche les résultats."""
        
        # On récupère le VIN en majuscules
        vin = self.vin_entry.get().upper().strip()
        
        # On vérifie si le VIN fait 17 caractères
        if len(vin) != 17:
            messagebox.showerror("Erreur", 
                f"Le VIN doit contenir 17 caractères.\nActuellement : {len(vin)} caractères")
            return
        
        # Message de chargement
        self.resultat_text.config(state="normal")
        self.resultat_text.delete(1.0, tk.END)
        self.resultat_text.insert(tk.END, "⏳ Recherche en cours...\n")
        self.resultat_text.config(state="disabled")
        self.root.update()
        
        # Appel à l'API (via notre module models.py)
        infos, erreur = recuperer_infos_api(vin)
        
        # Affichage des résultats
        self.resultat_text.config(state="normal")
        self.resultat_text.delete(1.0, tk.END)
        
        if infos:
            # On crée un objet Vehicule
            vehicule = Vehicule(infos)
            
            # On l'ajoute à notre LISTE garage
            self.garage_virtuel.append(vehicule)
            self.maj_affichage_garage()
            
            # On affiche la fiche
            self.resultat_text.insert(tk.END, "=" * 50 + "\n")
            self.resultat_text.insert(tk.END, f"  ✅ VÉHICULE TROUVÉ : {vehicule.marque} {vehicule.modele}\n")
            self.resultat_text.insert(tk.END, "=" * 50 + "\n\n")
            
            # On parcourt le dictionnaire pour afficher chaque info
            for cle, valeur in vehicule.to_dict().items():
                self.resultat_text.insert(tk.END, f"  ▸ {cle:<12} : {valeur}\n")
            
            self.resultat_text.insert(tk.END, "\n" + "-" * 50 + "\n")
            self.resultat_text.insert(tk.END, "  ✅ Véhicule ajouté à votre garage !\n")
        else:
            self.resultat_text.insert(tk.END, f"❌ Erreur : {erreur}\n")
        
        self.resultat_text.config(state="disabled")
    
    # ONGLET MUSÉE
    
    def creer_onglet_musee(self):
        """Crée l'onglet Musée des légendes."""
        
        main_frame = tk.Frame(self.tab_musee, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Description
        desc_label = tk.Label(main_frame,
                             text="🏆 Découvrez les véhicules légendaires de l'histoire automobile !",
                             font=("Arial", 11),
                             bg="#f0f0f0",
                             fg="#333333")
        desc_label.pack(pady=(0, 20))
        
        # Bouton découvrir (vert)
        btn_decouvrir = tk.Button(main_frame,
                                 text="✨ Découvrir une Légende",
                                 font=("Arial", 12, "bold"),
                                 bg="#28a745",  # Vert
                                 fg="white",
                                 padx=30,
                                 pady=12,
                                 cursor="hand2",
                                 command=self.visiter_musee)
        btn_decouvrir.pack(pady=10)
        
        # Zone d'affichage
        self.legende_text = scrolledtext.ScrolledText(main_frame,
                                                      font=("Consolas", 10),
                                                      bg="white",
                                                      fg="#333333",
                                                      height=15,
                                                      state="disabled")
        self.legende_text.pack(fill="both", expand=True, pady=(20, 0))
    
    def visiter_musee(self):
        """Pioche une voiture au hasard dans le musée (utilise RANDOM)."""
        
        # On utilise notre fonction du module models.py
        vehicule = piocher_legende()
        
        # On l'ajoute au garage
        self.garage_virtuel.append(vehicule)
        self.maj_affichage_garage()
        
        # On affiche la légende
        self.legende_text.config(state="normal")
        self.legende_text.delete(1.0, tk.END)
        
        self.legende_text.insert(tk.END, "✨" * 25 + "\n\n")
        self.legende_text.insert(tk.END, f"  🏆 LÉGENDE DÉCOUVERTE !\n\n")
        self.legende_text.insert(tk.END, f"  {vehicule.marque} {vehicule.modele} ({vehicule.annee})\n")
        self.legende_text.insert(tk.END, "-" * 50 + "\n\n")
        
        for cle, valeur in vehicule.to_dict().items():
            self.legende_text.insert(tk.END, f"  ▸ {cle:<12} : {valeur}\n")
        
        self.legende_text.insert(tk.END, "\n" + "✨" * 25 + "\n")
        self.legende_text.insert(tk.END, "\n  ✅ Véhicule ajouté à votre garage !\n")
        
        self.legende_text.config(state="disabled")
    
    # ONGLET GARAGE

    def creer_onglet_garage(self):
        """Crée l'onglet Mon Garage avec les statistiques."""
        
        main_frame = tk.Frame(self.tab_garage, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # --- En-tête du garage ---
        header = tk.Frame(main_frame, bg="#f0f0f0")
        header.pack(fill="x", pady=(0, 10))
        
        self.label_compteur_garage = tk.Label(header,
                                              text="🚘 Mon Garage (0 véhicules)",
                                              font=("Arial", 12, "bold"),
                                              bg="#f0f0f0",
                                              fg="#333333")
        self.label_compteur_garage.pack(side="left")
        
        btn_vider = tk.Button(header,
                             text="🗑️ Vider le garage",
                             font=("Arial", 9),
                             bg="#6c757d",  # Gris
                             fg="white",
                             padx=10,
                             pady=3,
                             cursor="hand2",
                             command=self.vider_garage)
        btn_vider.pack(side="right")
        
        # --- Liste des véhicules (Treeview) ---
        liste_frame = tk.Frame(main_frame, bg="white")
        liste_frame.pack(fill="both", expand=True)
        
        colonnes = ("Marque", "Modèle", "Année", "Pays", "Puissance")
        self.garage_tree = ttk.Treeview(liste_frame, 
                                        columns=colonnes, 
                                        show="headings",
                                        height=8)
        
        # Configuration des colonnes
        for col in colonnes:
            self.garage_tree.heading(col, text=col)
            self.garage_tree.column(col, width=100, anchor="center")
        
        # Barre de défilement
        scrollbar = ttk.Scrollbar(liste_frame, orient="vertical", command=self.garage_tree.yview)
        self.garage_tree.configure(yscrollcommand=scrollbar.set)
        
        self.garage_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        # Double-clic pour voir les détails
        self.garage_tree.bind("<Double-1>", self.voir_details)
        
        # --- CADRE STATISTIQUES ---
        stats_frame = tk.LabelFrame(main_frame,
                                    text="📊 Statistiques du Garage",
                                    font=("Arial", 10, "bold"),
                                    bg="#f0f0f0",
                                    fg="#333333")
        stats_frame.pack(fill="x", pady=(15, 0))
        
        inner_stats = tk.Frame(stats_frame, bg="#f0f0f0")
        inner_stats.pack(padx=15, pady=10)
        
        # Label pour le nombre de véhicules
        self.stat_nombre = tk.Label(inner_stats,
                                    text="📦 Véhicules scannés : 0",
                                    font=("Arial", 10),
                                    bg="#f0f0f0",
                                    fg="#333333")
        self.stat_nombre.pack(anchor="w", pady=2)
        
        # Label pour la puissance moyenne
        self.stat_puissance = tk.Label(inner_stats,
                                       text="⚡ Puissance moyenne : 0 HP",
                                       font=("Arial", 10),
                                       bg="#f0f0f0",
                                       fg="#333333")
        self.stat_puissance.pack(anchor="w", pady=2)
        
        # Label pour le pays le plus fréquent
        self.stat_pays = tk.Label(inner_stats,
                                  text="🌍 Pays le plus fréquent : Aucun",
                                  font=("Arial", 10),
                                  bg="#f0f0f0",
                                  fg="#333333")
        self.stat_pays.pack(anchor="w", pady=2)
    
    def maj_affichage_garage(self):
        """Met à jour l'affichage du garage et les statistiques."""
        
        # Mise à jour du compteur
        nb = len(self.garage_virtuel)
        self.label_compteur_garage.config(text=f"🚘 Mon Garage ({nb} véhicules)")
        
        # Mise à jour du Treeview
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
        
        # Mise à jour des statistiques
        stats = calculer_statistiques(self.garage_virtuel)
        
        self.stat_nombre.config(text=f"📦 Véhicules scannés : {stats['nombre']}")
        self.stat_puissance.config(text=f"⚡ Puissance moyenne : {stats['puissance_moyenne']} HP")
        self.stat_pays.config(text=f"🌍 Pays le plus fréquent : {stats['pays_frequent']}")
    
    def voir_details(self, event):
        """Affiche les détails d'un véhicule sélectionné."""
        
        selection = self.garage_tree.selection()
        if selection:
            # On récupère l'index du véhicule sélectionné
            idx = self.garage_tree.index(selection[0])
            vehicule = self.garage_virtuel[idx]
            
            # On construit le message
            details = f"""
{'='*45}
  {vehicule.marque} {vehicule.modele}
{'='*45}

  ▸ Année      : {vehicule.annee}
  ▸ Pays       : {vehicule.pays}
  ▸ Cylindrée  : {vehicule.cylindree}L
  ▸ Puissance  : {vehicule.chevaux} HP
  ▸ Carburant  : {vehicule.carburant}

   Note :
  {vehicule.anecdote}
{'='*45}
"""
            messagebox.showinfo(f"{vehicule.marque} {vehicule.modele}", details)
    
    def vider_garage(self):
        """Vide le garage après confirmation."""
        
        if len(self.garage_virtuel) > 0:
            reponse = messagebox.askyesno("Confirmation", 
                "Voulez-vous vraiment vider votre garage ?")
            if reponse:
                self.garage_virtuel.clear()  # On vide la LISTE
                self.maj_affichage_garage()
        else:
            messagebox.showinfo("Info", "Le garage est déjà vide !")



# LANCEMENT DE L'APPLICATION

if __name__ == "__main__":
    root = tk.Tk()
    app = VinApp(root)
    root.mainloop()
