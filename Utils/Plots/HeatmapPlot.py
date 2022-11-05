import os
from typing import List
from matplotlib import pyplot as plt
from torch.utils.tensorboard import SummaryWriter

from Utils.Plots.Plot import Plot


class HeatmapPlot(Plot):
    def __init__(
        self, name: str, xSize: int, ySize: int, writer: SummaryWriter, step: int
    ):
        super().__init__(name, writer, step)

        self.xSize: int = xSize
        self.ySize: int = ySize

        self.values: List[List[float]] = [
            [0 for _ in range(xSize)] for _ in range(ySize)
        ]

    def storeVal(self, xPos: int, yPos: int, val: float) -> None:
        assert 0 <= xPos < self.xSize, "X position must be in range [0, xSize)"
        assert 0 <= yPos < self.ySize, "Y position must be in range [0, ySize)"

        self.values[yPos][xPos] += val

    def show(self, label: str = "") -> None:
        plt.figure(self.name)
        plt.title(self.name)

        plt.imshow(self.values, cmap="hot", interpolation="nearest")

        self.store_in_tensorboard(f"{self.name}-{label}")

        plt.show(block=False)

    def clear(self):
        self.values = [[0 for _ in range(self.xSize)] for _ in range(self.ySize)]
