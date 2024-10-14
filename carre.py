from colorama import Fore, Style, init

# Initialisation pour gérer les couleurs dans la console
init(autoreset=True)

# Liste de quelques couleurs disponibles dans colorama
COULEURS = [
    Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, 
    Fore.CYAN, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX
]

def lire_instance(fichier):
    # Lire le fichier et extraire la largeur, la hauteur et la matrice
    with open(fichier, "r") as f:
        largeur = int(f.readline().strip())
        hauteur = int(f.readline().strip())
        contenu = f.readline().strip()  # Lire la matrice sous forme de chaîne unique
        matrice = []
        # Diviser la chaîne en lignes de la longueur 'largeur'
        for i in range(hauteur):
            ligne = contenu[i * largeur:(i + 1) * largeur]
            matrice.append([int(c) for c in ligne])  # Convertir chaque caractère en entier (0 ou 1)
    return largeur, hauteur, matrice

def afficher_matrice(matrice):
    """Affiche la matrice sous forme lisible avec les indices des carrés, chaque carré ayant une couleur différente."""
    for ligne in matrice:
        ligne_affichee = ""
        for case in ligne:
            if case == 1:
                couleur = Fore.WHITE
                ligne_affichee += f"{couleur}## "  # Case avec obstacle
            elif case == 0:
                ligne_affichee += ".. "  # Case vide
            else:
                # Assigner une couleur à chaque indice de carré (en mod utilisant l'index de couleur)
                couleur = COULEURS[(case - 2) % len(COULEURS)]
                ligne_affichee += f"{couleur}{case:02d} "  # Case occupée par un carré avec une couleur
        print(ligne_affichee.strip())

def est_valide(matrice, x, y, taille):
    """Vérifie si un carré de taille `taille` peut être placé à la position (x, y) sans sortir des limites ou chevaucher un obstacle."""
    if x + taille > len(matrice) or y + taille > len(matrice[0]):
        return False  # Si le carré dépasse les limites
    for i in range(taille):
        for j in range(taille):
            if matrice[x + i][y + j] != 0:  # Si la case est déjà couverte ou s'il y a un obstacle
                return False
    return True

def placer_carre(matrice, x, y, taille, valeur):
    """Place ou enlève un carré de taille `taille` à la position (x, y) en fonction de `valeur` (indice du carré)."""
    for i in range(taille):
        for j in range(taille):
            matrice[x + i][y + j] = valeur  # Marque les cases avec l'indice du carré

def copie_matrice(matrice):
    """Renvoie une copie profonde de la matrice."""
    return [ligne[:] for ligne in matrice]

def couverture_minimale(matrice):
    """Retourne le nombre minimal de carrés nécessaires pour couvrir toutes les cases vides de la matrice, et affiche la matrice finale remplie."""
    meilleur_resultat = float('inf')
    meilleure_matrice = None
    
    def recherche_minimum(matrice, x, y, largeur, hauteur, couverture_actuelle, indice):
        nonlocal meilleur_resultat, meilleure_matrice
        
        if couverture_actuelle >= meilleur_resultat:
            return  # Arrêter si le nombre de carrés dépasse déjà le meilleur résultat trouvé
        
        # Si toutes les cases sont couvertes
        if all(all(c != 0 for c in row) for row in matrice):
            meilleur_resultat = couverture_actuelle
            meilleure_matrice = copie_matrice(matrice)  # Sauvegarder la matrice courante comme solution optimale
            return
        
        # Trouver la première case vide
        for i in range(x, hauteur):
            for j in range(y if i == x else 0, largeur):
                if matrice[i][j] == 0:
                    # Essayer de placer des carrés de taille décroissante
                    for taille in range(min(largeur - j, hauteur - i), 0, -1):
                        if est_valide(matrice, i, j, taille):
                            # Placer un carré avec un indice unique
                            placer_carre(matrice, i, j, taille, indice)
                            # Rechercher plus loin
                            recherche_minimum(matrice, i, j, largeur, hauteur, couverture_actuelle + 1, indice + 1)
                            # Retirer le carré (backtracking)
                            placer_carre(matrice, i, j, taille, 0)
                    return  # Retourner après avoir essayé toutes les tailles de carré
        return
    
    largeur, hauteur = len(matrice[0]), len(matrice)
    indice_initial = 2  # On commence l'indice des carrés à 2, car 0 et 1 sont déjà utilisés
    recherche_minimum(matrice, 0, 0, largeur, hauteur, 0, indice_initial)
    
    # Après la recherche, afficher la matrice avec les indices des carrés
    print("\nMatrice remplie avec indices des carrés :")
    if meilleure_matrice:
        afficher_matrice(meilleure_matrice)
    
    return meilleur_resultat

# Exemple d'appel avec un fichier lu précédemment
fichier = "tests/s1.txt"
largeur, hauteur, matrice = lire_instance(fichier)
afficher_matrice(matrice)  # Afficher la matrice pour la visualiser

# Calculer et afficher le nombre minimal de carrés nécessaires
resultat = couverture_minimale(matrice)
print("Nombre minimal de carrés nécessaires:", resultat)