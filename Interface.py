from Reservation import Reservation
from Table import Table
from datetime import datetime, date
import re
import time


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
        print(cpy_list)          
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
        return cpy_list            
    

    def dsplayBy(self,table : list, date, heure, seats):
        t = self.filterBySeats(seats, self.filterByDateTime(date, heure, table))
        print(t)
        return t


    def askDate(self):
        valid = False
        formatDate = r"^\d{2}/\d{2}/\d{4}$"
        proposedDate = ""
        while not valid:
            proposedDate = input("Entrée une date valide sous le format dd/mm/yyyy (ex:24/10/2023) : ")
            valid = re.match(formatDate, proposedDate)
            if valid:
                proposedDate = datetime.strptime(proposedDate,"%d/%m/%Y").date()
        return proposedDate

    
    def askTime(self):
        valid = False
        formatTime = r"^\d{2}:\d{2}$"
        proposedTime = ""
        while not valid:
            proposedTime = input("Entrée une heure valide sous le format hh:mm (ex:20:30) : ")  # à faire: ne pouvoir entrer des heures que si elles sont entre les crénaux de 10H - 14h30 et 18h - 22h30
            valid = re.match(formatTime, proposedTime)
            if valid:
                proposedTime = datetime.strptime(proposedTime,"%H:%M").time()
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
        

    def makeReservation(self, typeReservation="P"):
        reservationDate = date.today().strftime("%d/%m/%Y")
        reservationTime = datetime.now().strftime("%h:%m")
        reservationName = "defaultName"
        if typeReservation == "R":
            reservationDate = self.askDate()
            reservationTime = self.askTime()
            reservationName = input("Entrée un nom pour la réservation : ")

        reservationSeats = self.askSeats()
        reservationTable = self.filterBySeats(reservationSeats,self.filterByDateTime(reservationDate, reservationTime, self._all_table))[0]
        self._reservations_list.append(Reservation(reservationTable,reservationTime, reservationDate, reservationName))


    def sortTablesByAvailability(self, tables):
            tables.sort(key=lambda table: len(table.reservations))

    def __str__(self):
        return f"{self._all_table}"
    
    def __repr__(self):
        return f"{self._all_table}"
    
interface = Interface()

for i in range(1, 21):
    if i <= 10:
        interface.addTable(Table(2))
    elif i <= 16:
        interface.addTable(Table(4))
    else:
        interface.addTable(Table(6))

interface.makeReservation()
            

"""
Note d'ajout: 
- la date proposer ne doit pas excéder 2mois
- Faire une fonction qu trie les listes des tables par les tables les plus disponibles aux moins disponibles
- Faire une fonction qui affiche les heures disponibles pour une tables choisis
- Faire une fonction qui affiche les listes des tables selon un format clair et bien visuelle
- Dans makeReservation, faire en sorte d'ajouter la reservation à la table
- Faire le système de notification (flou)
- Faire en sorte de pouvoir ajouter plusieurs tables à une reservation (mergedTable)
- Faire une fonction qui check les réservation, places les tables dans les listes correspondantes et change l'état des Tables si l'heure des réservation correspond 
"""