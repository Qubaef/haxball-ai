import os
from collections import deque
from typing import Dict, Deque, Tuple
import matplotlib.pyplot as plt
import numpy as np


class DataStory(object):
    def __init__(self, outputDir: str, maxLen: int):
        self.outputDir: str = outputDir
        self.maxLen: int = maxLen

        self.valuesDict: Dict[str, Tuple[Deque, Deque]] = {}

    def storeVal(self, name: str, xVal: float, yVal: float):
        if name not in self.valuesDict:
            self.valuesDict[name] = (deque(maxlen=self.maxLen), deque(maxlen=self.maxLen))

        self.valuesDict[name][0].append(xVal)
        self.valuesDict[name][1].append(yVal)

    def plot(self, show: bool = True, storeToPng: bool = False, clearAfterPlot: bool = False):
        # Create output directory if it doesn't exist
        if not os.path.exists(self.outputDir):
            os.makedirs(self.outputDir)

        for name, values in self.valuesDict.items():
            # Create new named figure
            plt.plot(values[0], values[1], label=name)
            plt.legend()

            if show:
                plt.show()

            if storeToPng:
                plt.savefig(f"{self.outputDir}/{name}.png")

            plt.clf()

            if clearAfterPlot:
                self.valuesDict[name] = (deque(maxlen=self.maxLen), deque(maxlen=self.maxLen))
