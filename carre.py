import time
from colorama import Fore, Style, init

# Initialisation pour gérer les couleurs dans la console
init(autoreset=True)

COULEURS = [
    Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA,
    Fore.CYAN, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX,
    Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX
]

def lire_instance(fichier):
    with open(fichier, "r") as f:
        largeur = int(f.readline().strip())
        hauteur = int(f.readline().strip())
        contenu = f.readline().strip()
        matrice = []
        for i in range(hauteur):
            ligne = contenu[i * largeur:(i + 1) * largeur]
            matrice.append([int(c) for c in ligne])
    return largeur, hauteur, matrice

def afficher_matrice(matrice):
    for ligne in matrice:
        ligne_affichee = ""
        for case in ligne:
            if case == 1:
                couleur = Fore.WHITE
                ligne_affichee += f"{couleur}## "
            elif case == 0:
                ligne_affichee += ".. "
            else:
                couleur = COULEURS[(case - 2) % len(COULEURS)]
                ligne_affichee += f"{couleur}{case:02d} "
        print(ligne_affichee.strip())

def est_valide(matrice, x, y, taille):
    if x + taille > len(matrice) or y + taille > len(matrice[0]):
        return False
    for i in range(taille):
        for j in range(taille):
            if matrice[x + i][y + j] != 0:
                return False
    return True

def placer_carre(matrice, x, y, taille, valeur):
    for i in range(taille):
        for j in range(taille):
            matrice[x + i][y + j] = valeur

def copier_matrice(matrice):
    return [ligne[:] for ligne in matrice]

def couverture_minimale(matrice):
    meilleur_resultat = float('inf')
    meilleure_matrice = None
    tentative_count = 0

    def recherche_minimum(matrice, x, y, largeur, hauteur, couverture_actuelle, indice):
        nonlocal meilleur_resultat, meilleure_matrice, tentative_count
        
        tentative_count += 1
        
        # Élagage
        if couverture_actuelle >= meilleur_resultat:
            return
        
        # Si toutes les cases sont couvertes
        if all(all(c != 0 for c in row) for row in matrice):
            meilleur_resultat = couverture_actuelle
            meilleure_matrice = copier_matrice(matrice)
            return
        
        # Trouver la première case vide
        for i in range(x, hauteur):
            for j in range(y if i == x else 0, largeur):
                if matrice[i][j] == 0:
                    # Essayer de placer des carrés de taille décroissante
                    for taille in range(min(largeur - j, hauteur - i), 0, -1):
                        if est_valide(matrice, i, j, taille):
                            placer_carre(matrice, i, j, taille, indice)
                            recherche_minimum(matrice, i, j, largeur, hauteur, couverture_actuelle + 1, indice + 1)
                            placer_carre(matrice, i, j, taille, 0)
                    return
        return
    
    largeur, hauteur = len(matrice[0]), len(matrice)
    indice_initial = 2

    debut = time.process_time()
    recherche_minimum(matrice, 0, 0, largeur, hauteur, 0, indice_initial)
    fin = time.process_time()
    
    print(f"Nombre de tentatives : {tentative_count}")
    if meilleure_matrice:
        afficher_matrice(meilleure_matrice)
    temps_cpu = fin - debut
    print(f"Temps CPU : {temps_cpu:.4f} secondes")
    
    return meilleur_resultat

# Exemple d'appel avec un fichier lu précédemment
fichier = "tests/s4.txt"
largeur, hauteur, matrice = lire_instance(fichier)
afficher_matrice(matrice)  # Afficher la matrice pour la visualiser

# Calculer et afficher le nombre minimal de carrés nécessaires
resultat = couverture_minimale(matrice)
print("Nombre minimal de carrés nécessaires :", resultat)