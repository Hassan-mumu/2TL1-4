# Importer les classes nécessaires
from Interface import *  # Assurer que l'interface est correctement initialisée avec des tables
import tkinter as tk

#Constantes
RED_COLOR = "indianred"
DARK_CREAM_COLOR = "#FAF0E6"
LIGHT_CREAM_COLOR = "#FFFAF0"
POlICE = "Garamond"
BTN_SIZE_X = 20
BTN_SIZE_Y = 10


# test init
interface = Interface()

for i in range(1, 21):
    if i <= 10:
        interface.addTable(Table(2))
    elif i <= 16:
        interface.addTable(Table(4))
    else:
        interface.addTable(Table(6))

interface.makeReservation()

# Créer la fenêtre principale
fenetre = tk.Tk()
fenetre.geometry("1920x1080")
fenetre.title("La bonne fourchette")
fenetre.configure(background=DARK_CREAM_COLOR, pady=20)

# Méthodes

# Fonction pour afficher les tables dans la frame de droite
def afficher_tables():
    # Effacer le contenu actuel de la zone d'affichage
    for widget in frame_droite.winfo_children():
        widget.destroy()
    tables = interface._all_table
    x = y = 0
    
    # Créer un cadre pour organiser les tables
    for table in tables:
        cadre_table = tk.Frame(frame_droite, background="white", pady=10, padx=10, relief="raised", borderwidth=2)
        cadre_table.grid(pady=10, padx=10, column=x, row=y)
        if x == 3:
            y +=1
        x = (x + 1) % 4
        # Informations sur la table
        label_id = tk.Label(cadre_table, text=f"Table ID : {table.getId()}", font=(POlICE, 16), background="white")
        label_id.pack(anchor="w", padx=10)
        
        label_places = tk.Label(cadre_table, text=f"Places : {table.getSeat_nbr()}", font=(POlICE, 16), background="white")
        label_places.pack(anchor="w", padx=10)
        
        label_etat = tk.Label(cadre_table, text=f"État : {table.getState()}", font=(POlICE, 16), background="white")
        label_etat.pack(anchor="w", padx=10)


def afficher_reservation():
    for widget in frame_droite.winfo_children():
        widget.destroy()
    reservations = interface._reservations_list
    x = y = 0
    
    # Créer un cadre pour organiser les tables
    for reservation in reservations:
        cadre_table = tk.Frame(frame_droite, background="white", pady=10, padx=10, relief="raised", borderwidth=2)
        cadre_table.grid(pady=10, padx=10, column=x, row=y)
        if x == 3:
            y +=1
        x = (x + 1) % 4

        # Informations sur la table
        label_id = tk.Label(cadre_table, text=f"Name : {reservation.getName()}", font=(POlICE, 16), background="white")
        label_id.pack(anchor="w", padx=10)
        
        label_etat = tk.Label(cadre_table, text=f"Table(s) : {reservation.getTable()}", font=(POlICE, 16), background="white")
        label_etat.pack(anchor="w", padx=10)

        label_places = tk.Label(cadre_table, text=f"Date : {reservation.getDate()}", font=(POlICE, 16), background="white")
        label_places.pack(anchor="w", padx=10)
        
        label_etat = tk.Label(cadre_table, text=f"Hour : {reservation.getHour()}", font=(POlICE, 16), background="white")
        label_etat.pack(anchor="w", padx=10)


# Titre de la partie gauche
label_titre = tk.Label(fenetre, text="La Bonne Fourchette", font=(POlICE, 34, "bold"), background=DARK_CREAM_COLOR, anchor="w")
label_titre.pack(pady=(10, 0), padx=(50, 0), anchor="nw")  # Ancrer en haut à gauche

# Créer une frame pour la partie gauche (40% de la largeur)
frame_gauche = tk.Frame(fenetre, width=0.35*1920, background=LIGHT_CREAM_COLOR)
frame_gauche.pack(side="left", fill="y", padx=10)
frame_gauche.pack_propagate(False)  # Fixer la taille


# Créer la frame des boutons à l'intérieur de frame_gauche
frame_boutons = tk.Frame(frame_gauche, background=LIGHT_CREAM_COLOR)
frame_boutons.pack(pady=20, padx=20, fill="y")

# Ligne de séparation
ligne_separation = tk.Frame(fenetre, width=5, background="white")
ligne_separation.pack(side="left", fill="y")

# Créer la zone d'affichage sur la droite (60% de la largeur)
frame_droite = tk.Frame(fenetre, width=0.55*1920, background=LIGHT_CREAM_COLOR)
frame_droite.pack(side="left", fill="both", padx=50, expand=True)
frame_droite.pack_propagate(False)  # Fixer la taille

# Zone de texte affichant le message
zone_affichage = tk.Label(frame_droite, text="", font=("Garamond", 20), background="#FFF5EE", justify="center")
zone_affichage.pack(pady=20, padx=20, anchor="center")


# bouton pour afficher les tables
bouton = tk.Button(
    frame_boutons, text="Afficher les Tables", font=(POlICE, 18),  height=BTN_SIZE_Y, width=BTN_SIZE_X, background=RED_COLOR,
    command=afficher_tables
)
bouton.grid(pady=20, padx=10, row=0, column=0)

# bouton pour afficher les réservations
bouton = tk.Button(
    frame_boutons, text="Afficher les Reservations", font=(POlICE, 18) , height=BTN_SIZE_Y, width=BTN_SIZE_X, background=RED_COLOR,
    command=afficher_reservation
)
bouton.grid(pady=20, padx=10, row=0, column=1)


# Lancer la boucle principale de la fenêtre
fenetre.mainloop()


"""
Note d'ajout: 
- Dans makeReservation, faire en sorte d'ajouter la reservation à la table
- Faire en sorte de pouvoir ajouter plusieurs tables à une reservation (mergedTable)
- Faire une fonction qui check les réservations, places les tables dans les listes correspondantes et change l'état des Tables si l'heure des réservation correspond 
- enregistrer l'état des tables à la fin du programmes dans un fichier json ou dans une base de données
- charger les tables depuis un fichier json qui contient l'etat des tables pré-existantes ou charger les tables depuis une base de donnée
- ajouter setter et properties aux classes
- restructurer le code (le rendre plus lisibles, séparer les constantes, les imports, les getter/setter et les méthodes dans différentes sections pour chaque fichier)
"""
