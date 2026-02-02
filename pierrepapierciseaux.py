import random
import getpass

feuille = ["pierre", "papier", "ciseaux"]
somme = 20

def jouer_ordi(mise):
    choixOrdi = random.choice(feuille)
    choixUser = getpass.getpass("Choisissez pierre, papier ou ciseaux : ").lower()

    if (choixOrdi == "pierre" and choixUser == "ciseaux") or \
         (choixOrdi == "papier" and choixUser == "pierre") or \
         (choixOrdi == "ciseaux" and choixUser == "papier"):
        print("L'ordinateur a choisi", choixOrdi, ". Vous avez perdu !")
        return -mise
    elif choixOrdi == choixUser:
        print("L'ordinateur a choisi", choixOrdi, ". Égalité !")
        return 0
    else:
        print("L'ordinateur a choisi", choixOrdi, ". Vous avez gagné !")
        return mise


def jouer():
    choix_joueur1 = getpass.getpass("Choisissez pierre, papier ou ciseaux : ").lower()
    choix_joueur2 = getpass.getpass("Choisissez pierre, papier ou ciseaux : ").lower()

    if (choix_joueur1 == "pierre" and choix_joueur2 == "ciseaux") or \
         (choix_joueur1 == "papier" and choix_joueur2 == "pierre") or \
         (choix_joueur1 == "ciseaux" and choix_joueur2 == "papier"):
        print("Le joueur 2 a choisi", choix_joueur2)
        print("Le joueur 1 a choisi", choix_joueur1, ". bravo joueur 1 !")
        return 
    elif choix_joueur1 == choix_joueur2:
        print("Le joueur 2 a choisi", choix_joueur2)
        print("Le joueur 1 a choisi", choix_joueur1, ". Égalité !")
        return 
    else:
        print("Le joueur 2 a choisi", choix_joueur2)
        print("Le joueur 1 a choisi", choix_joueur1, ". bravo joueur 2 !")
        return 


while somme > 0:
    jeu = input("\nVoulez-vous jouer contre l'ordinateur (o/n) ? ").lower()
    if jeu == 'o':
        print("\nVous avez", somme, "euros.")
        mise = input("Combien voulez-vous miser ? ")
        mise = int(mise)

        if mise > somme or mise <= 0:
            print("Vous ne pouvez pas miser plus que ce que vous avez et il faut miser plus que 0 !")
            continue

        resultat = jouer_ordi(mise)
        somme += resultat
    else:
        jouer()
        break

print("\nVous n'avez plus d'argent. Game Over !")

 