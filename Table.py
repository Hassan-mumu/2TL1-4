from datetime import datetime, timedelta


class Table:
    id = 1

    def __init__(self, seat_nbr: int, tId=None, state="V", start_time=None):
        self.__t_id = tId if tId else Table.id
        self.__seat_nbr = seat_nbr
        self.__state = state
        self.__reservations = []
        self.__start_time = start_time
        Table.id += 1

    # Propriétés pour table_id
    @property
    def t_id(self):
        return self.__t_id

    @t_id.setter
    def t_id(self, value):
        self.__t_id = value

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
        now = datetime.now()

        # Si la table est en état 'R' (Réservée), vérifier si le temps est dépassé
        if self.__state == 'R':
            for reservation in self.__reservations:
                res_time = datetime.combine(reservation.res_date, reservation.res_hour)
                if now > res_time + timedelta(minutes=30):  # Réservation expirée
                    print(f"La réservation pour la table {self.__t_id} a expiré.")
                    self.remove_reservation(reservation)
                    self.__state = 'V'  # Table redevient disponible
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
        return f"Table {self.t_id}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Table):
            return self.t_id == other.table_id
        return False

