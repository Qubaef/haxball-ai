import io
from abc import ABC, abstractmethod

from torch.utils.tensorboard import SummaryWriter
from torchvision.transforms import ToTensor
import PIL
import matplotlib.pyplot as plt


class Plot(ABC):

    OUTPUT_DIR: str = "plots"

    def __init__(self, name: str, writer: SummaryWriter, step: int):
        self.name: str = name
        self.writer = writer
        self.step = step

    @abstractmethod
    def show(self, label: str = "") -> None:
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        raise NotImplementedError()

    def store_in_tensorboard(self, plot_name):
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        # convert image to torch format
        image = PIL.Image.open(buf)
        image = ToTensor()(image).unsqueeze(0)
        self.writer.add_image(plot_name, image[0], self.step)
