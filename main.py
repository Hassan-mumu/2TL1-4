
# ----------------------------------------------------------------IMPORTS-----------------------------------------------------------------------------#

# Assurer que l'interface est correctement initialisée avec des tables
from Restaurant import *
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta

# ----------------------------------------------------------------NOTIFICATION-----------------------------------------------------------------------------#

RED_COLOR = "indianred"
DARK_CREAM_COLOR = "#FAF0E6"
LIGHT_CREAM_COLOR = "#FFFAF0"
POlICE = "Garamond"
BTN_SIZE_X = 20
BTN_SIZE_Y = 10
EMPTY_TABLE = "Pas de table disponible."
EMPTY_RESERVATION = "Pas de réservations"

# ----------------------------------------------------------------CHARGEMENT DES DONNEES-----------------------------------------------------------------------------#

interface = Restaurant()

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

selected_date = None
selected_time = None

# ----------------------------------------------------------------RESERVATIONS-----------------------------------------------------------------------------#
# Méthodes


def afficher_reservations(liste_reservation):
    """Affiche la liste des réservations avec une grille et une scrollbar."""
    configurer_scrollable_frame()
    x, y = 0, 0

    if liste_reservation == []:
        displayEmpty(scrollable_frame, EMPTY_RESERVATION)
    else:
        for reservation in liste_reservation:
            cadre_reservation = Frame(
                scrollable_frame, background="white", pady=10, padx=10, relief="raised", borderwidth=2)
            cadre_reservation.grid(pady=10, padx=10, column=x, row=y)

            afficher_details_reservation(cadre_reservation, reservation)

            if x == 3:  # 4 colonnes par ligne
                y += 1
            x = (x + 1) % 4


def afficher_details_reservation(cadre, reservation):
    """Affiche les informations d'une table dans le cadre donné."""
    Label(cadre, text=f"Name : {reservation.getName()}", font=(
        POlICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Table(s) : {reservation.getTable()}", font=(
        POlICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Date : {reservation.getDate()}", font=(
        POlICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Hour : {reservation.getHour()}", font=(
        POlICE, 16), background="white").pack(anchor="w", padx=10)

# ----------------------------------------------------------------TABLES-----------------------------------------------------------------------------#


def afficher_tables(liste_table):
    """Affiche la liste des tables avec une grille et une scrollbar."""
    configurer_scrollable_frame()
    x, y = 0, 0

    if liste_table == []:
        displayEmpty(scrollable_frame, EMPTY_TABLE)
    else:
        for table in liste_table:
            cadre_table = Frame(scrollable_frame, background="white",
                                pady=10, padx=10, relief="raised", borderwidth=2)
            cadre_table.grid(pady=10, padx=10, column=x, row=y)

            afficher_details_table(cadre_table, table)

            cadre_table.bind("<Button-1>", lambda event, ct=cadre_table,
                             t=table: basculer_options_table(ct, t))

            if x == 3:  # 4 colonnes par ligne
                y += 1
            x = (x + 1) % 4


def afficher_details_table(cadre, table):
    """Affiche les informations d'une table dans le cadre donné."""
    Label(cadre, text=f"Table ID : {table.getId()}", font=(
        POlICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Places : {table.getSeat_nbr()}", font=(
        POlICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"État : {table.getState()}", font=(
        POlICE, 16), background="white").pack(anchor="w", padx=10)


def afficher_boutons_options(cadre, table: Table):
    """Affiche les boutons Réserver et Voir Réservations dans le cadre donné."""
    Button(
        cadre, text="Réserver", font=(POlICE, 14), background="lightgreen",
        command=lambda: reserver_table(table)
    ).pack(pady=5, padx=10, anchor="w")

    Button(
        cadre, text="Voir Réservations", font=(POlICE, 14), background="lightblue",
        command=lambda: afficher_reservations(table.getReservations())
    ).pack(pady=5, padx=10, anchor="w")


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

# ----------------------------------------------------------------RESERVER TABLE-----------------------------------------------------------------------------#


def reserver_table(table):
    """Affiche un écran pour sélectionner la date, l'heure et le nom de réservation."""
    configurer_scrollable_frame()

    # Ajout du champ pour le nom
    nom_var = ajouter_champ_nom(scrollable_frame)

    # Conteneur principal pour le calendrier et les créneaux horaires
    frame_principal = Frame(scrollable_frame, background=LIGHT_CREAM_COLOR)
    frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

    # Section calendrier
    cal = ajouter_calendrier(frame_principal)

    # Section créneaux horaires
    selected_time_var = ajouter_choix_horaires(frame_principal)

    # Bouton de validation
    Button(
        scrollable_frame, text="Valider", font=(POlICE, 14),
        background="lightgreen", command=lambda: valider_reservation(table, cal, selected_time_var, nom_var)
    ).pack(pady=20)


def ajouter_champ_nom(parent):
    """Ajoute un champ pour le nom de réservation."""
    frame_nom = Frame(parent, background=LIGHT_CREAM_COLOR)
    frame_nom.pack(fill="x", pady=10)
    Label(frame_nom, text="Nom de la réservation :", font=(POlICE, 16),
          background=LIGHT_CREAM_COLOR).pack(side="left", padx=10)

    nom_var = StringVar()
    Entry(frame_nom, textvariable=nom_var, font=(
        POlICE, 16), width=20).pack(side="left", padx=10)
    return nom_var


def ajouter_calendrier(parent):
    """Ajoute un calendrier pour choisir une date."""
    frame_cal = Frame(parent, background=LIGHT_CREAM_COLOR)
    frame_cal.pack(side="left", fill="y", padx=40)

    Label(frame_cal, text="Choisissez une date :", font=(
        POlICE, 16), background=LIGHT_CREAM_COLOR).pack(pady=10)
    cal = Calendar(frame_cal, selectmode="day", mindate=datetime.now(),
                   maxdate=datetime.now() + timedelta(days=60))
    cal.pack()
    return cal


def ajouter_choix_horaires(parent):
    """Ajoute les créneaux horaires matin et soir avec des boutons radio en grille."""
    frame_heures = Frame(parent, background=LIGHT_CREAM_COLOR)
    frame_heures.pack(side="right", fill="both", padx=20)

    Label(frame_heures, text="Choisissez une heure :", font=(
        POlICE, 16), background=LIGHT_CREAM_COLOR).pack(pady=10)

    time_slots = generate_time_slots()
    selected_time_var = StringVar(value="")

    for label, slots in time_slots.items():
        Label(frame_heures, text=label, font=(POlICE, 14, "bold"),
              background=LIGHT_CREAM_COLOR).pack(pady=5)

        slot_frame = Frame(frame_heures, background=LIGHT_CREAM_COLOR)
        slot_frame.pack(pady=5, fill="x")

        # Afficher les créneaux horaires dans une grille
        max_columns = 4  # Nombre maximal de colonnes par ligne
        for index, slot in enumerate(slots):
            row, col = divmod(index, max_columns)
            ttk.Radiobutton(
                slot_frame,
                text=slot,
                variable=selected_time_var,
                value=slot
            ).grid(row=row, column=col, padx=5, pady=5, sticky="w")

    return selected_time_var


def generate_time_slots():
    """Génère des créneaux horaires matin et soir."""
    def slots(start, end):
        while start <= end:
            yield start.strftime("%H:%M")
            start += timedelta(minutes=30)

    return {
        "Matin :": list(slots(datetime.strptime("10:00", "%H:%M"), datetime.strptime("13:30", "%H:%M"))),
        "Soir :": list(slots(datetime.strptime("18:00", "%H:%M"), datetime.strptime("21:30", "%H:%M"))),
    }


def valider_reservation(table: Table, cal, selected_time_var, nom_var):
    """Valide la réservation et affiche une confirmation."""
    selected_date = cal.get_date()
    selected_time = selected_time_var.get()
    nom_reservation = nom_var.get().strip() or "defaultName"
    r = Reservation(table, datetime.strptime(selected_time, "%H:%M").time(
    ), datetime.strptime(selected_date, "%m/%d/%y").date(), nom_reservation)
    interface.add_reservation(r)
    table.addReservation(r)
    if selected_time:
        afficher_confirmation(table, selected_date,
                              selected_time, nom_reservation)
    else:
        Label(scrollable_frame, text="Veuillez sélectionner une heure !",
              font=(POlICE, 14), background="red").pack(pady=10)


def afficher_confirmation(table, date, heure, nom):
    """Affiche un message de confirmation et revient à l'écran des tables."""
    configurer_scrollable_frame()

    Label(
        scrollable_frame,
        text=f"Réservation confirmée pour la Table {table.getId()}",
        font=(POlICE, 20, "bold"), background=LIGHT_CREAM_COLOR
    ).pack(pady=20)

    Label(
        scrollable_frame,
        text=f"Date : {date}\nHeure : {heure}\nNom : {nom}",
        font=(POlICE, 16), background=LIGHT_CREAM_COLOR
    ).pack(pady=10)

    Button(
        scrollable_frame, text="Retour aux tables", font=(POlICE, 14),
        background="lightblue", command=lambda: afficher_tables(interface.all_table)
    ).pack(pady=20)

# --------------------------------------------------------------------AFFICHAGE FRAME DROIT---------------------------------------------------------------------------#


def configurer_scrollable_frame():
    """Configure le canvas et le frame scrollable de la frame de droite."""
    global canvas, scrollbar, scrollable_frame
    for widget in frame_droite.winfo_children():
        widget.destroy()

    canvas = Canvas(frame_droite, background=LIGHT_CREAM_COLOR)
    scrollbar = Scrollbar(frame_droite, orient="vertical",
                          command=canvas.yview)
    scrollable_frame = Frame(canvas, background=LIGHT_CREAM_COLOR)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


def displayEmpty(parent_frame, message):
    """Affiche un message indiquant qu'il n'y a pas de données à afficher."""
    Label(parent_frame, text=message, font=(POlICE, 20), background=LIGHT_CREAM_COLOR, justify="center"
          ).pack(pady=20, padx=20, anchor="center")

# ----------------------------------------------------------------NOTIFICATIONS-----------------------------------------------------------------------------#


def verifier_et_notifier():
    """Vérifie les tables et affiche des notifications si nécessaire."""
    interface.check_table_status()
    fenetre.after(60000, verifier_et_notifier)


def afficher_notifications_recues():
    """Affiche les notifications reçues dans la dernière heure."""
    interface.clean_old_notifications()  # Nettoie les anciennes notifications
    configurer_scrollable_frame()
    if not interface.notifications:
        displayEmpty(scrollable_frame, "Aucune notification récente.")
    else:
        for timestamp, message in interface.notifications:
            Label(scrollable_frame, text=f"{timestamp.strftime('%H:%M:%S')} - {message}", font=(
                POlICE, 14), background="white", justify="left").pack(anchor="w", pady=5, padx=10)

# ----------------------------------------------------------------AFFICHAGE-----------------------------------------------------------------------------#


# Titre de la partie gauche
label_titre = Label(fenetre, text="La Bonne Fourchette", font=(
    POlICE, 34, "bold"), background=DARK_CREAM_COLOR, anchor="w")
# Ancrer en haut à gauche
label_titre.pack(pady=(10, 0), padx=(50, 0), anchor="nw")

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
frame_droite = Frame(fenetre, width=0.50*1920, background=LIGHT_CREAM_COLOR)
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
zone_affichage = Label(frame_droite, text="", font=(
    "Garamond", 20), background="#FFF5EE", justify="center")
zone_affichage.pack(pady=20, padx=20, anchor="center")

# ----------------------------------------------------------------BOUTONS-----------------------------------------------------------------------------#
# bouton pour afficher les tables
bouton = Button(
    frame_boutons, text="Afficher les Tables", font=(POlICE, 18),  height=BTN_SIZE_Y, width=BTN_SIZE_X, background=RED_COLOR,
    command=lambda: afficher_tables(interface.all_table)
)
bouton.grid(pady=20, padx=10, row=0, column=0)

# bouton pour afficher les réservations
bouton = Button(
    frame_boutons, text="Afficher les Reservations", font=(POlICE, 18), height=BTN_SIZE_Y, width=BTN_SIZE_X, background=RED_COLOR,
    command=lambda: afficher_reservations(interface.reservations_list)
)
bouton.grid(pady=20, padx=10, row=0, column=1)

button = Button(
    frame_boutons, text="Afficher Notifications", font=(POlICE, 18), height=BTN_SIZE_Y, width=BTN_SIZE_X, background="lightcoral", command=afficher_notifications_recues
)
button.grid(pady=20, padx=10, row=1, column=0)

# ----------------------------------------------------------------LANCEMENT DU PROGRAMME-----------------------------------------------------------------------------#
# Lancer la boucle principale de la fenêtre
verifier_et_notifier()
fenetre.mainloop()

"""
Note d'ajout: 
- Faire en sorte de pouvoir ajouter plusieurs tables à une reservation (mergedTable)
- Faire une fonction qui check les réservations, places les tables dans les listes correspondantes et change l'état des Tables si l'heure des réservation correspond 
- enregistrer l'état des tables à la fin du programmes dans un fichier json ou dans une base de données
- charger les tables depuis un fichier json qui contient l'etat des tables pré-existantes ou charger les tables depuis une base de donnée
- ajouter setter et properties aux classes
- restructurer le code (le rendre plus lisibles, séparer les constantes, les imports, les getter/setter et les méthodes dans différentes sections pour chaque fichier)
- faire la gestion des erreurs avec exception
- ajouter le linter
"""
