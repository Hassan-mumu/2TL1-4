from datetime import datetime, timedelta


class Table:
    id = 1

    def __init__(self, seat_nbr: int, tId=None, state="V"):
        self.__table_id = tId if tId else Table.id
        self.__seat_nbr = seat_nbr
        self.__state = state
        self.__reservations = []
        self.__start_time = None
        Table.id += 1

    # Propriétés pour table_id
    @property
    def table_id(self):
        return self.__table_id

    @table_id.setter
    def table_id(self, value):
        self.__table_id = value

    # Propriétés pour seat_nbr
    @property
    def seat_nbr(self):
        return self.__seat_nbr

    @seat_nbr.setter
    def seat_nbr(self, value):
        self.__seat_nbr = value

    # Propriétés pour state
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, new_state):
        """Change l'état de la table et met à jour le temps si nécessaire."""
        if new_state not in ['X', 'V', 'R']:
            raise ValueError("État invalide : doit être 'X', 'V' ou 'R'")
        self.__state = new_state
        if new_state == 'X':
            self.start_time = datetime.now()
        elif new_state == 'V':
            self.reset_time()

    # Propriétés pour reservations
    @property
    def reservations(self):
        return self.__reservations

    def add_reservation(self, reservation):
        if reservation not in self.reservations:
            self.__reservations.append(reservation)

    def remove_reservation(self, reservation):
        """Retire une réservation si elle est présente."""
        if reservation in self.reservations:
            self.__reservations.remove(reservation)

    # Propriétés pour start_time
    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, value):
        self.__start_time = value

    def end_time(self):
        """Retourne l'heure de fin d'occupation (90 minutes après start_time)."""
        if self.start_time is not None:
            return self.start_time + timedelta(minutes=90)
        return None

    def reset_time(self):
        """Réinitialise le temps de début."""
        self.__start_time = None

    # Méthodes spéciales
    def __str__(self):
        return f"Table {self.table_id} (Seats: {self.seat_nbr}, State: {self.state})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Table):
            return self.table_id == other.table_id
        return False
