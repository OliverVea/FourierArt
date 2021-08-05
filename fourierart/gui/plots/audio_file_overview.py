from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np

from fourierart.gui.plots.plot_properties import PlotProperties
from fourierart.utility import db_to_lin
from fourierart.audio_file import AudioFile

class AudioFileOverview(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, edgecolor=PlotProperties.primary_color, facecolor=PlotProperties.background_color)
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

        #xticks = self.axes.xaxis.get_major_ticks() 
        #xticks[0].label1.set_visible(False)

        self.axes.set_ylim(-1, 1)

        self.lines = self.axes.plot([], [], color=PlotProperties.accent_color, zorder=-1)

        fig.tight_layout()
        super(AudioFileOverview, self).__init__(fig)

    def set_audio(self, audio_file: AudioFile, start: float = 0, end: int = 1): 
        x, y = audio_file.get_time_amplitudes(start, end)

        self.axes.set_xlim(np.min(x), np.max(x))

        self.lines[0].set_data(x, y)
        self.draw()