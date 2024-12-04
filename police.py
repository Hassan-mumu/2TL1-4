from tkinter import Tk, Listbox, Scrollbar, RIGHT, Y, Frame, Label
import tkinter.font as tkFont

def afficher_style_police(event):
    """Affiche un exemple de la police sélectionnée."""
    selection = liste.get(liste.curselection())  # Récupère la police sélectionnée
    label_exemple.config(
        text=f"Exemple avec {selection}",
        font=(selection, 20)
    )

# Créer la fenêtre principale
fenetre = Tk()
fenetre.geometry("600x400")
fenetre.title("Prévisualisation des Polices")

# Frame pour organiser la disposition
frame_principal = Frame(fenetre)
frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

# Ajouter une liste déroulante avec une barre de défilement
scrollbar = Scrollbar(frame_principal)
scrollbar.pack(side=RIGHT, fill=Y)

liste = Listbox(frame_principal, yscrollcommand=scrollbar.set, font=("Arial", 12), width=30, height=15)
liste.pack(side="left", fill="both", expand=True)

# Ajouter une zone pour afficher le style
label_exemple = Label(frame_principal, text="Sélectionnez une police", font=("Arial", 16), wraplength=300)
label_exemple.pack(side="right", padx=20, pady=20)

# Obtenir et afficher toutes les polices
polices = tkFont.families()
for police in sorted(polices):
    liste.insert("end", police)

# Connecter l'événement de sélection à la fonction d'affichage
liste.bind("<<ListboxSelect>>", afficher_style_police)

# Configurer la barre de défilement
scrollbar.config(command=liste.yview)

fenetre.mainloop()
