import os
from typing import List
from matplotlib import pyplot as plt

from Utils.Plots.Plot import Plot


class HeatmapPlot(Plot):
    def __init__(self, name: str, xSize: int, ySize: int):
        super().__init__(name)

        self.xSize: int = xSize
        self.ySize: int = ySize

        self.values: List[List[float]] = [[0 for _ in range(xSize)] for _ in range(ySize)]

    def storeVal(self, xPos: int, yPos: int, val: float):
        assert 0 <= xPos < self.xSize, "X position must be in range [0, xSize)"
        assert 0 <= yPos < self.ySize, "Y position must be in range [0, ySize)"

        self.values[yPos][xPos] += val

    def show(self, saveToPng: bool = False, label: str = ""):
        plt.figure(self.name)
        plt.title(self.name)

        plt.imshow(self.values, cmap="hot", interpolation="nearest")

        if saveToPng:
            if not os.path.exists(self.OUTPUT_DIR):
                os.makedirs(self.OUTPUT_DIR)

            plt.savefig(f"{self.OUTPUT_DIR}/{self.name}-{label}.png")

        plt.show(block=False)

    def clear(self):
        self.values = [[0 for _ in range(self.xSize)] for _ in range(self.ySize)]
