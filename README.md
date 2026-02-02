# Expert VIN & Musée Automobile

Application Python permettant de décoder des numéros VIN et de découvrir des véhicules légendaires.

**Projet Bachelor 2** - AntoineL, AntoineS, Ridwan

---

## Description

Cette application permet de :
- **Décoder un VIN** : Entrez un numéro VIN (17 caractères) pour obtenir les informations du véhicule via l'API NHTSA.
- **Visiter le Musée** : Découvrez 10 voitures légendaires chargées depuis un fichier JSON.
- **Gérer son Garage** : Consultez l'historique des véhicules scannés avec des statistiques (nombre, puissance moyenne, pays le plus fréquent).

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
| `models.py` | Logique métier (classe Vehicule, API, chargement JSON) |
| `legendes.json` | Liste des 10 véhicules légendaires du musée |

---

## Concepts Python utilisés

1. **Dictionnaires** - Stockage des données véhicules
2. **Listes** - Historique du garage
3. **Librairies** - requests, tkinter, random, json
4. **API Publique** - NHTSA (décodage VIN)
5. **Random** - Sélection aléatoire dans le musée
6. **JSON** - Lecture du fichier legendes.json avec `with open()`

---

## Véhicules du Musée

| Véhicule | Année | Pays | Puissance |
|----------|-------|------|-----------|
| Ferrari F40 | 1987 | Italie | 478 HP |
| DeLorean DMC-12 | 1981 | Irlande du Nord | 130 HP |
| Shelby AC Cobra | 1965 | USA/UK | 425 HP |
| Tesla Roadster | 2008 | USA | 248 HP |
| Mercedes A45S | 2023 | Allemagne | 421 HP |
| Volkswagen Golf 8R | 2022 | Allemagne | 320 HP |
| Mercedes GT63s | 2021 | Allemagne | 639 HP |
| Citroen Saxo VTS | 1999 | France | 120 HP |
| Lamborghini Urus | 2022 | Italie | 650 HP |
| Renault Scénic 3 | 2016 | France | 110 HP |

---

## Dépendances

- Python 3.x
- requests (`pip install requests`)
- tkinter (inclus avec Python)
- json (inclus avec Python)
