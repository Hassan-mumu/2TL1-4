import sqlite3
from datetime import datetime, timedelta
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

    def clean_expired_reservations(self):
        """Supprime les réservations expirées et met à jour l'état des tables associées."""
        now = datetime.now()
        today = now.date()
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Rechercher les réservations expirées
        expired_reservations_query = """
            SELECT id, table_ids
            FROM reservations
            WHERE res_date = ? AND time(res_hour) <= time(?)
        """
        cursor.execute(expired_reservations_query, (today, (now - timedelta(minutes=30)).time().strftime('%H:%M:%S')))
        expired_reservations = cursor.fetchall()

        for reservation_id, table_ids in expired_reservations:
            if table_ids:  # Vérifie que des tables sont associées
                table_id_list = table_ids.split(",")  # Transforme les IDs des tables en liste
                for table_id in table_id_list:
                    # Vérifie si la table est associée à une autre réservation
                    cursor.execute("""
                        SELECT COUNT(*)
                        FROM reservations
                        WHERE instr(table_ids, ?) > 0
                    """, (table_id,))
                    other_reservations = cursor.fetchone()[0]

                    # Vérifie que la table n'est pas occupée (state != 'X')
                    cursor.execute("SELECT state FROM tables WHERE id = ?", (table_id,))
                    current_state = cursor.fetchone()[0]

                    # Si aucune autre réservation n'est associée ET la table est en état 'R'
                    if other_reservations == 0 and current_state == 'R':
                        cursor.execute("UPDATE tables SET state = 'V' WHERE id = ?", (table_id,))
                        print(f"Table {table_id} mise à jour à l'état 'V' (plus aucune réservation et non occupée).")

            # Supprimer la réservation expirée
            cursor.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
            print(f"Réservation {reservation_id} supprimée (expirée).")

        conn.commit()
        conn.close()
        print("Les réservations expirées ont été supprimées et les tables associées mises à jour.")

#supprimer la réservation.