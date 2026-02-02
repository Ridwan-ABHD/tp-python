import requests
import random
import json

class Vehicule:
    """
    Représente un véhicule avec ses caractéristiques.
    Utilise un dictionnaire pour structurer les données.
    """
    
    def __init__(self, donnees, anecdote="Véhicule décodé via l'API NHTSA."):
        # On extrait les infos du dictionnaire reçu
        self.marque = donnees.get("Make", "Inconnue")
        self.modele = donnees.get("Model", "Inconnu")
        self.annee = donnees.get("Model Year", "N/A")
        self.pays = donnees.get("Plant Country", "Inconnu")
        self.cylindree = donnees.get("Displacement (L)", "N/A")
        self.chevaux = donnees.get("Engine HP", "N/A")
        self.carburant = donnees.get("Fuel Type - Primary", "Inconnu")
        self.anecdote = anecdote

    def to_dict(self):
        """Retourne les infos du véhicule sous forme de dictionnaire."""
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


# FONCTION API  
def recuperer_infos_api(vin):
    """
    Appelle l'API NHTSA pour décoder un numéro VIN.
    Retourne un tuple : (dictionnaire_infos, message_erreur)
    """
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    
    try:
        # timeout 
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # reponse en dictionnaire
        resultats = {}
        for item in data.get('Results', []):
            if item['Value']:  # seulement valeur non vides
                resultats[item['Variable']] = item['Value']
        
        # verif vin
        if resultats.get("Error Code") != "0":
            return None, resultats.get('Error Text', 'VIN invalide')
        
        return resultats, None
        
    except Exception as e:
        return None, f"Erreur réseau : {e}"


# CHARGEMENT FICHIER JSON
def charger_musee():
    """
    Charge la liste des véhicules légendaires depuis le fichier legendes.json.

    """
    try:
        # Ouverture du fichier JSON
        with open("legendes.json", "r", encoding="utf-8") as fichier:
            musee = json.load(fichier)
        return musee
    except FileNotFoundError:
        # Si le fichier n'existe pas
        print("Attention : fichier legendes.json introuvable.")
        return []
    except Exception as e:
        # En cas d'autre erreur
        print(f"Erreur lors du chargement du musée : {e}")
        return []


# MUSÉE DES LÉGENDES (chargé depuis le fichier JSON) 
musee_legendes = charger_musee()


# FONCTION RANDOM
def piocher_legende():
    """
    Pioche un véhicule au hasard dans le musée.
    """
    legende = random.choice(musee_legendes)
    vehicule = Vehicule(legende["data"], legende["anecdote"])
    return vehicule


# FONCTIONS STATISTIQUES
def calculer_statistiques(liste_vehicules):
    """
    Calcule les statistiques du garage.
    Retourne un dictionnaire avec les stats.
    """
    # Si le garage est vide, on retourne des valeurs par défaut
    if len(liste_vehicules) == 0:
        return {
            "nombre": 0,
            "puissance_moyenne": 0,
            "pays_frequent": "Aucun"
        }
    
    # Nombre de véhicules
    nombre = len(liste_vehicules)
    
    # Calcul de la puissance moyenne
    total_chevaux = 0
    compteur_valide = 0
    
    for vehicule in liste_vehicules:
        try:
            # Cheuvaux en nombre
            chevaux = float(vehicule.chevaux)
            total_chevaux = total_chevaux + chevaux
            compteur_valide = compteur_valide + 1
        except:
            # ignore si non convertible
            pass
    
    if compteur_valide > 0:
        puissance_moyenne = total_chevaux / compteur_valide
    else:
        puissance_moyenne = 0
    
    # Trouver le pays le plus fréquent
    compteur_pays = {}  
    
    for vehicule in liste_vehicules:
        pays = vehicule.pays
        if pays in compteur_pays:
            compteur_pays[pays] = compteur_pays[pays] + 1
        else:
            compteur_pays[pays] = 1
    
    # On cherche le pays avec le plus grand compteur
    pays_frequent = "Inconnu"
    max_count = 0
    
    for pays, count in compteur_pays.items():
        if count > max_count:
            max_count = count
            pays_frequent = pays
    
    return {
        "nombre": nombre,
        "puissance_moyenne": round(puissance_moyenne, 1),
        "pays_frequent": pays_frequent
    }
