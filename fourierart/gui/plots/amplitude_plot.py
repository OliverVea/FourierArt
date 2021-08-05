from fourierart import db_to_lin, PlotProperties

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class AmplitudePlot(FigureCanvasQTAgg):
    def __init__(self):
        fig = Figure(edgecolor=PlotProperties.primary_color, facecolor=PlotProperties.background_color)
        self.axes = fig.add_subplot(111, facecolor=PlotProperties.background_color)
        self.axes.tick_params(axis='x', colors=PlotProperties.primary_color)
        self.axes.tick_params(axis='y', colors=PlotProperties.primary_color)

        self.axes.spines['left'].set_visible(True)

        self.axes.spines['bottom'].set_visible(True)
        self.axes.spines['bottom'].set_position('zero')

        self.axes.spines['right'].set_visible(False)
        self.axes.spines['top'].set_visible(False)

        tick_values = [1.0, db_to_lin(-3), db_to_lin(-9)]
        tick_labels = ['0dB', '-3dB', '-9dB']

        tick_values += [-v for v in tick_values]
        tick_labels += tick_labels

        self.axes.set_yticks(tick_values)
        self.axes.set_yticklabels(tick_labels)

        self.axes.set_ylim(-1, 1)

        fig.tight_layout()

        super().__init__(fig)