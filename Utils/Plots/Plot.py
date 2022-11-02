from abc import ABC, abstractmethod


class Plot(ABC):

    OUTPUT_DIR: str = "plots"

    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def show(self, saveToPng: bool = False, label: str = ""):
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        raise NotImplementedError()
