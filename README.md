# Expert VIN & Musée Automobile

Application Python permettant de décoder des numéros VIN et de découvrir des véhicules légendaires.

**Projet Bachelor 2** - AntoineL, AntoineS, Ridwan

---

## Description

Cette application permet de :
- **Décoder un VIN** : Entrez un numéro VIN (17 caractères) pour obtenir les informations du véhicule via l'API NHTSA.
- **Visiter le Musée** : Découvrez des voitures légendaires (Ferrari F40, DeLorean, Shelby Cobra, etc.).
- **Gérer son Garage** : Consultez l'historique des véhicules scannés avec des statistiques.

---

## Lancement

```bash
python main.py
```

---

## Structure du projet

| Fichier | Description |
|---------|-------------|
| `main.py` | Interface graphique (Tkinter) |
| `models.py` | Logique métier (classe Vehicule, API, musée) |

---

## Concepts Python utilisés

1. **Dictionnaires** - Stockage des données véhicules
2. **Listes** - Historique du garage
3. **Librairies** - requests, tkinter, random
4. **API Publique** - NHTSA (décodage VIN)
5. **Random** - Sélection aléatoire dans le musée

---

## Dépendances

- Python 3.x
- requests (`pip install requests`)
- tkinter (inclus avec Python)
