import random
from datetime import datetime, timedelta

# ETAPE 6 : CONFIGURATION ET CHIFFRE D'AFFAIRES ---
date_actuelle = datetime(2026, 1, 15).date()
chiffre_affaires = 0
compteur_ventes = 0   # Pour 6.1
compteur_clients = 0  # Pour 6.2

# ETAPE 1 : Saisie initiale
print("--- CONFIGURATION DU MAGASIN ---")
date_input = input("Entrez la date de péremption pour les produits alimentaires (JJ/MM/AA) : ")
date_peremption = datetime.strptime(date_input, "%d/%m/%y").date()

# ETAPE 4 & 5 : CLASSES ET HERITAGE
class Produit:
    def __init__(self, nom, prix, quantite):
        self.nom = nom
        self.prix = prix
        self.quantite = quantite

    def vendre_unite(self):
        """[ETAPE 4] : Méthode de vente de base"""
        global chiffre_affaires
        if self.quantite > 0:
            self.quantite -= 1
            chiffre_affaires += self.prix
            print(f"Succès : 1 {self.nom} vendu ({self.prix}€).")
            return True
        print(f"Échec : {self.nom} est en rupture de stock.")
        return False

class ProduitAlimentaire(Produit):
    def vendre_unite(self):
        """[ETAPE 5] : Interdiction si périmé"""
        if date_actuelle > date_peremption:
            print(f"ERREUR : {self.nom} est périmé ! Vente impossible.")
            return False
        return super().vendre_unite()

class ProduitElectronique(Produit):
    def __init__(self, nom, prix, quantite, garantie):
        """[ETAPE 5] : Sous-classe avec attribut garantie"""
        super().__init__(nom, prix, quantite)
        self.garantie = garantie 

# ETAPE 2 STOCK
stock = {} # Dictionnaire

def afficher_stock():
    """[ETAPE 2] : Affichage, Valeur totale et Statistiques"""
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
    
    # statistiques
    plus_cher = max(stock.values(), key=lambda x: x.prix)
    print("-" * 30)
    print(f"CHIFFRE D'AFFAIRES : {chiffre_affaires}€")
    print(f"Valeur du stock : {valeur_totale_stock}€")
    print(f"Produit le plus cher : {plus_cher.nom}")
    print(f"Date limite (Alim) : {date_peremption.strftime('%d/%m/%y')}")

# ETAPE 3 : MENU INTERACTIF 
while True:
    print("\n--- MENU MAGASIN ---")
    print("1. Voir stock | 2. Ajouter produit | 3. Achat Manuel (6.1)")
    print("4. Client Aléatoire (6.2) | 5. Modifier stock | 6. Supprimer | 7. Quitter")
    choix = input("Choix : ")

    if choix == "1":
        afficher_stock()

    elif choix == "2":
        # 1 & 3Saisie et ajout au dictionnaire
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
                if compteur_ventes % 3 == 0:
                    date_actuelle += timedelta(days=1)
                    print(f"--- INFO : 3 achats effectués, le temps avance au {date_actuelle} ---")
        else:
            print("Produit introuvable.")

    elif choix == "4":
        # ETAPE 6.2 : client Aléatoire
        if not stock:
            print("Magasin vide !")
            continue
        
        nb_articles = random.randint(1, 3)
        print(f"\nUn client arrive pour {nb_articles} article(s)...")
        for _ in range(nb_articles):
            nom_hasard = random.choice(list(stock.keys()))
            stock[nom_hasard].vendre_unite()
        
        compteur_clients += 1
        if compteur_clients % 3 == 0:
            date_actuelle += timedelta(days=1)
            print(f"--- INFO : 3 clients sont passés, la date avance au {date_actuelle} ---")

        # ETAPE 6.2 : Remboursement 
        if random.random() < 0.3:
            p_retour = random.choice(list(stock.values()))
            print(f"--- Client tente un remboursement pour : {p_retour.nom} ---")
            # Remboursable si Electronique ou chance aléatoire
            if isinstance(p_retour, ProduitElectronique) or random.choice([True, False]):
                chiffre_affaires -= p_retour.prix
                p_retour.quantite += 1
                print(f"Remboursement ACCEPTE. CA actuel : {chiffre_affaires}€")
            else:
                print("Remboursement REFUSE.")

    elif choix == "5":
        # ETAPE 3Modifier une quantité
        nom = input("Nom du produit : ")
        if nom in stock:
            nouvelle_qte = int(input(f"Quantité à ajouter pour {nom} : "))
            stock[nom].quantite += nouvelle_qte
            print("Stock mis à jour.")
        else:
            print("Produit introuvable.")

    elif choix == "6":
        # étape 3 Supprimer
        nom = input("Nom du produit à supprimer : ")
        if nom in stock:
            del stock[nom]
            print(f"{nom} supprimé.")

    elif choix == "7":
        print(f"Fermeture. Chiffre d'Affaires Final : {chiffre_affaires}€")
        break