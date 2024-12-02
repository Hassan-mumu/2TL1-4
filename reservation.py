from datetime import date, datetime, time


class Reservation:
    id = 1

    def __init__(self, table: list, res_hour : datetime, res_date : datetime, name="defaultName",res_id=None, babychairs=0):
        self.__res_id = res_id if res_id else Reservation.id
        self.__name = name
        self.__table = table if isinstance(table, list) else [table]
        self.__res_hour = res_hour 
        self.__res_date = res_date
        self.__babychairs = babychairs
        
        if not isinstance(res_date, date):
            raise TypeError(f"{res_date} is {type(res_date)} not of datetime type")
        if not isinstance(self.hour, time):
            raise TypeError(f"{res_hour} is {type(res_hour)} not of datetime type")

        # Mise à jour des états des tables
        new_state = 'R' if self.name != "defaultName" else 'X'
        for tb in self.table:
            tb.state = new_state

        Reservation.id += 1
        print(f"La réservation {self.res_id} a été établie.")

    @property
    def res_id(self):
        return self.__res_id
    
    @res_id.setter
    def res_id(self,value):
        self.__res_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def table(self):
        return self.__table

    @table.setter
    def table(self, value):
        self.__table = value if isinstance(value, list) else [value]

    @property
    def res_hour(self):
        return self.__res_hour

    def hour_representation(self):
        return self.res_hour.strftime("%H:%M")

    @res_hour.setter
    def hour(self, value):
        self.__res_hour = value
        
    @property
    def res_date(self):
        return self.__res_date
    
    def date_representation(self):
        return self.res_date.strftime("%d/%m/%y")

    @ res_date.setter
    def date(self, value):
        self.__res_date = value
        
    @property
    def babychairs(self):
        return self.__babychairs
    
    @babychairs.setter
    def babychairs(self,value):
        self.__babychairs = value

    # Méthodes spéciales
    def __str__(self):
        return f"Nom : {self.name}\nTable(s) : {self.table}\nDate : {self.date}\nHeure : {self.hour}"

    def __repr__(self):
        return str(self)
