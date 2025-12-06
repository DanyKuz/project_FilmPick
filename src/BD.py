import sqlite3
import os
from datetime import date

class FilmDB:
    def __init__(self, db_path="data/films.db"):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS films (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT,
                    age_restriction TEXT,
                    status TEXT DEFAULT 'не смотрел',
                    date_added TEXT,
                    rating INTEGER CHECK(rating >= 0 AND rating <= 10),
                    cover TEXT
                )
            """)
            conn.commit()

    def add_film(self, title, category=None, age_restriction=None,
                 status="не смотрел", rating=None, cover=None):
        today = date.today().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO films (title, category, age_restriction, status, date_added, rating, cover)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (title, category, age_restriction, status, today, rating, cover))
            conn.commit()
            return cursor.lastrowid

    def get_all_films(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM films ORDER BY date_added DESC, title")
            return cursor.fetchall()

    def delete_film(self, film_id):
        if not isinstance(film_id, int):
            raise ValueError("film_id must be an integer")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM films WHERE id = ?", (film_id,))
            conn.commit()

    def update_film_status(self, film_id, new_status):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE films SET status = ? WHERE id = ?", (new_status, film_id))
            conn.commit()

    def get_random_film_by_category(self, category=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if category:
                cursor.execute("SELECT * FROM films WHERE category = ? ORDER BY RANDOM() LIMIT 1", (category,))
            else:
                cursor.execute("SELECT * FROM films ORDER BY RANDOM() LIMIT 1")
            return cursor.fetchone()
