from fourierart.utility import time_func
from fourierart import ApplicationSettings, PlotProperties
from fourierart.gui.plots.amplitude_plot import AmplitudePlot

import numpy as np
from scipy.interpolate import CubicSpline

class QuantizationPlot(AmplitudePlot):
    def __init__(self, n_bars=ApplicationSettings.qu_max_bars):
        super().__init__()

        self.spline_top = self.axes.plot([], [], color=PlotProperties.primary_color, zorder=-1)[0]
        self.spline_bottom = self.axes.plot([], [], color=PlotProperties.primary_color, zorder=-1)[0]

        self.bars = self.axes.bar([0 for i in range(n_bars)], [0 for i in range(n_bars)], color=PlotProperties.accent_color, zorder=-2, visible=False)

    def set_data(self, 
            audio_file, 
            gain, 
            time_step, 
            normalization, 
            bar_method, 
            spline_points: int = ApplicationSettings.qu_spline_points): 

        audio = audio_file.get_amplitudes(
            normalization=normalization,
            gain=gain, 
            clip=True, 
            abs=True)

        n_bars = round(audio_file.t / time_step)
        time_step = audio_file.t / n_bars

        bin_time = [i * time_step for i in range(n_bars)]
        bin_slices = [(int(t * audio_file.fs), int((t + time_step) * audio_file.fs)) for t in bin_time]
        bin_amplitudes = [bar_method(audio[a:b]) for a, b in bin_slices]

        self.axes.set_xlim(np.min(bin_time), np.max(bin_time) + time_step)

        bar_width = ApplicationSettings.qu_bar_width
        bar_x_offset = time_step * (1 - bar_width) / 2

        for i, bar in enumerate(self.bars):
            if i < len(bin_time):
                bar.set_visible(True)
                bar.set_height(bin_amplitudes[i] * 2)
                bar.set_x(bin_time[i] + bar_x_offset)
                bar.set_width(time_step * bar_width)
                bar.set_y(-bin_amplitudes[i])

            else:
                if not bar.get_visible():
                    break

                bar.set_visible(False)
                #bar.set_height(0)
                #bar.set_width(0)
        
        # Spline stuff
        spline = CubicSpline(bin_time, bin_amplitudes)
        spline_xs = np.linspace(0, audio_file.t, num=spline_points)
        spline_ys = spline([v - 0.5 * time_step for v in spline_xs])

        self.spline_top.set_data(spline_xs, spline_ys)
        self.spline_bottom.set_data(spline_xs, -spline_ys)
            
        time_func(self.draw) # Is the majority of the time spent.

        return spline