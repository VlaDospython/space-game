from .storage_strategy import StorageStrategy
from datetime import datetime
import getpass
from src.constants import *
import sqlite3


class DbStorage(StorageStrategy):
    def __init__(self):
        self.connection = sqlite3.connect("data/scores.db")
        self.cursor = self.connection.cursor()

    def save(self, level, score):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS "scores" (
            "id"	INTEGER,
            "username"	TEXT NOT NULL,
            "datetime"	TEXT NOT NULL,
            "level"	INTEGER NOT NULL,
            "score"	INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        )   
        """)

        self.cursor.execute("""
        INSERT INTO "scores" ("username", "datetime", "level", "score") VALUES (?, ?, ?, ?)
        """, ("admin", "2025-06-22 19:01:46", 3, 568))
        self.connection.commit()

    def load(self, level):
        try:
            self.cursor.execute("""
                    SELECT MAX(score) FROM scores WHERE level = ?
                """, (level,))
            result = self.cursor.fetchone()
            return result[0] if result[0] is not None else 0
        except (FileNotFoundError, ValueError, IndexError):
            return 0

    def __del__(self):
        self.connection.close()
