from abc import ABC, abstractmethod


class StorageStrategy(ABC):
    @abstractmethod
    def save(self, level, score):
        pass

    @abstractmethod
    def load(self, level):
        pass
