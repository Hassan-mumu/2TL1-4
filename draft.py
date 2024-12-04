# ----------------------------------------------------------------IMPORTS-----------------------------------------------------------------------------#

# Assurer que l'interface est correctement initialisée avec des tables
from DatabaseManager import DatabaseManager
from tkinter import *
from Restaurant import *
from tkinter import ttk, NORMAL, DISABLED
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
selected_tables = []  # Liste pour stocker les tables sélectionnées

# ----------------------------------------------------------------CHARGEMENT DES DONNEES-----------------------------------------------------------------------------#

# Créer une instance de DatabaseManager
db_manager = DatabaseManager()

# Charger ou initialiser l'interface
interface = Restaurant(db_manager)

# Ajouter des tables si aucune n'existe
if not interface.all_table:
    for i in range(1, 21):
        if i <= 10:
            interface.addTable(Table(2))
        elif i <= 16:
            interface.addTable(Table(4))
        else:
            interface.addTable(Table(6))

# Exemple de sauvegarde à la fin du programme

# Créer la fenêtre principale
fenetre = Tk()
fenetre.geometry("1920x1080")
fenetre.title("La bonne fourchette")
fenetre.configure(background=DARK_CREAM_COLOR, pady=20)


# ----------------------------------------------------------------RESERVATIONS-----------------------------------------------------------------------------#
# Méthodes

def update_reservation(reservation: Reservation):
    interface.add_reservation(reservation)
    for table in reservation.table:
        table.add_reservation(reservation)


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


def afficher_details_reservation(cadre, reservation: Reservation):
    """Affiche les informations d'une table dans le cadre donné."""
    Label(cadre, text=f"Name : {reservation.name}", font=(
        POlICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Table(s) : {reservation.table}", font=(
        POlICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Date : {reservation.date_representation()}", font=(
        POlICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Hour : {reservation.hour_representation()}", font=(
        POlICE, 16), background="white").pack(anchor="w", padx=10)

    now = datetime.now()
    reservation_time = datetime.combine(reservation.res_date, reservation.res_hour)

    # Vérifie si le bouton doit être activé ou grisé
    button_state = NORMAL if now >= reservation_time - timedelta(minutes=10) else DISABLED

    # Ajouter un bouton "Occupée" avec l'état dynamique
    occupe_button = Button(
        cadre, text="Occupée", font=(POlICE, 14), background="lightcoral",
        state=button_state,  # État dynamique
        command=lambda res=reservation: set_table_occupee(res)  # Capture explicite de "reservation"
    )
    occupe_button.pack(pady=5, padx=10, anchor="w")

    # Planification pour réactiver le bouton automatiquement à l'approche de l'heure
    def verifier_et_rafraichir_bouton():
        now = datetime.now()
        if now >= reservation_time - timedelta(minutes=10):
            occupe_button.config(state=NORMAL)  # Activer le bouton
        else:
            occupe_button.after(1000, verifier_et_rafraichir_bouton)  # Vérifie à nouveau dans 1 seconde

    # Lancer la vérification dynamique
    verifier_et_rafraichir_bouton()

    # Ajouter un bouton "Annuler la réservation"
    Button(
        cadre, text="Annuler la réservation", font=(POlICE, 14), background="indianred",
        command=lambda: annuler_reservation(reservation)
    ).pack(pady=5, padx=10, anchor="w")


# ----------------------------------------------------------------TABLES-----------------------------------------------------------------------------#

'''
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
'''


def afficher_tables(liste_table):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    for table in liste_table:
        cadre_table = Frame(scrollable_frame, background="white",
                            pady=10, padx=10, relief="raised", borderwidth=2,
                            width=150, height=100)
        cadre_table.grid(pady=10, padx=10)

        # Forcer le style d'origine
        cadre_table.configure(background="white", relief="raised", borderwidth=2)

        Label(cadre_table, text=f"Table ID : {table.t_id}", font=("Arial", 12, "bold"), bg="white").pack(pady=2)
        Label(cadre_table, text=f"Places : {table.seat_nbr}", font=("Arial", 10), bg="white").pack(pady=2)
        Label(cadre_table,
              text=f"État : {'Occupée' if table.state == 'X' else 'Réservée' if table.state == 'R' else 'Disponible'}",
              font=("Arial", 10), bg="white").pack(pady=2)

        cadre_table.bind("<Button-1>", lambda event, ct=cadre_table, t=table: on_table_clicked(ct, t))


'''
def on_table_clicked(cadre_table, table):
    """
    Gère le clic sur une table et diagnostique les modifications de style.
    """
    print(f"Table {table.t_id} cliquée. État actuel : {table.state}")

    # Appliquer les options ou toute autre logique
    basculer_options_table(cadre_table, table)

    # Restauration du style
    cadre_table.configure(background="white", relief="raised", borderwidth=2)
    print(f"Table {table.t_id} : Style restauré.")

def rafraichir_apres_interaction():
    """
    Rafraîchit les informations et le style de toutes les tables après interaction.
    """
    afficher_tables(interface.all_table)  # Recharge les données et réinitialise les styles

'''


def afficher_tables(liste_table):
    """
    Affiche la liste des tables avec une grille, des informations (ID, places, état),
    et ajoute une boule colorée pour indiquer l'état :
    - Rouge : Occupée
    - Orange : Réservée
    - Vert : Disponible
    """
    # Configure le cadre défilable
    configurer_scrollable_frame()
    x, y = 0, 0

    # Nettoie les widgets existants dans le cadre défilable
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Affiche un message si aucune table n'est disponible
    if not liste_table:
        displayEmpty(scrollable_frame, EMPTY_TABLE)
    else:
        for table in liste_table:
            # Crée un cadre pour chaque table
            cadre_table = Frame(scrollable_frame, background="white",
                                pady=10, padx=10, relief="raised", borderwidth=2,
                                width=150, height=100)  # Dimensions fixes
            cadre_table.grid(pady=10, padx=10, column=x, row=y)

            # Empêche les dimensions de changer avec le contenu
            cadre_table.grid_propagate(False)

            # Ajout des détails de la table : ID, places et état
            Label(cadre_table, text=f"Table ID : {table.t_id}", font=("Arial", 12, "bold"),
                  bg="white").pack(pady=2)
            Label(cadre_table, text=f"Places : {table.seat_nbr}", font=("Arial", 10),
                  bg="white").pack(pady=2)
            Label(cadre_table,
                  text=f"État : {'Occupée' if table.state == 'X' else 'Réservée' if table.state == 'R' else 'Disponible'}",
                  font=("Arial", 10), bg="white").pack(pady=2)

            # Ajouter une boule colorée selon l'état de la table
            boule_couleur = {
                'X': 'red',  # Rouge pour Occupée
                'R': 'orange',  # Orange pour Réservée
                'V': 'green'  # Vert pour Disponible
            }
            boule_canvas = Canvas(cadre_table, width=20, height=20, bg="white", highlightthickness=0)
            boule_canvas.create_oval(2, 2, 18, 18, fill=boule_couleur.get(table.state, 'grey'))  # Boule sans contour
            boule_canvas.pack(pady=5)

            # Ajouter un événement ou un bouton interactif
            cadre_table.bind("<Button-1>", lambda event, ct=cadre_table, t=table: basculer_options_table(ct, t))

            # Organisation en grille (4 colonnes par ligne)
            if x == 3:  # 4 colonnes par ligne
                y += 1
            x = (x + 1) % 4


'''
def afficher_tables(liste_table):
    """
    Affiche la liste des tables avec une grille, des informations (ID, numéro, état)
    et conserve leur style initial après mise à jour.
    """
    # Configure le cadre défilable
    configurer_scrollable_frame()
    x, y = 0, 0

    # Nettoie les widgets existants dans le cadre défilable
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Affiche un message si aucune table n'est disponible
    if not liste_table:
        displayEmpty(scrollable_frame, EMPTY_TABLE)
    else:
        for table in liste_table:
            # Crée un cadre pour chaque table
            cadre_table = Frame(scrollable_frame, background="white",
                                pady=10, padx=10, relief="raised", borderwidth=2,
                                width=150, height=100)  # Dimensions fixes
            cadre_table.grid(pady=10, padx=10, column=x, row=y)

            # Empêche les dimensions de changer avec le contenu
            cadre_table.grid_propagate(False)

            # Ajout des détails de la table : ID, numéro et état
            Label(cadre_table, text=f"Table  : {table.t_id}", font=("Arial", 12, "bold"),
                  bg="white").pack(pady=2)
            Label(cadre_table, text=f"Places : {table.seat_nbr}", font=("Arial", 10),
                  bg="white").pack(pady=2)
            Label(cadre_table, text=f"État : {'Occupée' if table.state == 'X' else 'Réservée' if table.state == 'R' else 'Disponible'}",
                  font=("Arial", 10), bg="white").pack(pady=2)

            # Ajouter un événement ou un bouton interactif
            cadre_table.bind("<Button-1>", lambda event, ct=cadre_table, t=table: basculer_options_table(ct, t))

            # Organisation en grille (4 colonnes par ligne)
            if x == 3:  # 4 colonnes par ligne
                y += 1
            x = (x + 1) % 4
'''


def afficher_details_table(cadre, table: Table):
    """Affiche les informations d'une table dans le cadre donné."""
    Label(cadre, text=f"Table ID : {table.t_id}", font=(
        POlICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Places : {table.seat_nbr}", font=(
        POlICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"État : {table.state}", font=(
        POlICE, 16), background="white").pack(anchor="w", padx=10)


'''
def afficher_boutons_options(cadre, table: Table):
    """Affiche les boutons Réserver et Voir Réservations dans le cadre donné."""
    Button(
        cadre, text="Réserver", font=(POlICE, 14), background="lightgreen",
        command=lambda: reserver_table(table)
    ).pack(pady=5, padx=10, anchor="w")

    Button(
        cadre, text="Voir Réservations", font=(POlICE, 14), background="lightblue",
        command=lambda: afficher_reservations(table.reservations)
    ).pack(pady=5, padx=10, anchor="w")
'''


def afficher_boutons_options(cadre, table: Table):
    """Affiche les boutons Réserver, Voir Réservations et Libérer dans le cadre donné."""
    # Bouton Réserver
    Button(
        cadre, text="Réserver", font=(POlICE, 14), background="lightgreen",
        command=lambda: reserver_table(table)
    ).pack(side="left", pady=5, padx=10, anchor="w")

    # Bouton Voir Réservations
    Button(
        cadre, text="Voir Réservations", font=(POlICE, 14), background="lightblue",
        command=lambda: afficher_reservations(table.reservations)
    ).pack(side="left", pady=5, padx=10, anchor="w")

    # Bouton Libérer la table
    Button(
        cadre, text="Libérer", font=(POlICE, 14), background="indianred",
        command=lambda: liberer_table(table)
    ).pack(side="left", pady=5, padx=10, anchor="w")


def liberer_table(table: Table):
    """
    Change l'état de la table à 'V' (Disponible) et rafraîchit l'interface.
    """
    if table.state != 'V':  # Vérifie si la table n'est pas déjà disponible
        table.state = 'V'
        table.reservations.clear()  # Vide les réservations associées à la table
        print(f"Table {table.t_id} libérée avec succès.")

        # Met à jour l'affichage
        afficher_tables(interface.all_table)
        afficher_reservations(interface.reservations_list)
    else:
        print(f"La table {table.t_id} est déjà disponible.")


def basculer_options_table(cadre_table, table: Table):
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


def reload_table_states(self):
    """Recharge l'état des tables depuis la base de données."""
    self.__all_table = self.db_manager.load_tables()
    print("Les états des tables ont été rechargés.")


# ----------------------------------------------------------------RESERVER TABLE-----------------------------------------------------------------------------#

def reserver_table(table: Table):
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
    selected_date = datetime.strptime(cal.get_date(), "%m/%d/%y").date()
    selected_time = datetime.strptime(selected_time_var.get(), "%H:%M").time()
    nom_reservation = nom_var.get().strip() or "defaultName"

    reservation = Reservation(table, selected_time, selected_date, nom_reservation)
    update_reservation(reservation)
    if selected_time:
        afficher_confirmation(reservation)
    else:
        Label(scrollable_frame, text="Veuillez sélectionner une heure !",
              font=(POlICE, 14), background="red").pack(pady=10)


def afficher_confirmation(reservation: Reservation):
    """Affiche un message de confirmation et revient à l'écran des tables."""
    configurer_scrollable_frame()

    frame_reservation = Frame(scrollable_frame, background=LIGHT_CREAM_COLOR)
    frame_reservation.pack(pady=20)

    Label(
        frame_reservation,
        text=f"Réservation confirmée pour la Table {reservation.table}",
        font=(POlICE, 20, "bold"), background=LIGHT_CREAM_COLOR
    ).pack(pady=20)

    Label(
        frame_reservation,
        text=f"Date : {reservation.date_representation()}\nHeure : {reservation.hour_representation()}\nNom : {reservation.name}",
        font=(POlICE, 16), background=LIGHT_CREAM_COLOR
    ).pack(pady=10)

    Button(
        frame_reservation, text="Retour aux tables", font=(POlICE, 14),
        background="lightblue", command=lambda: afficher_tables(interface.all_table)
    ).pack(pady=20)


def afficher_reservations_type():
    configurer_scrollable_frame()

    Label(
        scrollable_frame, text="Choisissez un type de réservation : ", font=(POlICE, 26), background=LIGHT_CREAM_COLOR
    ).pack(pady=75, padx=100)

    button_frame = Frame(scrollable_frame, background=LIGHT_CREAM_COLOR)
    button_frame.pack(pady=20)

    Button(
        button_frame, text="Sur Place", width=BTN_SIZE_X, height=BTN_SIZE_Y, font=(POlICE, 22),
        background="lightblue", command=filter_liste
    ).pack(padx=10, side="left")

    Button(
        button_frame, text="Sur Reservation", width=BTN_SIZE_X, height=BTN_SIZE_Y, font=(POlICE, 22),
        background="lightblue", command=choisir_date_heure
    ).pack(side="right")


def choisir_date_heure():
    configurer_scrollable_frame()
    frame_principal = Frame(scrollable_frame, background=LIGHT_CREAM_COLOR)
    frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

    # Ajout du champ pour le nom
    nom_var = ajouter_champ_nom(frame_principal)

    # Section calendrier
    cal = ajouter_calendrier(frame_principal)

    # Section créneaux horaires
    selected_time_var = ajouter_choix_horaires(frame_principal)

    # Bouton de validation
    Button(
        scrollable_frame, text="Valider", font=(POlICE, 14),
        background="lightgreen", command=lambda: filter_liste((cal, selected_time_var, nom_var))
    ).pack(pady=20)


def filter_liste(reservation=None):
    reservation_hour = datetime.now().time()
    reservation_date = datetime.now().date()
    name = "defaultName"
    if reservation:
        reservation_hour = datetime.strptime(reservation[1].get(), "%H:%M").time()
        reservation_date = datetime.strptime(reservation[0].get_date(), "%m/%d/%y").date()
        name = reservation[2].get().strip() or name

    tables = interface.filterByDateTime(reservation_date, reservation_hour, interface.all_table)
    afficher_tables_selectionner(tables, reservation_hour, reservation_date, name)


def afficher_tables_selectionner(liste_table, hour, date, name):
    """Affiche la liste des tables avec une grille et une scrollbar."""
    configurer_scrollable_frame()
    x, y = 0, 0

    # Bouton pour confirmer la sélection
    Button(
        scrollable_frame, text="Confirmer la sélection", font=(POlICE, 12, "bold"),
        bg="green", fg="white", command=lambda: confirmer_selection(hour, date, name)
    ).grid(row=0, column=0, pady=10, padx=10, sticky="nw")

    if not liste_table:
        displayEmpty(scrollable_frame, EMPTY_TABLE)
    else:
        # Affichage des tables
        for table in liste_table:
            cadre_table = Frame(
                scrollable_frame, background="white", pady=10, padx=10,
                relief="raised", borderwidth=2,
            )
            cadre_table.grid(pady=10, padx=10, column=x, row=y + 1)  # Décaler à cause du bouton

            afficher_details_table(cadre_table, table)

            # Ajouter un bouton de sélection pour chaque table
            var = IntVar()
            Checkbutton(
                cadre_table, text="Sélectionner", variable=var, bg="white",
                command=lambda t=table, v=var: mettre_a_jour_selection(t, v)
            ).pack(pady=5)

            if x == 3:  # 4 colonnes par ligne
                y += 1
            x = (x + 1) % 4


def confirmer_selection(hour, date, name):
    reservation = Reservation(selected_tables.copy(), hour, date, name)
    update_reservation(reservation)
    afficher_confirmation(reservation)
    selected_tables.clear()


def mettre_a_jour_selection(table, var):
    """Met à jour la liste des tables sélectionnées."""
    if var.get():
        selected_tables.append(table)
    else:
        selected_tables.remove(table)


# --------------------------fonctions --> button ------------------------------------------------------------------------------------------------------------------
def set_table_occupee(reservation: Reservation):
    """
    Change l'état des tables associées à une réservation à 'X' (Occupée).
    """

    for table in reservation.table:
        table.state = 'X'  # Change l'état de la table
        print(f"Table {table.t_id} mise à jour comme occupée.")
    afficher_reservations(interface.reservations_list)
    afficher_tables(interface.all_table)


def annuler_reservation(reservation: Reservation):
    """Annule une réservation si elle est à plus d'une heure."""
    now = datetime.now()
    reservation_time = datetime.combine(reservation.res_date, reservation.res_hour)
    if reservation_time - now >= timedelta(hours=1):  # Plus d'une heure avant
        # Supprime la réservation de la liste principale
        interface.reservations_list.remove(reservation)

        # Supprime la réservation des tables associées
        # Met les tables associées à 'V'
        for table in reservation.table:
            table.state = 'V'  # Utilise le setter de la classe Table pour changer l'état
            table.remove_reservation(reservation)  # Retire la réservation de la table

        print(f"Réservation '{reservation.name}' annulée avec succès.")
        afficher_reservations(interface.reservations_list)  # Rafraîchit l'affichage
    else:
        # Notification que l'annulation est impossible
        messagebox.showwarning(
            "Annulation non autorisée",
            "L'annulation de cette réservation est refusée car elle est programmée dans moins d'une heure. Veuillez contacter le responsable si nécessaire."
        )


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


# ---------------------------------------nettoyage de la db----------------------------------------------------------------------------------------------


# Charger l'interface
interface = Restaurant(db_manager)


def nettoyer_reservations_periodiques():
    """Nettoie les réservations expirées toutes les 5 minutes."""
    db_manager.clean_expired_reservations()
    fenetre.after(300000, nettoyer_reservations_periodiques)  # 300000 ms = 5 minutes


# ----------------------------------------------------------------AFFICHAGE-----------------------------------------------------------------------------#


# Titre de la partie gauche
label_titre = Label(fenetre, text="La Bonne Fourchette", font=(
    POlICE, 34, "bold"), background=DARK_CREAM_COLOR, anchor="w")
# Ancrer en haut à gauche
label_titre.pack(pady=(10, 0), padx=(50, 0), anchor="nw")

# Créer une frame pour la partie gauche (40% de la largeur)
frame_gauche = Frame(fenetre, width=0.35 * 1920, background=LIGHT_CREAM_COLOR)
frame_gauche.pack(side="left", fill="y", padx=10)
frame_gauche.pack_propagate(False)  # Fixer la taille

# Créer la frame des boutons à l'intérieur de frame_gauche
frame_boutons = Frame(frame_gauche, background=LIGHT_CREAM_COLOR)
frame_boutons.pack(pady=20, padx=20, fill="y")

# Ligne de séparation
ligne_separation = Frame(fenetre, width=5, background="white")
ligne_separation.pack(side="left", fill="y")

# Créer la zone d'affichage sur la droite (60% de la largeur)
frame_droite = Frame(fenetre, width=0.50 * 1920, background=LIGHT_CREAM_COLOR)
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
Button(
    frame_boutons, text="Afficher les Tables", font=(POlICE, 18), height=BTN_SIZE_Y, width=BTN_SIZE_X,
    background=RED_COLOR,
    command=lambda: afficher_tables(interface.all_table)
).grid(pady=20, padx=10, row=0, column=0)

# bouton pour afficher les réservations
Button(
    frame_boutons, text="Afficher les Reservations", font=(POlICE, 18), height=BTN_SIZE_Y, width=BTN_SIZE_X,
    background=RED_COLOR,
    command=lambda: afficher_reservations(interface.reservations_list)
).grid(pady=20, padx=10, row=0, column=1)

Button(
    frame_boutons, text="Afficher Notifications", font=(POlICE, 18), height=BTN_SIZE_Y, width=BTN_SIZE_X,
    background="lightcoral", command=afficher_notifications_recues
).grid(pady=20, padx=10, row=1, column=0)

Button(
    frame_boutons, text="Créer Une Reservation", font=(POlICE, 18), height=BTN_SIZE_Y, width=BTN_SIZE_X,
    background="lightcoral", command=afficher_reservations_type
).grid(pady=20, padx=10, row=1, column=1)

# ----------------------------------------------------------------LANCEMENT DU PROGRAMME-----------------------------------------------------------------------------#
# Lancer la boucle principale de la fenêtre
verifier_et_notifier()
fenetre.mainloop()
interface.save_data()
nettoyer_reservations_periodiques()
# Nettoyer les réservations expirées au démarrage
db_manager.clean_expired_reservations()

print("Données sauvegardées avec succès.")

"""
Note d'ajout:
- La selection des tables ne doit pas etre confirmer tant que le nombre de personnes pour une reservation n'est pas inferieur ou égal au nombre de places 
- Faire une fonction qui check les réservations, places les tables dans les listes correspondantes et change l'état des Tables si l'heure des réservation correspond 
- restructurer le code (le rendre plus lisibles, séparer les constantes, les imports, les getter/setter et les méthodes dans différentes sections pour chaque fichier)
- faire la gestion des erreurs avec exception
- ajouter le linter
"""

#-----------------------------
def charger_logo():
    """Charge le logo du fichier et le redimensionne."""
    try:
        image = Image.open("logo.png")  # Remplacez par le nom correct de votre logo
        image = image.resize((100, 100), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Erreur lors du chargement du logo : {e}")
        return None

# Couleurs pour le design
BACKGROUND_COLOR = '#2f2b2d'  # Marron foncé
TITLE_COLOR = "#F5F5DC"  # Doré


# Créer le header (logo + titre)
header_frame = Frame(fenetre, bg=BACKGROUND_COLOR)
header_frame.pack(fill="x", pady=20)

# Charger et afficher le logo
logo_image = charger_logo()
if logo_image:
    logo_label = Label(header_frame, image=logo_image, bg=BACKGROUND_COLOR)
    logo_label.pack(side="left", padx=10)

# Ajouter le titre doré
label_titre = Label(
    header_frame,
    text="La Bonne Fourchette",
    font=("Garamond", 34, "bold"),
    bg=BACKGROUND_COLOR,
    fg=TITLE_COLOR,  # Couleur dorée
    anchor="w"
)
label_titre.pack(side="left", padx=10)

# Cadre pour les boutons sur la gauche
frame_gauche = Frame(fenetre, bg=BACKGROUND_COLOR)
frame_gauche.pack(side="left", fill="y", padx=50, pady=50)

# Boutons dans le cadre gauche
Button(
    frame_gauche, text="Afficher les Tables", font=("Garamond", 18), height=3, width=20,
    background="indianred",
).pack(pady=10)

Button(
    frame_gauche, text="Afficher les Reservations", font=("Garamond", 18), height=3, width=20,
    background="indianred",
).pack(pady=10)

Button(
    frame_gauche, text="Afficher Notifications", font=("Garamond", 18), height=3, width=20,
    background="lightcoral",
).pack(pady=10)

Button(
    frame_gauche, text="Créer Une Reservation", font=("Garamond", 18), height=3, width=20,
    background="lightcoral",
).pack(pady=10)
----------