import requests
import random


# --- CLASSE VEHICULE 
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


# --- FONCTION API (utilise la librairie REQUESTS) ---
def recuperer_infos_api(vin):
    """
    Appelle l'API NHTSA pour décoder un numéro VIN.
    Retourne un tuple : (dictionnaire_infos, message_erreur)
    """
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    
    try:
        # On fait la requête HTTP avec un timeout de 10 secondes
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # On transforme la réponse en dictionnaire simple
        resultats = {}
        for item in data.get('Results', []):
            if item['Value']:  # On garde seulement les valeurs non vides
                resultats[item['Variable']] = item['Value']
        
        # On vérifie si le VIN est valide
        if resultats.get("Error Code") != "0":
            return None, resultats.get('Error Text', 'VIN invalide')
        
        return resultats, None
        
    except Exception as e:
        return None, f"Erreur réseau : {e}"


# --- MUSÉE DES LÉGENDES (utilise une LISTE de DICTIONNAIRES) ---
musee_legendes = [
    {
        "data": {
            "Make": "Ferrari",
            "Model": "F40",
            "Model Year": "1987",
            "Plant Country": "Italie",
            "Displacement (L)": "2.9",
            "Engine HP": "478",
            "Fuel Type - Primary": "Essence"
        },
        "anecdote": "La dernière voiture validée par Enzo Ferrari de son vivant."
    },
    {
        "data": {
            "Make": "DeLorean",
            "Model": "DMC-12",
            "Model Year": "1981",
            "Plant Country": "Irlande du Nord",
            "Displacement (L)": "2.8",
            "Engine HP": "130",
            "Fuel Type - Primary": "Essence"
        },
        "anecdote": "Célèbre pour son rôle de machine à voyager dans le temps au cinéma."
    },
    {
        "data": {
            "Make": "Shelby",
            "Model": "AC Cobra",
            "Model Year": "1965",
            "Plant Country": "UK/USA",
            "Displacement (L)": "7.0",
            "Engine HP": "425",
            "Fuel Type - Primary": "Essence"
        },
        "anecdote": "Un châssis anglais léger avec un énorme V8 américain."
    },
    {
        "data": {
            "Make": "Tesla",
            "Model": "Roadster",
            "Model Year": "2008",
            "Plant Country": "USA",
            "Displacement (L)": "0.0",
            "Engine HP": "248",
            "Fuel Type - Primary": "Électrique"
        },
        "anecdote": "Le premier modèle de Tesla, basé sur un châssis de Lotus Elise."
    },
    {
        "data": {
            "Make": "Porsche",
            "Model": "911 Carrera",
            "Model Year": "1973",
            "Plant Country": "Allemagne",
            "Displacement (L)": "2.7",
            "Engine HP": "210",
            "Fuel Type - Primary": "Essence"
        },
        "anecdote": "La 911 RS 2.7 est considérée comme l'une des meilleures Porsche jamais produites."
    }
]


# --- FONCTION RANDOM
def piocher_legende():
    """
    Pioche un véhicule au hasard dans le musée.
    Utilise random.choice() pour la sélection aléatoire.
    """
    legende = random.choice(musee_legendes)
    vehicule = Vehicule(legende["data"], legende["anecdote"])
    return vehicule


# --- FONCTIONS STATISTIQUES ---
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
            # On essaie de convertir les chevaux en nombre
            chevaux = float(vehicule.chevaux)
            total_chevaux = total_chevaux + chevaux
            compteur_valide = compteur_valide + 1
        except:
            # Si la conversion échoue, on ignore ce véhicule
            pass
    
    if compteur_valide > 0:
        puissance_moyenne = total_chevaux / compteur_valide
    else:
        puissance_moyenne = 0
    
    # Trouver le pays le plus fréquent
    compteur_pays = {}  # Dictionnaire pour compter les pays
    
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
