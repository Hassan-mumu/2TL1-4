from Reservation import Reservation
from Table import Table
from datetime import datetime, date
from copy import deepcopy


class Interface():
    def __init__(self, *tables):
        self._all_table = list(tables)
        self._occupied_table = []
        self._reservations_list = []
        self.__password = 0000
    

    def addTable(self, table):
        if isinstance(table, Table):
            table = [table]
        for tab in table:
            if table.getState == 'V':
                self._available_table.append(tab)
    

    def askpswd(self, attempt):
        return attempt == self.__password


    def filterByDateTime(self,date, heure ,table_list):
        cpy_list = deepcopy(table_list) 
        if table_list == None:
            table_list = self._all_table
            cpy_list = deepcopy(self._all_table)

        if self._reservations_list != []:
            for table in table_list:
                if table._reservations != []:
                    for reservation in table._reservations:
                        if self.isNotReservable(reservation, (heure,date)):
                            cpy_list.remove(table)
                            
        return cpy_list


    def isNotReservable(self, res, suggested_res ):
        res_hour = res.getHeure()
        res_date = res.getDate()
        sug_hour = suggested_res[0]
        sug_date = suggested_res[1]
        return res_date == sug_date and abs((res_hour.hour * 60 + res_hour.minute)-(sug_hour.hour * 60 + sug_hour.minute) < 90 )
    

    def filterBySeats(self, seats : int, table_list=None):
        cpy_list = deepcopy(table_list) 
        if table_list == None:
            table_list = self._all_table
            cpy_list = deepcopy(self._all_table)
        
        for table in table_list:
            if table.seat_nbr < seats:
                cpy_list.remove(table)    

        return cpy_list            
    

    def dsplayBy(self,table : list, date, heure, seats):
        t = self.filterBySeats(seats, self.filterByDateTime(date, heure, table))
        print(t)
        return t


    def makeReservation(self, typeReservation): 
        
        if typeReservation == "R":
            seats = int(input("Pour combien de personne : (max 12)"))

