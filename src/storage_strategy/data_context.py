from .storage_strategy import StorageStrategy


class DataContext:
    def __init__(self, strategy: StorageStrategy):
        self.strategy = strategy

    def save_data(self, level, score):
        self.strategy.save(level, score)

    def load_data(self, level):
        return self.strategy.load(level)

