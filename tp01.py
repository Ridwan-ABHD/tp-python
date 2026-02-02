# TP Python (01) - Gestion simplifiée d'un magasin
# Travail progressif avec toutes les étapes intégrées

from datetime import datetime, timedelta
import random

# ========== ÉTAPE 4 & 5 : CLASSES ==========

class Produit:
    """Classe de base pour un produit"""
    def __init__(self, nom, prix, quantite, rayon):
        self.nom = nom
        self.prix = prix
        self.quantite = quantite
        self.rayon = rayon
    
    def vendre(self, qte=1):
        """Vend une quantité de produit"""
        if self.quantite >= qte:
            self.quantite -= qte
            return True
        return False
    
    def afficher(self):
        """Affiche les informations du produit"""
        return f"{self.nom} - {self.prix}€ - Stock: {self.quantite} - Rayon: {self.rayon}"

class ProduitAlimentaire(Produit):
    """Produit alimentaire avec date d'expiration"""
    def __init__(self, nom, prix, quantite, rayon, date_peremption):
        super().__init__(nom, prix, quantite, rayon)
        self.date_peremption = date_peremption
    
    def est_perime(self, date_actuelle):
        """Vérifie si le produit est périmé"""
        return date_actuelle > self.date_peremption
    
    def vendre(self, qte=1, date_actuelle=None):
        """Vend si non périmé"""
        if date_actuelle and self.est_perime(date_actuelle):
            print(f"❌ {self.nom} est périmé!")
            return False
        return super().vendre(qte)
    
    def afficher(self):
        return f"{super().afficher()} - Expire le: {self.date_peremption.strftime('%d/%m/%Y')}"

class ProduitElectronique(Produit):
    """Produit électronique avec garantie"""
    def __init__(self, nom, prix, quantite, rayon, garantie_mois):
        super().__init__(nom, prix, quantite, rayon)
        self.garantie_mois = garantie_mois
    
    def afficher(self):
        return f"{super().afficher()} - Garantie: {self.garantie_mois} mois"

# ========== GESTION DU MAGASIN ==========

class Magasin:
    """Classe pour gérer le magasin"""
    def __init__(self):
        self.stock = {}
        self.chiffre_affaires = 0.0
        self.date_actuelle = datetime.now()
    
    def ajouter_produit(self, produit):
        """Ajoute un produit au stock"""
        self.stock[produit.nom] = produit
    
    def afficher_stock(self):
        """Affiche tout le stock"""
        print("\n📦 === STOCK DU MAGASIN ===")
        if not self.stock:
            print("Stock vide")
        for produit in self.stock.values():
            print(f"  • {produit.afficher()}")
        print(f"💰 Chiffre d'affaires: {self.chiffre_affaires:.2f}€")
        print(f"📅 Date actuelle: {self.date_actuelle.strftime('%d/%m/%Y')}\n")
    
    def calculer_valeur_stock(self):
        """Calcule la valeur totale du stock"""
        return sum(p.prix * p.quantite for p in self.stock.values())
    
    def produit_plus_cher(self):
        """Trouve le produit le plus cher"""
        if not self.stock:
            return None
        return max(self.stock.values(), key=lambda p: p.prix)
    
    def produit_plus_quantite(self):
        """Trouve le produit avec le plus de quantité"""
        if not self.stock:
            return None
        return max(self.stock.values(), key=lambda p: p.quantite)
    
    def vendre_produit(self, nom_produit, qte=1):
        """Vend un produit"""
        if nom_produit not in self.stock:
            print(f"❌ Produit '{nom_produit}' introuvable")
            return False
        
        produit = self.stock[nom_produit]
        
        # Vérification pour produit alimentaire
        if isinstance(produit, ProduitAlimentaire):
            if produit.vendre(qte, self.date_actuelle):
                montant = produit.prix * qte
                self.chiffre_affaires += montant
                print(f"✅ Vendu {qte}x {nom_produit} pour {montant:.2f}€")
                return True
        else:
            if produit.vendre(qte):
                montant = produit.prix * qte
                self.chiffre_affaires += montant
                print(f"✅ Vendu {qte}x {nom_produit} pour {montant:.2f}€")
                return True
            else:
                print(f"❌ Stock insuffisant pour {nom_produit}")
        return False
    
    def avancer_jour(self, jours=1):
        """Avance la date"""
        self.date_actuelle += timedelta(days=jours)
        print(f"⏰ Date avancée au {self.date_actuelle.strftime('%d/%m/%Y')}")

# ========== FONCTIONS PRINCIPALES ==========

def saisie_initiale():
    """Étape 1 & 2 : Saisie du stock initial"""
    magasin = Magasin()
    
    print("=== SAISIE DU STOCK INITIAL ===")
    print("Tapez 'stop' pour terminer\n")
    
    while True:
        nom = input("Nom du produit (ou 'stop'): ").strip()
        if nom.lower() == 'stop':
            break
        
        try:
            type_produit = input("Type (1=Alimentaire, 2=Électronique, 3=Standard): ").strip()
            prix = float(input("Prix: "))
            quantite = int(input("Quantité: "))
            rayon = input("Rayon: ").strip()
            
            if type_produit == '1':
                jours = int(input("Jours avant péremption: "))
                date_peremption = datetime.now() + timedelta(days=jours)
                produit = ProduitAlimentaire(nom, prix, quantite, rayon, date_peremption)
            elif type_produit == '2':
                garantie = int(input("Garantie (mois): "))
                produit = ProduitElectronique(nom, prix, quantite, rayon, garantie)
            else:
                produit = Produit(nom, prix, quantite, rayon)
            
            magasin.ajouter_produit(produit)
            print(f"✅ {nom} ajouté!\n")
        
        except ValueError:
            print("❌ Erreur de saisie, réessayez\n")
    
    return magasin

def menu_interactif(magasin):
    """Étape 3 : Menu interactif"""
    while True:
        print("\n=== MENU ===")
        print("1. Afficher le stock")
        print("2. Ajouter un produit")
        print("3. Modifier une quantité")
        print("4. Supprimer un produit")
        print("5. Statistiques")
        print("6. Mode vente manuelle")
        print("7. Mode vente automatique")
        print("0. Quitter")
        
        choix = input("\nChoix: ").strip()
        
        if choix == '1':
            magasin.afficher_stock()
        
        elif choix == '2':
            nom = input("Nom: ").strip()
            try:
                type_produit = input("Type (1=Alim, 2=Élec, 3=Standard): ").strip()
                prix = float(input("Prix: "))
                quantite = int(input("Quantité: "))
                rayon = input("Rayon: ").strip()
                
                if type_produit == '1':
                    jours = int(input("Jours avant péremption: "))
                    date_peremption = magasin.date_actuelle + timedelta(days=jours)
                    produit = ProduitAlimentaire(nom, prix, quantite, rayon, date_peremption)
                elif type_produit == '2':
                    garantie = int(input("Garantie (mois): "))
                    produit = ProduitElectronique(nom, prix, quantite, rayon, garantie)
                else:
                    produit = Produit(nom, prix, quantite, rayon)
                
                magasin.ajouter_produit(produit)
                print(f"✅ {nom} ajouté!")
            except ValueError:
                print("❌ Erreur de saisie")
        
        elif choix == '3':
            nom = input("Nom du produit: ").strip()
            if nom in magasin.stock:
                try:
                    nouvelle_qte = int(input("Nouvelle quantité: "))
                    magasin.stock[nom].quantite = nouvelle_qte
                    print("✅ Quantité modifiée")
                except ValueError:
                    print("❌ Quantité invalide")
            else:
                print("❌ Produit introuvable")
        
        elif choix == '4':
            nom = input("Nom du produit: ").strip()
            if nom in magasin.stock:
                del magasin.stock[nom]
                print("✅ Produit supprimé")
            else:
                print("❌ Produit introuvable")
        
        elif choix == '5':
            print(f"\n📊 Valeur totale du stock: {magasin.calculer_valeur_stock():.2f}€")
            plus_cher = magasin.produit_plus_cher()
            if plus_cher:
                print(f"💎 Produit le plus cher: {plus_cher.nom} ({plus_cher.prix}€)")
            plus_stock = magasin.produit_plus_quantite()
            if plus_stock:
                print(f"📦 Plus grande quantité: {plus_stock.nom} ({plus_stock.quantite})")
        
        elif choix == '6':
            mode_vente_manuelle(magasin)
        
        elif choix == '7':
            mode_vente_automatique(magasin)
        
        elif choix == '0':
            print("👋 Au revoir!")
            break
        
        else:
            print("❌ Choix invalide")

def mode_vente_manuelle(magasin):
    """Étape 6.1 : Vente manuelle avec avancement du temps"""
    print("\n=== MODE VENTE MANUELLE ===")
    compteur_achats = 0
    
    while True:
        produit = input("Produit à acheter (ou 'stop'): ").strip()
        if produit.lower() == 'stop':
            break
        
        try:
            qte = int(input("Quantité: "))
            magasin.vendre_produit(produit, qte)
            compteur_achats += 1
            
            # Tous les 3 achats, on avance d'un jour
            if compteur_achats % 3 == 0:
                magasin.avancer_jour(1)
        except ValueError:
            print("❌ Quantité invalide")

def mode_vente_automatique(magasin):
    """Étape 6.2 : Vente automatique avec remboursements"""
    print("\n=== MODE VENTE AUTOMATIQUE ===")
    nb_clients = int(input("Nombre de clients à simuler: "))
    
    produits_disponibles = list(magasin.stock.keys())
    if not produits_disponibles:
        print("❌ Aucun produit en stock")
        return
    
    for i in range(1, nb_clients + 1):
        print(f"\n--- Client #{i} ---")
        
        # 10% de chance de demander un remboursement
        if random.random() < 0.1 and magasin.chiffre_affaires > 0:
            # Tentative de remboursement
            remboursable = random.choice([True, False])
            if remboursable:
                montant = random.uniform(5, 20)
                magasin.chiffre_affaires -= montant
                print(f"💸 Remboursement accepté: {montant:.2f}€")
            else:
                print("❌ Remboursement refusé (produit non remboursable)")
        else:
            # Achat normal
            nb_produits = random.randint(1, 3)
            print(f"Client achète {nb_produits} produit(s)")
            
            for _ in range(nb_produits):
                produit = random.choice(produits_disponibles)
                magasin.vendre_produit(produit, 1)
        
        # Tous les 3 clients, on avance d'un jour
        if i % 3 == 0:
            magasin.avancer_jour(1)
    
    print(f"\n✅ Simulation terminée - CA final: {magasin.chiffre_affaires:.2f}€")

# ========== PROGRAMME PRINCIPAL ==========

def main():
    """Fonction principale"""
    print("🏪 === GESTION DE MAGASIN ===\n")
    
    # Choix du mode de démarrage
    print("1. Saisie manuelle du stock")
    print("2. Stock de démonstration")
    choix = input("Choix: ").strip()
    
    if choix == '2':
        # Stock de démonstration
        magasin = Magasin()
        magasin.ajouter_produit(ProduitAlimentaire("Pain", 1.5, 20, "Boulangerie", datetime.now() + timedelta(days=2)))
        magasin.ajouter_produit(ProduitAlimentaire("Lait", 1.2, 15, "Frais", datetime.now() + timedelta(days=5)))
        magasin.ajouter_produit(ProduitElectronique("Souris", 15.99, 10, "Informatique", 24))
        magasin.ajouter_produit(ProduitElectronique("Clavier", 29.99, 5, "Informatique", 24))
        magasin.ajouter_produit(Produit("Cahier", 2.5, 30, "Papeterie"))
        print("✅ Stock de démonstration créé!")
    else:
        magasin = saisie_initiale()
    
    # Affichage initial
    magasin.afficher_stock()
    
    # Menu interactif
    menu_interactif(magasin)

if __name__ == "__main__":
    main()
