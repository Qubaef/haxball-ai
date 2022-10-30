from abc import ABC


class Entity(ABC):
    def update(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError
