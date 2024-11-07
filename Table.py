import time

class Table:

    id = 0
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
        if new_state in ['X', 'V', 'R']:  # 'X' = occupée, 'V' = disponible, 'R' = réservé
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
        self._start_time = time.perf_counter()
        
    def endTime(self):
        if self._start_time is not None:
            timer_tb = time.perf_counter() - self._start_time
            self.resetTime()
            return timer_tb
        return 0

    def resetTime(self):
        self._start_time = None


    def __str__(self):
        return f"table {self.getId()}"
    
    def __del__(self):
        Table.idTab -= 1
