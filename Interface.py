from anyio import current_time
from tkinter import messagebox
from Reservation import Reservation
from Table import Table
from datetime import *
import re


class Interface():

    def __init__(self, *tables):
        self._all_table = list(tables) if tables else []
        self._available_table = []
        self._occupied_table = []
        self._reservations_list = []
        self.__password = 0000
    

    def addTable(self, table):
        if isinstance(table, Table):
            table = [table]
        for tab in table:
            if tab.getState() == 'V':
                self._available_table.append(tab)
                self._all_table.append(tab)
    

    def askpswd(self, attempt):
        return attempt == self.__password


    def filterByDateTime(self,date, heure ,table_list):
        if table_list == None:
            table_list = self._all_table

        cpy_list = [table for table in table_list]
        if self._reservations_list != []:
            cpy_list = [[table for reservation in table._reservations if  self.isReservable(reservation, (heure,date))] for table in table_list]
        return cpy_list


    def isReservable(self, res, suggested_res ):
        res_hour = res.getHeure()
        res_date = res.getDate()
        sug_hour = suggested_res[0]
        sug_date = suggested_res[1]
        return res_date == sug_date and abs((res_hour.hour * 60 + res_hour.minute)-(sug_hour.hour * 60 + sug_hour.minute) >= 90 )


    def filterBySeats(self, seats : int, table_list=None):
        if table_list == None:
            table_list = self._all_table
        cpy_list = [table for table in table_list if table._seat_nbr >= seats]
        print(f"\nListe des tables proposé :\n {cpy_list}")
        return cpy_list            
    

    def dsplayBy(self,table : list, date, heure, seats):
        t = self.filterBySeats(seats, self.filterByDateTime(date, heure, table))
        print(t)
        return t


    def askDate(self):
        valid = False
        formatDate = r"^\d{2}/\d{2}/\d{4}$"
        proposedDate = ""
        today = datetime.today().date()
        max_date = today + timedelta(days=60)
        while not valid:
            proposedDate = input("Entrée une date valide sous le format dd/mm/yyyy (ex:24/10/2023) : ")
            valid = re.match(formatDate, proposedDate)
            if valid:
                proposedDate = datetime.strptime(proposedDate,"%d/%m/%Y").date()
                #valid = proposedDate < max_date
                if today <= proposedDate <= max_date:
                    valid = True

                else:
                    print(f"La date doit être dans les 2 mois suivant aujourd'hui ({today}) et avant le {max_date}.")
                    valid = False
        return proposedDate


    def askTime(self):
        valid = False
        formatTime = r"^\d{2}:\d{2}$"
        proposedTime = ""
        while not valid:
            proposedTime = input("Entrée une heure valide sous le format hh:mm (ex:20:30) : ")  # à faire: ne pouvoir entrer des heures que si elles sont entre les crénaux de 10H - 14h30 et 18h - 22h30
            valid = re.match(formatTime, proposedTime)
            if valid:
                proposedTime = datetime.strftime(proposedTime,"%H:%M").time()
        return proposedTime
    
    
    def askSeats(self):
        valid = False
        proposedNumber = 0
        while not valid :
            proposedNumber = input("Pour combien de personne (entre 1 et 12) : ")
            if proposedNumber.isdigit():
                proposedNumber = int(proposedNumber)
                valid = 0 < int(proposedNumber) <= 12

        return proposedNumber
    

    def makeReservation(self):
        typeReservation = input("Sur place 'P' ou sur reservation 'R' : ")
        reservationDate = date.today().strftime("%d/%m/%Y")
        reservationTime = datetime.now().strftime("%H:%M")
        reservationName = "defaultName"
        if typeReservation == "R":
            reservationDate = self.askDate()
            reservationTime = self.askTime()
            reservationName = input("Entrée un nom pour la réservation : ")

        reservationSeats = self.askSeats()
        reservationTable = self.filterBySeats(reservationSeats,self.filterByDateTime(reservationDate, reservationTime, self._all_table))[0]
        self._reservations_list.append(Reservation(reservationTable,reservationTime, reservationDate, reservationName))
        print(f"La table à été assigné : {reservationTable} \n{self._reservations_list[-1]}\n")

    def __str__(self):
        return f"{self._all_table}"
    
    def __repr__(self):
        return f"{self._all_table}"

    def sortTablesByAvailability(self, tables):
        tables.sort(key=lambda table: len(table._reservations))
        return tables

    def generateTimeSlots(self,start,end,duration):
        """#Rajae
        Pré:
        :param start: un objet de datetime.time qui représente l'heure de début.
        :param end: un objet de datetime.time qui représente l'heure de fin (start < end)
        :param duration: un objet de type de datetime.timedelta qui repéresente la durée entre deux crénaux (start et end)

        Post:
            return: une liste triée de datetime.time qui représente des crénaux horaires
        """
        slots=[]
        current_hour=start
        iterations = 0  # Limite pour éviter une boucle infinie
        max_iterations = 100
        while(datetime.combine(datetime.today(), current_hour) + duration).time() <= end and iterations < max_iterations:
            if current_hour not in slots:
                slots.append(current_hour)
            next_hour=(datetime.combine(datetime.today(),current_hour) + duration).time()
            current_hour=next_hour
            iterations += 1
        slots.sort()
        return slots #gérer les erreurs

    def getTodayAvailableTimes(self, table):
        """#Rajae
        Pré:
            :param table: un objet de type Table qui contient une liste '_reservation' avec des objets de type Reservation ou chaque
                    Reservation contient un attribut 'hour'
        Post:
            :return: Affiche des crénaux disponibles pour la table .
        """
        open_morning=  time(10,0)
        close_morning= time(14,30)
        open_evening = time(18,0)
        close_evening= time(22,30)

        morning_slots=self.generateTimeSlots(open_morning,close_morning,timedelta(minutes=90))
        evening_slots=self.generateTimeSlots(open_evening,close_evening,timedelta(minutes=90))

        current_time=datetime.now().time()
        today = datetime.today().date()

        reserved_slots=[ (reservation.hour , (datetime.combine(today, reservation.hour)+ timedelta(minutes=90)).time()) for reservation in table._reservations if reservation.date == today ]
        available_slots=[ slot for slot in (morning_slots + evening_slots) if slot> current_time and not any(res[0]<= slot < res[1] for res in reserved_slots) ]

        print(f"Créneaux disponibles pour la table {table.getId()} aujourd'hui ({today.strftime('%d/%m/%Y')}):")
        if available_slots:
            for slot in available_slots:
                print(slot.strftime("%H:%M"))
        else:
            print("Aucun créneau disponible pour aujourd'hui.")


    def check_table_status(self):
        """ #Rajae
        Pré: self._all_table est une liste contenant des objets de type Table.
        -chaque objet Table doit avoir :
            - une méthode gatState() qui retourne un état parti ['X','R','V']
            - une méthode endTime() qui retourne qui retourne un datetime ou None
            - une liste _reservations contenant des objets Reservation.
        -chaque objet Reservation doit avoir :
            - une méthode getHour() sui retourne un objet datetime.time
            - une méthode getDate() qui retourne un objet datetime.date

        Post :
        -Génère une notification via self.notify(message) si :
          - l'heure actuelle est exactement exacte à l'heure de la réservation
          et la table concerné n'est pas occupée .
          -une table occupée sera libre dans 15 minutes.
        """
        current_time= datetime.now()

        for table in self._all_table:
            for reservation in table._reservations:
                reservation_time=datetime.combine(current_time.date(),reservation.getHour())
                if reservation_time <= current_time <= reservation_time + timedelta(minutes=15):
                    if table.getState() != 'X':
                        self.notify(f"Rappel : La table {table.getId()} réservée à {reservation.getHour().strftime('%H:%M')} n'est toujours pas marquée occupée.")

                if table.getState== 'X' and table.endTime():
                    end_time = table.endTime()
                    if end_time and (end_time - current_time <= timedelta(minutes=15)):
                        self.notify(f"Notification : La table {table.getId()} sera disponible dans 15 minutes.")


    def notify(self, message):
        # Affiche une notification dans une boîte de dialogue
        messagebox.showinfo("Notification de table", message)


"""
Note d'ajout: 
- Dans makeReservation, faire en sorte d'ajouter la reservation à la table
- Faire en sorte de pouvoir ajouter plusieurs tables à une reservation (mergedTable)
- Faire une fonction qui check les réservations, places les tables dans les listes correspondantes et change l'état des Tables si l'heure des réservation correspond 
- Permettre la gestion de chaises pour bébé (on peut supposer 8 chaises dans tout le restaurant)
"""
