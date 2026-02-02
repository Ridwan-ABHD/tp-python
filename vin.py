import requests
import random
from datetime import datetime

# --- MODULE 1 : STRUCTURE DES DONNÉES (Antoine L.) ---
class Vehicule:
    def __init__(self, d, anecdote="Véhicule décodé via l'API NHTSA."):
        # Stockage des infos techniques (Dictionnaires - Etape 2 & 4)
        self.marque = d.get("Make", "Inconnue")
        self.modele = d.get("Model", "Inconnu")
        self.annee = d.get("Model Year", "N/A")
        self.pays = d.get("Plant Country", "Inconnu")
        self.cylindree = d.get("Displacement (L)", "N/A")
        self.chevaux = d.get("Engine HP", "N/A")
        self.carburant = d.get("Fuel Type - Primary", "Inconnu")
        self.anecdote = anecdote # [NOUVEAU] Ajout d'une info culturelle

    def afficher_fiche(self):
        """Affiche une fiche technique élégante."""
        print(f"\n" + "═"*55)
        print(f" FICHE TECHNIQUE : {self.marque} {self.modele}")
        print(f" " + "─"*53)
        print(f" > Année      : {self.annee:<15} | Origine : {self.pays}")
        print(f" > Moteur     : {self.cylindree}L ({self.chevaux} HP) | Carburant : {self.carburant}")
        print(f" > Note       : {self.anecdote}")
        print("═"*55)

# MODULE 2 : COMMUNICATION API 
def recuperer_infos_api(vin):
    """Interroge l'API et gère les erreurs de format (Etape 5)."""
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Extraction des résultats vers un dictionnaire simple
        res = {item['Variable']: item['Value'] for item in data.get('Results', []) if item['Value']}
        
        # Vérification de la validité du VIN (Error Code 0 = OK)
        if res.get("Error Code") != "0":
            print(f"\n[!] ERREUR : {res.get('Error Text', 'VIN invalide')}")
            return None
        return res
    except Exception as e:
        print(f"\n[!] Erreur réseau : {e}")
        return None

# --- MODULE 3 : LOGIQUE DU GARAGE ET MUSÉE
garage_virtuel = []

# [PROPOSITION 2] : Base de données locale des Légendes
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

def menu():
    while True:
        print("\n" + "■"*35)
        print("   EXPERT VIN & MUSÉE AUTOMOBILE")
        print("■"*35)
        print("1. Décoder un VIN (Saisie manuelle)")
        print("2. Visiter le Musée (Légende Aléatoire)")
        print("3. Voir mon Garage (Historique)")
        print("4. Quitter")
        
        choix = input("\nVotre choix : ")

        if choix == "1":
            vin = input("Entrez le VIN (17 caractères) : ").upper().strip()
            if len(vin) != 17:
                print(f"ERREUR : Format incorrect ({len(vin)}/17 caractères).")
                continue
            
            infos = recuperer_infos_api(vin)
            if infos:
                v = Vehicule(infos)
                v.afficher_fiche()
                garage_virtuel.append(v)

        elif choix == "2":
            # [PROPOSITION 2] : On pioche dans le dictionnaire local sans risque de bug
            item = random.choice(musee_legendes)
            v_legende = Vehicule(item["data"], item["anecdote"])
            print("\n[INFO] : Vous avez découvert une légende du musée !")
            v_legende.afficher_fiche()
            garage_virtuel.append(v_legende)

        elif choix == "3":
            print("\n" + "─"*35)
            print(f" MON GARAGE ({len(garage_virtuel)} véhicules)")
            print("─"*35)
            if not garage_virtuel:
                print("Le garage est vide.") #
            else:
                for idx, v in enumerate(garage_virtuel, 1):
                    print(f"{idx}. {v.marque:<10} {v.modele:<12} ({v.annee})")

        elif choix == "4":
            print("Fermeture du programme. Bonne route !")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    menu()