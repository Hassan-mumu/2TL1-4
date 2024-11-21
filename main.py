# Importer les classes nécessaires
from Interface import *  # Assurer que l'interface est correctement initialisée avec des tables
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta


#Constantes
RED_COLOR = "indianred"
DARK_CREAM_COLOR = "#FAF0E6"
LIGHT_CREAM_COLOR = "#FFFAF0"
POlICE = "Garamond"
BTN_SIZE_X = 20
BTN_SIZE_Y = 10
EMPTY_TABLE = "Pas de table disponible."
EMPTY_RESERVATION = "Pas de réservations"


# test init
interface = Interface()

for i in range(1, 21):
    if i <= 10:
        interface.addTable(Table(2))
    elif i <= 16:
        interface.addTable(Table(4))
    else:
        interface.addTable(Table(6))

# Créer la fenêtre principale
fenetre = Tk()
fenetre.geometry("1920x1080")
fenetre.title("La bonne fourchette")
fenetre.configure(background=DARK_CREAM_COLOR, pady=20)

# Méthodes

selected_date = None
selected_time = None

def reserver_table(table : Table):
    """Affiche un écran pour sélectionner la date et l'heure de réservation."""
    configurer_scrollable_frame()

    Label(
        scrollable_frame,
        text=f"Réserver pour la Table {table.getId()}",
        font=(POlICE, 20, "bold"),
        background=LIGHT_CREAM_COLOR
    ).pack(pady=20)

    # Sélection de la date
    Label(scrollable_frame, text="Choisissez une date :", font=(POlICE, 16), background=LIGHT_CREAM_COLOR).pack(pady=10)
    cal = Calendar(scrollable_frame, selectmode="day", mindate=datetime.now(), maxdate=datetime.now() + timedelta(days=60))
    cal.pack(pady=10)

    # Sélection des heures
    Label(scrollable_frame, text="Choisissez une heure :", font=(POlICE, 16), background=LIGHT_CREAM_COLOR).pack(pady=10)
    frame_heures = Frame(scrollable_frame, background=LIGHT_CREAM_COLOR)
    frame_heures.pack()

    time_slots = generate_time_slots()
    selected_time_var = StringVar(value="")  # Variable pour suivre le créneau sélectionné
    for slot in time_slots:
        ttk.Radiobutton(
            frame_heures,
            text=slot,
            variable=selected_time_var,
            value=slot,
            style="TRadiobutton"
        ).pack(side="left", padx=5, pady=5)

    # Bouton de validation
    def valider_reservation():
        global selected_date, selected_time
        selected_date = cal.get_date()  # Récupérer la date sélectionnée
        selected_time = selected_time_var.get()  # Récupérer l'heure sélectionnée
        reservation = Reservation(table,selected_time,selected_date)
        table.addReservation(reservation)
        interface._reservations_list.append(reservation)
        if selected_time:
            afficher_confirmation(table, selected_date, selected_time)
        else:
            Label(scrollable_frame, text="Veuillez sélectionner une heure !", font=(POlICE, 14), background="red").pack(pady=10)

    Button(
        scrollable_frame, text="Valider",
        font=(POlICE, 14), background="lightgreen", command=valider_reservation
    ).pack(pady=20)

def generate_time_slots():
    """Génère des créneaux horaires valides (10h-13h30 et 18h-21h30)."""
    slots = []
    morning_start = datetime.strptime("10:00", "%H:%M")
    morning_end = datetime.strptime("13:30", "%H:%M")
    evening_start = datetime.strptime("18:00", "%H:%M")
    evening_end = datetime.strptime("21:30", "%H:%M")
    
    while morning_start <= morning_end:
        slots.append(morning_start.strftime("%H:%M"))
        morning_start += timedelta(minutes=30)

    while evening_start <= evening_end:
        slots.append(evening_start.strftime("%H:%M"))
        evening_start += timedelta(minutes=30)
    
    return slots

def afficher_confirmation(table, date, heure):
    """Affiche un message de confirmation et revient à l'écran des tables."""
    configurer_scrollable_frame()

    Label(
        scrollable_frame,
        text=f"Réservation confirmée pour la Table {table.getId()}",
        font=(POlICE, 20, "bold"),
        background=LIGHT_CREAM_COLOR
    ).pack(pady=20)

    Label(
        scrollable_frame,
        text=f"Date : {date}\nHeure : {heure}",
        font=(POlICE, 16),
        background=LIGHT_CREAM_COLOR
    ).pack(pady=10)

    Button(
        scrollable_frame, text="Retour aux tables",
        font=(POlICE, 14), background="lightblue",
        command=lambda: afficher_tables(interface._all_table)
    ).pack(pady=20)


def configurer_scrollable_frame():
    """Configure le canvas et le frame scrollable de la frame de droite."""
    global canvas, scrollbar, scrollable_frame
    for widget in frame_droite.winfo_children():
        widget.destroy()

    canvas = Canvas(frame_droite, background=LIGHT_CREAM_COLOR)
    scrollbar = Scrollbar(frame_droite, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, background=LIGHT_CREAM_COLOR)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


def afficher_details_table(cadre, table):
    """Affiche les informations d'une table dans le cadre donné."""
    Label(cadre, text=f"Table ID : {table.getId()}", font=(POlICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Places : {table.getSeat_nbr()}", font=(POlICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"État : {table.getState()}", font=(POlICE, 16), background="white").pack(anchor="w", padx=10)

def afficher_details_reservation(cadre, reservation):
    """Affiche les informations d'une table dans le cadre donné."""
    Label(cadre, text=f"Name : {reservation.getName()}", font=(POlICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Table(s) : {reservation.getTable()}", font=(POlICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Date : {reservation.getDate()}", font=(POlICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Hour : {reservation.getHour()}", font=(POlICE, 16), background="white").pack(anchor="w", padx=10)

def afficher_boutons_options(cadre, table : Table):
    """Affiche les boutons Réserver et Voir Réservations dans le cadre donné."""
    Button(
        cadre, text="Réserver", font=(POlICE, 14), background="lightgreen",
        command=lambda: reserver_table(table)
    ).pack(pady=5, padx=10, anchor="w")

    Button(
        cadre, text="Voir Réservations", font=(POlICE, 14), background="lightblue",
        command=lambda: afficher_reservations(table.getReservations())
    ).pack(pady=5, padx=10, anchor="w")


def afficher_tables(liste_table):
    """Affiche la liste des tables avec une grille et une scrollbar."""
    configurer_scrollable_frame()
    x, y = 0, 0

    if liste_table == []:
        displayEmpty(scrollable_frame, EMPTY_TABLE )
    else:
        for table in liste_table:
            cadre_table = Frame(scrollable_frame, background="white", pady=10, padx=10, relief="raised", borderwidth=2)
            cadre_table.grid(pady=10, padx=10, column=x, row=y)

            afficher_details_table(cadre_table, table)

            cadre_table.bind("<Button-1>", lambda event, ct=cadre_table, t=table: basculer_options_table(ct, t))
            
            if x == 3:  # 4 colonnes par ligne
                y += 1
            x = (x + 1) % 4


def afficher_reservations(liste_reservation):
    """Affiche la liste des réservations avec une grille et une scrollbar."""
    configurer_scrollable_frame()
    x, y = 0, 0

    if liste_reservation == []:
        displayEmpty(scrollable_frame, EMPTY_RESERVATION )
    else:
        for reservation in liste_reservation:
            cadre_reservation = Frame(scrollable_frame, background="white", pady=10, padx=10, relief="raised", borderwidth=2)
            cadre_reservation.grid(pady=10, padx=10, column=x, row=y)

            afficher_details_reservation(cadre_reservation, reservation)
            
            if x == 3:  # 4 colonnes par ligne
                y += 1
            x = (x + 1) % 4


def basculer_options_table(cadre_table, table):
    """Affiche ou masque les options d'une table dans son cadre."""
    if any(isinstance(widget, Button) for widget in cadre_table.winfo_children()):
        # Si les options sont présentes, réaffiche seulement les détails
        for widget in cadre_table.winfo_children():
            widget.destroy()
        afficher_details_table(cadre_table, table)
    else:
        # Sinon, affiche les options
        for widget in cadre_table.winfo_children():
            widget.destroy()
        afficher_details_table(cadre_table, table)
        afficher_boutons_options(cadre_table, table)

def displayEmpty(parent_frame, message):
    """Affiche un message indiquant qu'il n'y a pas de données à afficher."""
    Label(
        parent_frame,
        text=message,
        font=(POlICE, 20),
        background=LIGHT_CREAM_COLOR,
        justify="center"
    ).pack(pady=20, padx=20, anchor="center")

# Titre de la partie gauche
label_titre = Label(fenetre, text="La Bonne Fourchette", font=(POlICE, 34, "bold"), background=DARK_CREAM_COLOR, anchor="w")
label_titre.pack(pady=(10, 0), padx=(50, 0), anchor="nw")  # Ancrer en haut à gauche

# Créer une frame pour la partie gauche (40% de la largeur)
frame_gauche = Frame(fenetre, width=0.35*1920, background=LIGHT_CREAM_COLOR)
frame_gauche.pack(side="left", fill="y", padx=10)
frame_gauche.pack_propagate(False)  # Fixer la taille


# Créer la frame des boutons à l'intérieur de frame_gauche
frame_boutons = Frame(frame_gauche, background=LIGHT_CREAM_COLOR)
frame_boutons.pack(pady=20, padx=20, fill="y")

# Ligne de séparation
ligne_separation = Frame(fenetre, width=5, background="white")
ligne_separation.pack(side="left", fill="y")

# Créer la zone d'affichage sur la droite (60% de la largeur)
frame_droite = Frame(fenetre, width=0.55*1920, background=LIGHT_CREAM_COLOR)
frame_droite.pack(side="left", fill="both", padx=50, expand=True)
frame_droite.pack_propagate(False)  # Fixer la taille

canvas = Canvas(frame_droite, background=LIGHT_CREAM_COLOR)
scrollbar = Scrollbar(frame_droite, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas, background=LIGHT_CREAM_COLOR)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Placer le canvas et la scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Zone de texte affichant le message
zone_affichage = Label(frame_droite, text="", font=("Garamond", 20), background="#FFF5EE", justify="center")
zone_affichage.pack(pady=20, padx=20, anchor="center")


# bouton pour afficher les tables
bouton = Button(
    frame_boutons, text="Afficher les Tables", font=(POlICE, 18),  height=BTN_SIZE_Y, width=BTN_SIZE_X, background=RED_COLOR,
    command= lambda : afficher_tables(interface._all_table)
)
bouton.grid(pady=20, padx=10, row=0, column=0)

# bouton pour afficher les réservations
bouton = Button(
    frame_boutons, text="Afficher les Reservations", font=(POlICE, 18) , height=BTN_SIZE_Y, width=BTN_SIZE_X, background=RED_COLOR,
    command=lambda : afficher_reservations(interface._reservations_list)
)
bouton.grid(pady=20, padx=10, row=0, column=1)


# Lancer la boucle principale de la fenêtre
fenetre.mainloop()

"""
Note d'ajout: 
- Faire en sorte de pouvoir ajouter plusieurs tables à une reservation (mergedTable)
- Faire une fonction qui check les réservations, places les tables dans les listes correspondantes et change l'état des Tables si l'heure des réservation correspond 
- enregistrer l'état des tables à la fin du programmes dans un fichier json ou dans une base de données
- charger les tables depuis un fichier json qui contient l'etat des tables pré-existantes ou charger les tables depuis une base de donnée
- ajouter setter et properties aux classes
- restructurer le code (le rendre plus lisibles, séparer les constantes, les imports, les getter/setter et les méthodes dans différentes sections pour chaque fichier)
"""
