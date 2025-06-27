from .storage_strategy import StorageStrategy
from datetime import datetime
import getpass
import csv
from src.constants import *

class CsvStorage(StorageStrategy):
    def save(self, level, score):
        name = getpass.getuser()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(SCORES_FILENAME, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, now, level, score])

    def load(self, level):
        try:
            with open(SCORES_FILENAME, "r") as f:
                reader = csv.reader(f)
                level_scores = [int(row[3]) for row in reader if int(row[2]) == level]
                return max(level_scores) if level_scores else 0
        except (FileNotFoundError, ValueError, IndexError):
            return 0
