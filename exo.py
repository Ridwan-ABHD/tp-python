infoByNames = {
    "LEMESLE": {"name": "Antoine", "birthMonth": 12, "age": 19},
    "SIMON": {"name": "Antoine", "birthMonth": 5, "age": 19},
    "LAGRANGE": {"name": "Augustin", "birthMonth": 5, "age": 19},
    "COURAULT": {"name": "Edouard", "birthMonth": 3, "age": 20},
    "TURCAS": {"name": "Henri", "birthMonth": 10, "age": 19},
    "MEURIEL": {"name": "Hugo", "birthMonth": 8, "age": 19},
    "DUSSAUD": {"name": "Jean-Marc", "birthMonth": 11, "age": 25},
    "ALANDJI": {"name": "Kelvya", "birthMonth": 5, "age": 18},
    "BRUEL": {"name": "Mathis", "birthMonth": 6, "age": 19},
    "LEFORT": {"name": "Maxime", "birthMonth": 2, "age": 19},
    "DURAND": {"name": "Rémi", "birthMonth": 6, "age": 20},
    "ABDOULKADER HOUMED": {"name": "Ridwan", "birthMonth": 11, "age": 19},
    "LETORT": {"name": "Sébastien", "birthMonth": 6, "age": 20},
    "BARRAUD": {"name": "Teddy", "birthMonth": 6, "age": 19}
}

Axel = {
    "name": "Axel",
    "surname": "BULLET",
    "birthMonth": 9,
    "age": 27
}

infoByNames[Axel["surname"]] = {
    "name": Axel["name"],
    "birthMonth": Axel["birthMonth"],
    "age": Axel["age"]
}

MonthByNames = {}
for surname, eleve in infoByNames.items():
    month = eleve["birthMonth"]
    if month not in MonthByNames:
        MonthByNames[month] = []
    MonthByNames[month].append(eleve["name"])

print("Regroupement par mois de naissance :")
print(MonthByNames)

# par âge puis par mois
trieParAge = sorted(infoByNames.items(), key=lambda x: (x[1]["age"], x[1]["birthMonth"]))
print("\nTrié par âge puis par mois :")
for surname, info in trieParAge:
    print(f"{info['name']} {surname} - {info['age']} ans, mois {info['birthMonth']}")
