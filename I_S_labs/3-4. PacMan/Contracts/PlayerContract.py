from abc import ABC, abstractmethod


class IPlayer(ABC):
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def update(self):
        pass
