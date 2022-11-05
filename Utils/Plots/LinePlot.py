import os
from typing import List
import matplotlib.pyplot as plt

from Utils.Plots.Plot import Plot


class LinePlot(Plot):
    def __init__(self, name: str, xLabel: str, yLabels: List[str]):
        super().__init__(name)

        self.xLabel: str = xLabel
        self.yLabels: List[str] = yLabels

        self.values: list = []
        self.values.append([])
        self.values.append([[] for _ in range(len(yLabels))])

    def storeVal(self, xVal: float, yVals: List[float]) -> None:
        assert len(yVals) == len(
            self.yLabels
        ), "Number of y values must match number of y labels"

        self.values[0].append(xVal)
        for i in range(len(yVals)):
            self.values[1][i].append(yVals[i])

    def show(self, saveToPng: bool = False, label: str = "") -> None:
        plt.figure(self.name)
        plt.title(self.name)

        plt.xlabel(self.xLabel)

        for i in range(len(self.yLabels)):
            plt.plot(self.values[0], self.values[1][i], label=self.yLabels[i])

        if saveToPng:
            if not os.path.exists(self.OUTPUT_DIR):
                os.makedirs(self.OUTPUT_DIR)

            plt.savefig(f"{self.OUTPUT_DIR}/{self.name}-{label}.png")

        plt.show(block=False)

    def store(self, label: str = "") -> None:
        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)

        plt.savefig(f"{self.OUTPUT_DIR}/{self.name}-{label}.png")

    def clear(self):
        self.values[0].clear()
        for i in range(len(self.values[1])):
            self.values[1][i].clear()
