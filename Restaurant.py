from tkinter import messagebox
from Reservation import Reservation
from Table import Table
from datetime import *
import re


class Restaurant:
    def __init__(self, db_manager, *tables):
        self.db_manager = db_manager  # Instance de DatabaseManager
        self.__all_table = self.db_manager.load_tables()
        self.__available_table = [t for t in self.__all_table if t.state == 'V']
        self.__occupied_table = [t for t in self.__all_table if t.state == 'X']
        self.__reservations_list = self.db_manager.load_reservations(self.__all_table)
        self.__password = 0000
        self.__baby_chairs_total = 8
        self.__baby_chairs_available = 8
        self.__notifications = []

    # Getters et setters avec décorateurs

    @property
    def all_table(self):
        return self.__all_table

    @all_table.setter
    def all_table(self, tables):
        self.__all_table = tables

    @property
    def available_table(self):
        return self.__available_table

    @available_table.setter
    def available_table(self, tables):
        self.__available_table = tables

    @property
    def occupied_table(self):
        return self.__occupied_table

    @occupied_table.setter
    def occupied_table(self, tables):
        self.__occupied_table = tables

    @property
    def reservations_list(self):
        return self.__reservations_list

    @reservations_list.setter
    def reservations_list(self, reservations):
        self.__reservations_list = reservations

    def add_reservation(self, reservation):
        self.__reservations_list.append(reservation)

    @property
    def baby_chairs_available(self):
        return self.__baby_chairs_available

    @baby_chairs_available.setter
    def baby_chairs_available(self, count):
        self.__baby_chairs_available = count

    @property
    def baby_chairs_total(self):
        return self.__baby_chairs_total

    @baby_chairs_total.setter
    def baby_chairs_total(self, count):
        self.__baby_chairs_total = count

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password
        
    @property
    def notifications(self):
        return self.__notifications

    @password.setter
    def password(self, notifications):
        self.__notifications = notifications


    # Sauvegarder les données
    def save_data(self):
        self.db_manager.save_tables(self.__all_table)
        self.db_manager.save_reservations(self.__reservations_list)

    # Méthodes liées aux tables
    def addTable(self, table):
        """
        Ajoute des tables à la liste des tables disponibles si leur état est 'V' (Disponible).

        PRE : table est un objet de type 'Table'
        POST : Ajoute la table aux listes 'all_table' et 'available_table' si son état est 'V'.
        """
        if isinstance(table, Table):
            table = [table]
        for tab in table:
            if tab.state == 'V':
                self.__available_table.append(tab)
                self.__all_table.append(tab)

    def filterByDateTime(self, res_date, res_heure, table_list):
        """
        Filtre les tables disponibles à une date et heure données.

        PRE : - date est un objet de type datetime.date
              - heure est un objet de type datetime.time 
              - table_list est une liste d'objets de type Table ou None
        POST : Retourne une liste de tables disponibles à la date et heure spécifiées.
        """
        if table_list is None:
            table_list = self.__all_table

        cpy_list = [table for table in table_list]
        if self.__reservations_list:
            cpy_list = []
            for table in table_list:
                i = 0
                reservable = True
                while i < len(table.reservations) and reservable:
                    reservable = self.isReservable(table.reservations[i], (res_heure, res_date))  
                    i += 1
                if reservable:
                    cpy_list.append(table)
        return cpy_list

    def isReservable(self, res: Reservation, suggested_res):
        """
        Vérifie si une réservation peut être faite à une heure et une date suggérées.

        PRE : - res est une instance de la classe Reservation
              - suggested_res est un tuple contenant un objet datetime.time et un objet datetime.date
        POST : Retourne un booléen indiquant si la réservation est possible.
        """
        res_hour = res.hour
        res_date = res.date
        sug_hour = suggested_res[0]
        sug_date = suggested_res[1]
        return res_date != sug_date or (res_date == sug_date and abs((res_hour.hour * 60 + res_hour.minute) - (sug_hour.hour * 60 + sug_hour.minute)) >= 90)

    def filterBySeats(self, seats: int, table_list=None):
        """
        Filtre les tables selon le nombre de sièges.

        PRE : - seats est un entier positif représentant le nombre de sièges requis.
              - table_list est une liste de tables. Si elle est omise, la liste de toutes les tables sera utilisée.
        POST : Retourne une liste de tables disponibles avec au moins le nombre de sièges indiqué.
        """
        if table_list is None:
            table_list = self.__all_table
        cpy_list = [table for table in table_list if table.seat_nbr >= seats]
        print(f"\nListe des tables proposées :\n {cpy_list}")
        return cpy_list

    # Méthodes de gestion des réservations
    def makeReservation(self):
        """
        Effectue une réservation pour une table et des chaises pour bébé si nécessaire.

        PRE : - La table choisie doit être disponible.
              - Les chaises pour bébé sont disponibles dans les limites du restaurant.
        POST : Crée une réservation et l'ajoute à la table et à la liste des réservations.
        """
        typeReservation = input("Sur place 'P' ou sur réservation 'R' : ")
        reservationDate = date.today().strftime("%d/%m/%Y")
        reservationTime = datetime.now().strftime("%H:%M")
        reservationName = "defaultName"
        if typeReservation == "R":
            reservationDate = self.askDate()
            reservationTime = self.askTime()
            reservationName = input("Entrez un nom pour la réservation : ")

        reservationSeats = self.askSeats()

        babySeatWanted = input(
            "Avez-vous besoin de chaises pour bébé ? (oui/non) : ").strip().lower() == "oui"
        babySeatCount = 0

        if babySeatWanted:
            if self.__baby_chairs_available == 0:
                print("Désolé, il n'y a plus de chaises pour bébé disponibles.")
                return
            else:
                babySeatCount = self.askBabySeat()
                if babySeatCount > self.__baby_chairs_available:
                    print(
                        f"Désolé, il n'y a plus assez de chaises pour bébé disponibles. Il reste seulement {self.__baby_chairs_available} chaise(s) pour bébé.")
                    return
                else:
                    self.__baby_chairs_available -= babySeatCount
                    print(f"{babySeatCount} chaises pour bébé réservées.")
                    print(
                        f"Il reste {self.__baby_chairs_available} chaises pour bébé disponibles")

        reservationTable = self.filterBySeats(reservationSeats, self.filterByDateTime(
            reservationDate, reservationTime, self.__all_table))[0]
        reservation = Reservation(
            reservationTable, reservationTime, reservationDate, reservationName)
        self.__reservations_list.append(reservation)
        reservationTable.addReservation(reservation)
        print(
            f"La table a été assignée : {reservationTable} \n{self.__reservations_list[-1]}\n")

    def askDate(self):
        """
        # Loyde 
        PRE : - La date entrée doit être dans le format `dd/mm/yyyy`
            - La date doit être comprise entre aujourd'hui et dans 60 jours maximum (c'est à dire 2 mois maximum) à partir d'aujourd'hui. 

        POST : Retourne un objet de type datetime.date qui repésente la date valide entrée par l'utilisateur.
        """

        valid = False
        formatDate = r"^\d{2}/\d{2}/\d{4}$"
        proposedDate = ""
        today = datetime.today().date()
        max_date = today + timedelta(days=60)
        while not valid:
            proposedDate = input(
                "Entrée une date valide sous le format dd/mm/yyyy (ex:24/10/2023) : ")
            valid = re.match(formatDate, proposedDate)
            if valid:
                proposedDate = datetime.strptime(proposedDate, "%d/%m/%Y").date()
                # valid = proposedDate < max_date
                if today <= proposedDate <= max_date:
                    valid = True

                else:
                    print(
                        f"La date doit être dans les 2 mois suivant aujourd'hui ({today}) et avant le {max_date}.")
                    valid = False
        return proposedDate

    def askTime(self):
        """
        PRE: - 
        POST:
        - renvoie un temps de type date time selon le bon format, et redemande au cas où le format n'a pas été bien entrée
        """
        valid = False
        formatTime = r"^\d{2}:\d{2}$"
        proposedTime = ""
        while not valid:
            proposedTime = input(
                "Entrée une heure valide sous le format hh:mm (ex:20:30) : ")
            valid = re.match(formatTime, proposedTime)
            if valid:
                proposedTime = datetime.strptime(proposedTime, "%H:%M").time()
            return proposedTime

    def askSeats(self):
        """#Hassan
        PRE:
        - 
        POST:
        - renvoie un nombre valide de chaise à entrer et recommence si le nombre de chaise entrée n'est 
            pas entre 1 et 12
        """
        valid = False
        proposedNumber = 0
        while not valid:
            proposedNumber = input(
                "Pour combien de personne (entre 1 et 12) : ")
            if proposedNumber.isdigit():
                proposedNumber = int(proposedNumber)
                valid = 0 < int(proposedNumber) <= 12

        return proposedNumber

    def askBabySeat(self):
        """#Hassan
        PRE:
        - 
        POST:
        - renvoie un nombre valide de chaise à entrer et recommence si le nombre de chaise entrée n'est 
            pas entre 1 et 8
        """
        valid = False
        proposedNumber = 0
        while not valid:
            proposedNumber = input(
                "Combien de chaises pour bébé avez-vous besoin (entre 1 et 8) : ")
            if proposedNumber.isdigit():
                proposedNumber = int(proposedNumber)
                valid = 0 < proposedNumber <= 8
        return proposedNumber

    # Méthodes de gestion des notifications
    def notify(self, message):
        """
        Affiche une notification dans une boîte de dialogue.

        PRE : - message est une chaîne de caractères.
        POST : Affiche la notification et l'ajoute à la liste des notifications.
        """
        timestamp = datetime.now()
        self.__notifications.append((timestamp, message))
        messagebox.showinfo("Notification de table", message)

    def clean_old_notifications(self):
        """
        Supprime les notifications vieilles de plus d'une heure.

        POST : Nettoie les notifications expirées.
        """
        one_hour_ago = datetime.now() - timedelta(hours=1)
        self.__notifications = [
            (time, msg) for time, msg in self.__notifications if time > one_hour_ago]

    def check_table_status(self):
        """
        Vérifie l'état des tables et génère des notifications.

        PRE : self.__all_table est une liste contenant des objets Table.
        POST : Envoie des notifications si une table doit être marquée comme occupée ou si une table se libère bientôt.
        """
        current_time = datetime.now()

        for table in self.__all_table:
            for reservation in table.reservations:
                reservation_time = datetime.combine(
                    current_time.date(), reservation.hour)
                if reservation_time <= current_time <= reservation_time + timedelta(minutes=15):
                    if table.state != 'X':
                        self.notify(
                            f"Rappel : La table {table.t_id()} réservée à {reservation.hour().strftime('%H:%M')} n'est toujours pas marquée occupée.")

                if table.state == 'X' and table.end_time():
                    end_time = table.end_time()
                    if end_time and (end_time - current_time <= timedelta(minutes=15)):
                        self.notify(
                            f"Notification : La table {table.t_id} sera disponible dans 15 minutes.")

    def askpswd(self, attempt):
        return attempt == self.__password

    # Methodes spécials

    def __str__(self):
        return f"{self.__all_table}"

    def __repr__(self):
        return f"{self.__all_table}"

    def sortTablesByAvailability(self, tables):
        """#Hassan
        PRE:
        - tables doit etre une liste de Tables
        - tables ne doit pas etre vides
        POST:
        - renvoie la liste de Table trié par disponibilité selon le nombre de réservation qu'elle possède
        - renvoie une liste vide si il n'y a rien dans la liste ou soulève une erreur si ce n'est pas une liste de table

        """
        tables.sort(key=lambda table: len(table.reservations))
        return tables

    def generateTimeSlots(self, start, end, duration):
        """#Rajae
        Pré:
        :param start: un objet de datetime.time qui représente l'heure de début.
        :param end: un objet de datetime.time qui représente l'heure de fin (start < end)
        :param duration: un objet de type de datetime.timedelta qui repéresente la durée entre deux crénaux (start et end)

        Post:
            return: une liste triée de datetime.time qui représente des crénaux horaires
        """
        slots = []
        current_hour = start
        iterations = 0  # Limite pour éviter une boucle infinie
        max_iterations = 100
        while (datetime.combine(datetime.today(), current_hour) + duration).time() <= end and iterations < max_iterations:
            if current_hour not in slots:
                slots.append(current_hour)
            next_hour = (datetime.combine(datetime.today(),
                         current_hour) + duration).time()
            current_hour = next_hour
            iterations += 1
        slots.sort()
        return slots  # gérer les erreurs

    def getTodayAvailableTimes(self, table):
        """#Rajae
        Pré:
            :param table: un objet de type Table qui contient une liste '_reservation' avec des objets de type Reservation ou chaque
                    Reservation contient un attribut 'hour'
        Post:
            :return: Affiche des crénaux disponibles pour la table .
        """
        open_morning = time(10, 0)
        close_morning = time(14, 30)
        open_evening = time(18, 0)
        close_evening = time(22, 30)

        morning_slots = self.generateTimeSlots(
            open_morning, close_morning, timedelta(minutes=90))
        evening_slots = self.generateTimeSlots(
            open_evening, close_evening, timedelta(minutes=90))

        current_time = datetime.now().time()
        today = datetime.today().date()

        reserved_slots = [(reservation.hour, (datetime.combine(today, reservation.hour) + timedelta(
            minutes=90)).time()) for reservation in table.reservations if reservation.date == today]
        available_slots = [slot for slot in (morning_slots + evening_slots) if slot >
                           current_time and not any(res[0] <= slot < res[1] for res in reserved_slots)]

        print(
            f"Créneaux disponibles pour la table {table.t_id()} aujourd'hui ({today.strftime('%d/%m/%Y')}):")
        if available_slots:
            for slot in available_slots:
                print(slot.strftime("%H:%M"))
        else:
            print("Aucun créneau disponible pour aujourd'hui.")

