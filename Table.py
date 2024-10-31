import time

class Table:
    def __init__(self, tableId, seat_nbr, state="V"):# command_nbr=0):
        self._tableId = tableId
        self._seat_nbr = seat_nbr
        self._state = state
        self._start_time = None


    def getTable_Id(self):
        return self._tableId

    def setTable_Id(self, tableId):
        self._tableId = tableId

    def getSeat_nbr(self):
        return self._seat_nbr

    def setSeat_nbr(self, seat_nbr):
        self._seat_nbr = seat_nbr

    #def getCommand_nbr(self):
        #return self._command_nbr

    #def setCommand_nbr(self, command_nbr):
        #self._command_nbr = command_nbr

    def changeState(self, new_state):
        if new_state in ['X', 'V', 'R']:  # 'X' = occupée, 'V' = disponible, 'R' = réservé
            self._state = new_state
            if new_state == 'X':
                self.startTime()
            elif new_state == 'V':
                self.resetTime()
            #elif new_state == 'R':
                #self.startTime()

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


