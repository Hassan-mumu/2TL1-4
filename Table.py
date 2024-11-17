import time
from datetime import datetime


class Table:

    id = 1
    def __init__(self, seat_nbr : int, state="V"):# command_nbr=0):
        
        self._tableId = Table.id
        self._seat_nbr = seat_nbr
        self._state = state
        self._reservations = []
        self._start_time = None
        Table.id += 1


    def getId(self):
        return self._tableId

    def setId(self, tableId):
        self._tableId = tableId

    def getSeat_nbr(self):
        return self._seat_nbr

    def setSeat_nbr(self, seat_nbr):
        self._seat_nbr = seat_nbr

    #def getCommand_nbr(self):
        #return self._command_nbr

    #def setCommand_nbr(self, command_nbr):
        #self._command_nbr = command_nbr

    def getState(self):
            return self._state

    def changeState(self, new_state):
        """#Rajae
        Pré: param new_state: doit être une valeur valide parmi ['X', 'V', 'R']

        Post:
            return: le nouvel état de la table si la valeur est valide.
            return: None si la valeur new_state est invalide.
        """

        if new_state not in ['X', 'V', 'R']:
            return None # 'X' = occupée, 'V' = disponible, 'R' = réservé
        self._state = new_state
        if new_state == 'X':
            self.startTime()
        elif new_state == 'V':
            self.resetTime()
        #elif new_state == 'R':
            #self.startTime()
        return new_state
    
    def addReservation(self, reservation):
        if reservation not in self._reservations:
            self._reservations.append(reservation)

    def removeReservation(self, reservation):
        if reservation in self._reservations:
            self._reservations.remove(reservation)

    def startTime(self):
        self._start_time = datetime.now()
        
    def endTime(self):
        """#Rajae
        Pré:
        -l'attribut self._star_time doit être un objet datetime qui représente le début d'occupation.

        Post:
        - return :  - un objet datetime si la table est occupée = self._star_time + 90
                    - None si la table n'est pas occupée .


        """
        if self._start_time is not None:
            return self._start_time + timedelta(minutes=90)
        return None

        #if self._start_time is not None:
           # timer_tb = time.perf_counter() - self._start_time
           # self.resetTime()
            #return timer_tb
        #return 0


    def resetTime(self):
        self._start_time = None


    def __str__(self):
        return f"table {self.getId()}\n Nombre de place : {self.getSeat_nbr()}\n"
    
    def __repr__(self):
        return f"table {self.getId()}\n Nombre de place : {self.getSeat_nbr()}\n"
    