import sqlite3
from datetime import datetime
from reservation import Reservation
from Table import Table

class DatabaseManager:
    def __init__(self, db_name="restaurant.db"):
        self.db_name = db_name
        self.initialize_database()

    def initialize_database(self):
        """Initialise la base de données en créant les tables nécessaires."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Créer la table `tables`
        cursor.execute('''CREATE TABLE IF NOT EXISTS tables (
                            id INTEGER PRIMARY KEY,
                            seat_nbr INTEGER,
                            state TEXT,
                            start_time TEXT
                        )''')

        # Créer la table `reservations`
        cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            res_hour TEXT,
                            res_date TEXT,
                            babychairs INTEGER,
                            table_ids TEXT
                        )''')
        conn.commit()
        conn.close()

    def save_tables(self, tables):
        """Sauvegarde une liste de tables dans la base de données."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Supprimer les tables existantes
        cursor.execute("DELETE FROM tables")

        # Ajouter les nouvelles tables
        for table in tables:
            cursor.execute('''
                INSERT INTO tables (id, seat_nbr, state, start_time)
                VALUES (?, ?, ?, ?)
            ''', (table.t_id, table.seat_nbr, table.state,
                  table.start_time.strftime('%Y-%m-%d %H:%M:%S') if table.start_time else None))
        conn.commit()
        conn.close()

    def load_tables(self):
        """Charge toutes les tables depuis la base de données."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT id, seat_nbr, state, start_time FROM tables")
        rows = cursor.fetchall()
        tables = []
        for row in rows:
            t_id, seat_nbr, state, start_time = row
            table = Table(seat_nbr, tId=t_id, state=state)
            if start_time:
                table.start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            tables.append(table)

        conn.close()
        return tables

    def save_reservations(self, reservations):
        """Sauvegarde une liste de réservations dans la base de données."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Supprimer les réservations existantes
        cursor.execute("DELETE FROM reservations")

        # Ajouter les nouvelles réservations
        for reservation in reservations:
            cursor.execute('''
                INSERT INTO reservations (id, name, res_hour, res_date, babychairs, table_ids)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (reservation.res_id, reservation.name,
                  reservation.res_hour.strftime('%H:%M:%S'),
                  reservation.res_date.strftime('%Y-%m-%d'),
                  reservation.babychairs,
                  ",".join([str(t.t_id) for t in reservation.table])))
        conn.commit()
        conn.close()

    def load_reservations(self, all_tables):
        """Charge toutes les réservations depuis la base de données."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, res_hour, res_date, babychairs, table_ids FROM reservations")
        rows = cursor.fetchall()
        reservations = []
        for row in rows:
            res_id, name, res_hour, res_date, babychairs, table_ids = row
            res_hour = datetime.strptime(res_hour, '%H:%M:%S').time()
            res_date = datetime.strptime(res_date, '%Y-%m-%d').date()
            table_list = [t for t in all_tables if str(t.t_id) in table_ids.split(",")]
            reservation = Reservation(table_list, res_hour, res_date, name=name, babychairs=babychairs)
            reservations.append(reservation)

        conn.close()
        return reservations
