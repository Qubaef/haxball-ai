import os
from typing import List
import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter

from Utils.Plots.Plot import Plot


class LinePlot(Plot):
    def __init__(
        self,
        name: str,
        xLabel: str,
        yLabels: List[str],
        writer: SummaryWriter,
        step: int,
    ):
        super().__init__(name, writer, step)

        self.xLabel: str = xLabel
        self.yLabels: List[str] = yLabels

        self.values: list = []
        self.values.append([])
        self.values.append([[] for _ in range(len(yLabels))])
        self.writer = writer
        self.step = step

    def storeVal(self, xVal: float, yVals: List[float]) -> None:
        assert len(yVals) == len(
            self.yLabels
        ), "Number of y values must match number of y labels"

        self.values[0].append(xVal)
        for i in range(len(yVals)):
            self.values[1][i].append(yVals[i])

    def show(self, label: str = "") -> None:
        plt.figure(self.name)
        plt.title(self.name)

        plt.xlabel(self.xLabel)

        for i in range(len(self.yLabels)):
            plt.plot(self.values[0], self.values[1][i], label=self.yLabels[i])

        self.store_in_tensorboard(f"{self.name}-{label}")
        plt.show(block=False)

    def store(self, label: str = "") -> None:
        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)

        self.store_in_tensorboard(f"{self.name}-{label}")

    def clear(self):
        self.values[0].clear()
        for i in range(len(self.values[1])):
            self.values[1][i].clear()
