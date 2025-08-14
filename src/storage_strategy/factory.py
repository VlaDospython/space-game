from .db_storage import DbStorage
from .csv_storage import CsvStorage
from .redis_storage import RedisStorage


class StorageStrategyFactory:
    def get_strategy(self, type):
        if type == 'database':
            return DbStorage()
        if type == 'csv':
            return CsvStorage()
        if type == 'redis':
            return RedisStorage
