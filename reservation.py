from Table import Table
from datetime import datetime, date

class Reservation : 
    def __init__(self, table : list , hour=None, date=None, name="defaultName"):
        self._name = name 
        self._table = table if isinstance(table, list) else [table]
        self._hour = hour if bool(hour) else datetime.now().time()
        self._date = date if date is not None else datetime.now().date()
        new_state = 'R' if self._name != "defaultName" else 'X'
        for tb in self._table:
            tb.changeState(new_state)
        
        print(f"La réservation a été établi")

    def getName(self):
        return self._name 
    
    def setName(self, name : str):
        self._name = name 
        
    def getTable(self):
        return self._table 
    
    def setTable(self, table):
        self._table = table 
    
    def getHour(self):
        return self._hour
    
    def setHour(self, hour) : 
        self._hour = hour 
    
    def getDate(self):
        return self._date
    
    def setDate(self, date) : 
        self._date = date 

    def __str__(self):
        return f"Nom : {self.getName()}\nTable(s) : {self.getTable()}\nDate : {self.getDate()}\nHeure : {self.getHour()}"
    
    def __repr__(self):
        return f"Nom : {self.getName()}\nTable(s) : {self.getTable()}\nDate : {self.getDate()}\nHeure : {self.getHour()}"