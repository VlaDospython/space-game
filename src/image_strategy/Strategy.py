from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def get_surface(self):
        pass