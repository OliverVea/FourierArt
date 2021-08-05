from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from fourierart.gui.plots.plot_properties import PlotProperties
from fourierart.utility import db_to_lin

import numpy as np
from scipy.interpolate import CubicSpline

class WaveformPlot(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, n_bars=1000):
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

        self.axes.set_ylim(-1, 1)

        self.spline_top = self.axes.plot([], [], color=PlotProperties.primary_color, zorder=-1)[0]
        self.spline_bottom = self.axes.plot([], [], color=PlotProperties.primary_color, zorder=-1)[0]

        self.bars = self.axes.bar([0 for i in range(n_bars)], [0 for i in range(n_bars)], color=PlotProperties.accent_color, zorder=-2)

        fig.tight_layout()
        super(WaveformPlot, self).__init__(fig)

    def set_data(self, audio_file, gain: float = 1, time_step: float = 0.02, normalization: str = 'max', bar_method = np.max, spline_points: int = 1000): 
        audio = audio_file.as_array(normalization=normalization)
        audio = np.abs(audio)
        audio = np.multiply(audio, gain)
        audio = np.clip(audio, 0, 1.0)

        iter = range(int(audio_file.t / time_step))

        bin_time = [i * time_step for i in iter]

        bin_slices = [(int(t * audio_file.fs), int((t + time_step) * audio_file.fs)) for t in bin_time]

        bin_amplitudes = [bar_method(audio[a:b]) for a, b in bin_slices]

        n = len(bin_time)

        self.axes.set_xlim(np.min(bin_time), np.max(bin_time))

        for i, bar in enumerate(self.bars):
            if i < n:
                bar.set_height(bin_amplitudes[i]*2)
                bar.set_x(bin_time[i])
                bar.set_width(time_step*0.75)
                bar.set_y(-bin_amplitudes[i])

            else:
                bar.set_height(0)
                bar.set_width(0)
        
        # Spline stuff
        spline = CubicSpline(bin_time, bin_amplitudes)
        
        spline_xs = [audio_file.t * i / (spline_points - 1) for i in range(spline_points)]
        spline_ys = spline([v - 0.5 * time_step for v in spline_xs])

        self.spline_top.set_data(spline_xs, spline_ys)
        self.spline_bottom.set_data(spline_xs, -spline_ys)
            
        self.draw()

        return spline