from .db_storage import DbStorage
from .csv_storage import CsvStorage


class StorageStrategyFactory:
    def get_strategy(self, type):
        if type == 'database':
            return DbStorage()
        if type == 'csv':
            return CsvStorage()
