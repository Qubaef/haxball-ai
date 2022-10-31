import os
from typing import Dict, Tuple, List
import matplotlib.pyplot as plt
import numpy as np


class DataStory(object):
    def __init__(self, outputDir: str):
        self.outputDir: str = outputDir

        self.valuesDict: Dict[str, List[List, List[List]]] = {}

    def storeVal(self, name: str, xVal: float, yVals: List[float]):
        if name not in self.valuesDict:
            self.valuesDict[name] = []
            self.valuesDict[name].append([])
            self.valuesDict[name].append([[] for _ in range(len(yVals))])

        assert len(yVals) == len(self.valuesDict[name][1])

        self.valuesDict[name][0].append(xVal)
        for i in range(len(yVals)):
            self.valuesDict[name][1][i].append(yVals[i])

    def plot(self, show: bool = True, storeToPng: bool = False, clearAfterPlot: bool = False):
        # Create output directory if it doesn't exist
        if not os.path.exists(self.outputDir):
            os.makedirs(self.outputDir)

        for name, values in self.valuesDict.items():
            plt.figure(name)
            plt.title(name)
            for i in range(len(values[1])):
                plt.plot(values[0], values[1][i])

            if show:
                plt.show()

            if storeToPng:
                plt.savefig(f"{self.outputDir}/{name}.png")

            plt.clf()

            if clearAfterPlot:
                self.valuesDict[name][0].clear()
                for i in range(len(values[1])):
                    self.valuesDict[name][1][i].clear()
