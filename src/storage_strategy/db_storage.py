from .storage_strategy import StorageStrategy
from datetime import datetime
import getpass
from src.constants import *

class DbStorage(StorageStrategy):
    def save(self, level, score):
        pass

    def load(self, level):
        try:
            pass
        except (FileNotFoundError, ValueError, IndexError):
            return 0
