from .storage_strategy import StorageStrategy
from datetime import datetime
import getpass
import sqlite3
from src.constants import *


class DbStorage(StorageStrategy):
    def __init__(self):
        with sqlite3.connect(SCORES_DB_FILENAME) as connection:
            cursor = connection.cursor()

            cursor.execute("""
               CREATE TABLE IF NOT EXISTS "scores" (
                   "id"	INTEGER,
                   "username"	TEXT NOT NULL,
                   "datetime"	TEXT NOT NULL,
                   "level"	INTEGER NOT NULL,
                   "score"	INTEGER NOT NULL,
               PRIMARY KEY("id" AUTOINCREMENT)
               )   
            """)

    def save(self, level, score):
        name = getpass.getuser()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with sqlite3.connect(SCORES_DB_FILENAME) as connection:
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO "scores" ("username", "datetime", "level", "score") VALUES (?, ?, ?, ?)
            """, (name, now, level, score))

    def load(self, level):
        try:
            with sqlite3.connect(SCORES_DB_FILENAME) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                                    SELECT MAX(score) FROM scores WHERE level = ?
                                """, (level,))
                result = cursor.fetchone()
                return result[0] if result[0] is not None else 0

        except (FileNotFoundError, ValueError, IndexError):
            return 0

