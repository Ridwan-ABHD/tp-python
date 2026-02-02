import random
from datetime import datetime, timedelta

# CONFIGURATION INITIALE
date_actuelle = datetime(2026, 1, 15).date()
compteur_ventes = 0   # 6.1
compteur_clients = 0  # 6.2
chiffre_affaires = 0  # ETAPE 6 CA Global

# Date de péremption
print("--- CONFIGURATION DU MAGASIN ---")
date_input = input("Entrez la date de péremption pour tous les produits alimentaires (JJ/MM/AA) : ")
date_peremption = datetime.strptime(date_input, "%d/%m/%y").date()

# CLASSES ETAPE 4 & 5
class Produit:
    def __init__(self, nom, prix, quantite):
        self.nom = nom
        self.prix = prix
        self.quantite = quantite

    def vendre_unite(self):
        """réduit le stock et gère le CA"""
        global chiffre_affaires
        if self.quantite > 0:
            self.quantite -= 1
            chiffre_affaires += self.prix
            print(f"Succès : 1 {self.nom} vendu ({self.prix}€).")
            return True
        else:
            print(f"Échec : {self.nom} est en rupture de stock.")
            return False

class ProduitAlimentaire(Produit):
    def vendre_unite(self):
        # [ETAPE 5] : Interdiction si périmé
        if date_actuelle > date_peremption:
            print(f"ERREUR : {self.nom} est périmé ! Vente impossible.")
            return False
        return super().vendre_unite()

class ProduitElectronique(Produit):
    def __init__(self, nom, prix, quantite, garantie):
        super().__init__(nom, prix, quantite)
        self.garantie = garantie 

# GESTION DU MAGASIN 
stock = {}

def afficher_stock():
    # ETAPE 2 affichage et statistiques
    print(f"\n--- INVENTAIRE AU {date_actuelle.strftime('%d/%m/%y')} ---")
    if not stock:
        print("Le stock est vide.")
        return

    valeur_totale_stock = 0
    for p in stock.values():
        valeur_totale_stock += p.prix * p.quantite
        txt = f"- {p.nom} | {p.prix}€ | Qte: {p.quantite}"
        if isinstance(p, ProduitElectronique):
            txt += f" | Garantie: {p.garantie}"
        print(txt)
    
    print("-" * 30)
    print(f"CHIFFRE D'AFFAIRES : {chiffre_affaires}€")
    print(f"Valeur du stock : {valeur_totale_stock}€")
    print(f"Date limite (Alim) : {date_peremption.strftime('%d/%m/%y')}")

# ETAPE 3 : MENU
while True:
    print("\n--- MENU MAGASIN ---")
    print("1. Voir stock | 2. Ajouter produit | 3. Achat Manuel (6.1) | 4. Client Aléatoire (6.2) | 5. Modifier stock | 6. Supprimer | 7. Quitter")
    choix = input("Choix : ")

    if choix == "1":
        afficher_stock()

    elif choix == "2":
        nom = input("Nom : ")
        prix = float(input("Prix : "))
        qte = int(input("Quantité : "))
        cat = input("Alimentaire (a) ou Electronique (e) ? ").lower()
        if cat == 'a':
            stock[nom] = ProduitAlimentaire(nom, prix, qte)
        else:
            garantie = input("Durée de garantie : ")
            stock[nom] = ProduitElectronique(nom, prix, qte, garantie)

    elif choix == "3":
        # ETAPE 6.1 : Achat manuel
        nom_achat = input("Quel produit voulez-vous acheter ? ")
        if nom_achat in stock:
            if stock[nom_achat].vendre_unite():
                compteur_ventes += 1
                # Avance de 1 jour tous les 3 achats
                if compteur_ventes % 3 == 0:
                    date_actuelle += timedelta(days=1)
                    print(f"--- Le temps avance... Nous sommes le {date_actuelle.strftime('%d/%m/%y')} ---")
        else:
            print("Produit introuvable.")

    elif choix == "4":
        # ETAPE 6.2 : Client Aléatoire
        if not stock:
            print("Magasin vide !")
            continue
        
        # Un client achète entre 1 et 3 produits
        nb_articles = random.randint(1, 3)
        print(f"\nUn client arrive pour acheter {nb_articles} article(s)...")
        
        for _ in range(nb_articles):
            nom_hasard = random.choice(list(stock.keys()))
            stock[nom_hasard].vendre_unite()
        
        compteur_clients += 1
        # Avance de 1 jour tous les 3 clients
        if compteur_clients % 3 == 0:
            date_actuelle += timedelta(days=1)
            print(f"--- INFO : 3 clients sont passés, la date avance au {date_actuelle.strftime('%d/%m/%y')} ---")

    elif choix == "5":
        nom = input("Nom du produit : ")
        if nom in stock:
            nouvelle_qte = int(input(f"Quantité à ajouter pour {nom} : "))
            stock[nom].quantite += nouvelle_qte
        else:
            print("Produit introuvable.")

    elif choix == "6":
        nom = input("Nom du produit à supprimer : ")
        if nom in stock:
            del stock[nom]

    elif choix == "7":
        print(f"Fermeture. CA Final : {chiffre_affaires}€")
        break