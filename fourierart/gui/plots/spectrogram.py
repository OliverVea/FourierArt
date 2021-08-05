from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt

from fourierart.gui.plots.plot_properties import PlotProperties
from fourierart.audio_processing import WindowFunction, get_spectrogram

import numpy as np

class SpectrogramPlot(FigureCanvasQTAgg):
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

        self.cmap = plt.get_cmap('plasma')

        fig.tight_layout()
        super(SpectrogramPlot, self).__init__(fig)

        self.audio_segment = None

    def on_update(self, audio_segment, 
            freq_min: float = 20, 
            freq_max: float = 8000, 
            norm: str = 'none', 
            freq_window_size: int = 1024, 
            freq_step_size: int = 32, 
            window_function: int = WindowFunction.Hanning):

        if not self.audio_segment or self.audio_segment.dBFS != audio_segment.dBFS or self.audio_segment.duration_seconds != audio_segment.duration_seconds:
            self.audio_segment = audio_segment

            self.update_spectrogram(
                audio_segment,
                freq_window_size = freq_window_size, 
                freq_step_size   = freq_step_size,
                window_function  = window_function
            )
            
        self.redraw(
            duration = audio_segment.duration_seconds,
            fs       = audio_segment.frame_rate,
            freq_min = freq_min,
            freq_max = freq_max,
            norm     = norm
        )

    def update_spectrogram(self, audio_segment, freq_window_size: int, freq_step_size: int, window_function: int):
        audio = np.array(audio_segment.get_array_of_samples())
        audio = np.divide(audio, np.max(audio))

        self.spectrogram, *_ = get_spectrogram(audio, freq_window_size, window_function, step_size=freq_step_size)
        self.spectrogram = self.spectrogram.T

    def redraw(self, duration, fs, freq_min, freq_max, norm):
        w = duration
        h = fs / 2

        y0, y1 = freq_min / h, freq_max / h 
        y0_rasterized = int(y0 * self.spectrogram.shape[1])
        y1_rasterized = int(np.ceil(y1 * self.spectrogram.shape[1]))

        y0 = h * y0_rasterized / self.spectrogram.shape[1]
        y1 = h * y1_rasterized / self.spectrogram.shape[1]

        spectrogram = self.spectrogram[:,y0_rasterized:y1_rasterized]

        self.axes.set_xlim(0, w)
        self.axes.set_ylim(y0, y1)

        if norm == 'log':
            norm = LogNorm()

        else:
            norm = None

        extent = [
            0, w, 
            y1, y0
        ]

        self.axes.imshow(
            spectrogram, 
            cmap=self.cmap, 
            norm=norm, 
            interpolation='none', 
            extent=extent, 
            aspect='auto'
        )

        self.draw()
