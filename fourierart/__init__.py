from fourierart.gui.primitives import *
from fourierart.gui.plots import PlotProperties

from fourierart.utility import *
from fourierart.audio.audio_file import AudioFile
from fourierart.audio.processing import WindowFunction, Filter, get_spectrogram

class ApplicationSettings:

    # Quantization
    qu_gain_min: float = -40
    qu_gain_max: float = 40
    qu_gain_step: float = 0.1

    qu_time_step_min: float = 0.001
    qu_time_step_default: float = 0.02
    qu_time_step_slider_steps: int = 1000

    qu_min_bars: int = 5

    # Spectrogram:
    sg_cmap_name = 'plasma'

    sg_default_f_min = 20
    sg_default_f_max = 8000
    sg_frequency_slider_steps = 1000

    sg_default_norm = 'none'
    sg_default_window_size = 1024
    sg_default_step_size = 64
    sg_default_window_function = WindowFunction.Hanning