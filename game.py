# Importation des bibliothèques nécessaires
import requests  # Pour faire des requêtes HTTP vers l'API Pokémon
import random    # Pour générer des nombres aléatoires

# Cache pour éviter de re-télécharger les mêmes infos de type
# Dictionnaire qui stocke les relations de types déjà récupérées
CACHE_TYPES = {}

def obtenir_faiblesses_type(type_name):
    """Récupère les faiblesses et forces d'un type depuis l'API.
    
    Args:
        type_name (str): Le nom du type Pokémon (ex: 'fire', 'water', etc.)
    
    Returns:
        dict: Dictionnaire avec les clés 'fort' et 'faible' contenant les listes de types
    """
    # Vérifier si le type est déjà dans le cache pour éviter une requête API
    if type_name in CACHE_TYPES:
        return CACHE_TYPES[type_name]

    # Construction de l'URL pour récupérer les infos de type
    url = f"https://pokeapi.co/api/v2/type/{type_name}"
    # Envoi de la requête GET à l'API
    response = requests.get(url)
    # Conversion de la réponse JSON en dictionnaire Python
    data = response.json()

    # Types contre lesquels ce type est fort (double damage to)
    # Liste des types qui subissent 2x de dégâts de ce type
    fort_contre = [t['name'] for t in data['damage_relations']['double_damage_to']]
    # Types contre lesquels ce type est faible (double damage from)
    # Liste des types qui infligent 2x de dégâts à ce type
    faible_contre = [t['name'] for t in data['damage_relations']['double_damage_from']]

    # Stockage dans le cache pour éviter de refaire la requête
    CACHE_TYPES[type_name] = {'fort': fort_contre, 'faible': faible_contre}
    return CACHE_TYPES[type_name]

def obtenir_pokemon(numero):
    """Récupère les informations d'un Pokémon depuis l'API PokeAPI.
    
    Args:
        numero (int): Le numéro du Pokémon dans le Pokédex
    
    Returns:
        dict: Dictionnaire contenant le nom et le type du Pokémon
    """
    # Construction de l'URL de l'API avec le numéro du Pokémon
    url = f"https://pokeapi.co/api/v2/pokemon/{numero}"
    # Envoi de la requête GET à l'API
    response = requests.get(url)
    # Conversion de la réponse JSON en dictionnaire Python
    data = response.json()
    # Extraction du nom et mise en majuscule de la première lettre
    nom = data['name'].capitalize()
    # Récupération du type principal (premier type dans la liste)
    type_principal = data['types'][0]['type']['name']
    # Retour des informations sous forme de dictionnaire
    return {'nom': nom, 'type': type_principal}

def combat(p1, p2):
    """Simule un combat entre deux Pokémon basé sur les avantages de types.
    
    Args:
        p1 (dict): Premier Pokémon avec 'nom' et 'type'
        p2 (dict): Deuxième Pokémon avec 'nom' et 'type'
    
    Returns:
        int: 1 si p1 gagne, 2 si p2 gagne
    """
    # Extraction des types des deux Pokémon
    type1, type2 = p1['type'], p2['type']

    # Récupérer les relations de types depuis l'API (forces et faiblesses)
    relations1 = obtenir_faiblesses_type(type1)
    relations2 = obtenir_faiblesses_type(type2)

    # Vérifier si p1 a un avantage de type sur p2
    # (le type de p2 est dans la liste des types contre lesquels p1 est fort)
    if type2 in relations1['fort']:
        return 1  # Pokémon 1 gagne
    # Vérifier si p2 a un avantage de type sur p1
    # (le type de p1 est dans la liste des types contre lesquels p2 est fort)
    elif type1 in relations2['fort']:
        return 2  # Pokémon 2 gagne
    # Aucun avantage de type : choix aléatoire du gagnant
    else:
        return random.choice([1, 2])

def creer_equipe(taille=5):
    """Crée une équipe de Pokémon aléatoires.
    
    Args:
        taille (int): Nombre de Pokémon dans l'équipe (par défaut 5)
    
    Returns:
        list: Liste de dictionnaires représentant les Pokémon de l'équipe
    """
    equipe = []  # Initialisation de la liste vide pour l'équipe
    # Boucle pour créer chaque Pokémon de l'équipe
    for _ in range(taille):
        # Génération d'un numéro aléatoire entre 1 et 150 (première génération)
        numero = random.randint(1, 150)
        # Récupération des données du Pokémon depuis l'API
        pokemon = obtenir_pokemon(numero)
        # Ajout du Pokémon à l'équipe
        equipe.append(pokemon)
    return equipe

# Affichage du titre du jeu
print("=== COMBAT POKÉMON ===\n")

# Création des deux équipes de 5 Pokémon chacune
equipe1 = creer_equipe(5)
equipe2 = creer_equipe(5)

# Affichage de la composition de l'équipe 1
print("ÉQUIPE 1:")
for p in equipe1:
    print(f"  - {p['nom']} ({p['type']})")

# Affichage de la composition de l'équipe 2
print("\nÉQUIPE 2:")
for p in equipe2:
    print(f"  - {p['nom']} ({p['type']})")

# Début de la phase de combats
print("\n=== COMBATS ===")
# Initialisation des scores à 0
score1, score2 = 0, 0

# Boucle pour faire combattre les Pokémon un par un
for i in range(5):
    # Simulation du combat entre les Pokémon à l'index i
    gagnant = combat(equipe1[i], equipe2[i])
    # Si l'équipe 1 gagne
    if gagnant == 1:
        score1 += 1  # Incrémentation du score de l'équipe 1
        # Affichage du résultat : flèche pointant vers le perdant
        print(f"{equipe1[i]['nom']} ({equipe1[i]['type']}) -->> {equipe2[i]['nom']} ({equipe2[i]['type']})")
    # Si l'équipe 2 gagne
    else:
        score2 += 1  # Incrémentation du score de l'équipe 2
        # Affichage du résultat : flèche pointant vers le perdant
        print(f"{equipe1[i]['nom']} ({equipe1[i]['type']}) <<-- {equipe2[i]['nom']} ({equipe2[i]['type']})")

# Affichage du score final des deux équipes
print(f"\n=== SCORE: {score1} - {score2} ===")
# Détermination et affichage du vainqueur
if score1 > score2:
    print("ÉQUIPE 1 GAGNE!")  # L'équipe 1 a gagné plus de combats
elif score2 > score1:
    print("ÉQUIPE 2 GAGNE!")  # L'équipe 2 a gagné plus de combats
else:
    print("ÉGALITÉ!")  # Les deux équipes ont le même score

 