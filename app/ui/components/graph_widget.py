from typing import Callable

from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import QSizePolicy

from app.models.errors import NumericalError


class GraphWidget(FigureCanvasQTAgg):
    def __init__(self) -> None:
        figure = Figure(figsize=(7, 4.5), layout="constrained")
        super().__init__(figure)
        self.axes = figure.add_subplot(111)
        self.setMinimumHeight(380)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def render(self, painter: Callable[[Axes], None]) -> None:
        self.axes.clear()
        try:
            painter(self.axes)
        except NumericalError:
            self.axes.clear()
            self.axes.text(
                0.5,
                0.5,
                "Unable to draw the graph",
                ha="center",
                va="center",
                transform=self.axes.transAxes,
            )
        self.axes.grid(True, alpha=0.3)
        self.draw()

    def clear_plot(self) -> None:
        self.axes.clear()
        self.draw()
