import tkinter as tk

RED_COLOR = "indianred"
DARK_CREAM_COLOR = "#FAF0E6"
LIGHT_CREAM_COLOR = "#FFFAF0"
POlICE = "Garamond"


# Créer la fenêtre principale
fenetre = tk.Tk()
fenetre.geometry("1920x1080")
fenetre.title("La bonne fourchette")
fenetre.configure(background=DARK_CREAM_COLOR, pady=20)

# Fonction de commande du bouton
def afficher_message(message):
    # Exemple d'affichage dans la zone de droite
    zone_affichage.config(text=message)

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

# Ajouter les boutons dans frame_boutons
for i in range(4):
    bouton = tk.Button(
        frame_boutons, text=f"Bouton {i+1}", font=(POlICE, 18), width=20, background=RED_COLOR,
        command=lambda i=i: afficher_message(f"Vous avez cliqué sur le bouton {i+1}")
    )
    bouton.pack(pady=20, padx=10, fill="x")

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

# Lancer la boucle principale de la fenêtre
fenetre.mainloop()