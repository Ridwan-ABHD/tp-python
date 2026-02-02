# --- Données initiales ---
age = 27
legalAgeByCountry = {"fr": 18, "us": 21}
languageByCountry = {
    "fr": "francais", 
    "es": "espagnol", 
    "be": "francais", 
    "us": "anglais", 
    "au": "anglais", 
    "no": "neerlandais"
}
countryByLanguage = {} # Inutilisé dans le script original
allLanguage = []

def NightClubCheck(currentCountry):
    if i >= legalAgeByCountry[currentCountry]:
        print("on peut rentrer a ", i, " ans en ", currentCountry)


for i in range(age + 1):
    NightClubCheck("fr")
    NightClubCheck("us")


for country in languageByCountry:
    print(country, " parle en ", languageByCountry[country])
    try:
      
        allLanguage.index(languageByCountry[country])
    except:

        allLanguage.append(languageByCountry[country])

allLanguage.reverse()

# --- Affichage final ---
for langage in allLanguage:
    print(langage)