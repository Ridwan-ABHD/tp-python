import random

argent = 100
choix = ["pierre", "papier", "ciseaux"]

while argent > 0:
    print(f"\n Argent : {argent}€")
    mode = input("1-Jouer contre l'ordi | 2-Jouer à 2 : ")
    
    mise = int(input("Combien misez-vous ? "))
    if mise > argent:
        print("Pas assez d'argent !")
        continue
    
    joueur1 = input("Joueur 1 - Pierre, papier ou ciseaux ? ").lower()
    
    if mode == "1":
        joueur2 = random.choice(choix)
        print(f"Ordi : {joueur2}")
    else:
        joueur2 = input("Joueur 2 - Pierre, papier ou ciseaux ? ").lower()
    
    if joueur1 == joueur2:
        print(" Égalité !")
    elif (joueur1 == "pierre" and joueur2 == "ciseaux") or \
         (joueur1 == "papier" and joueur2 == "pierre") or \
         (joueur1 == "ciseaux" and joueur2 == "papier"):
        print(" Joueur 1 gagne !")
        argent += mise
    else:
        print(" Joueur 1 perd !")
        argent -= mise

print("\n Plus d'argent ! Game Over !")