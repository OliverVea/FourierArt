from fourierart import PlotProperties, ApplicationSettings, get_spectrogram

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
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

        self.cmap = plt.get_cmap(ApplicationSettings.sg_cmap_name)

        fig.tight_layout()
        super(SpectrogramPlot, self).__init__(fig)

        self.audio_file = None

    def on_update(self, audio_file, 
            freq_min: float = ApplicationSettings.sg_default_f_min, 
            freq_max: float = ApplicationSettings.sg_default_f_max, 
            norm: str = ApplicationSettings.sg_default_norm, 
            window_size: int = ApplicationSettings.sg_default_window_size, 
            step_size: int = ApplicationSettings.sg_default_step_size, 
            window_function: int = ApplicationSettings.sg_default_window_function):

        if self.audio_file != audio_file:
            self.audio_file = audio_file

            self.update_spectrogram(
                audio_file,
                window_size     = window_size, 
                step_size       = step_size,
                window_function = window_function
            )
            
        self.redraw(
            duration = audio_file.t,
            fs       = audio_file.fs,
            freq_min = freq_min,
            freq_max = freq_max,
            norm     = norm
        )

    def update_spectrogram(self, audio_file, window_size: int, step_size: int, window_function: int):
        audio = audio_file.get_amplitudes()

        self.spectrogram, *_ = get_spectrogram(audio, window_size, window_function, step_size=step_size)
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
