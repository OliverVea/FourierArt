from fourierart.gui.primitives import *

from fourierart.utility import *
from fourierart.audio.audio_file import AudioFile
from fourierart.audio.processing import WindowFunction, Filter, get_spectrogram

import matplotlib
matplotlib.use('Qt5Agg')
matplotlib.rc('axes',edgecolor='w')

class PlotProperties:
    background_color = (53/255, 53/255, 53/255)
    primary_color = 'white'
    accent_color = 'orange'

class ApplicationSettings:

    # Quantization
    qu_gain_min: float = -40
    qu_gain_max: float = 40
    qu_gain_step: float = 0.1

    #qu_time_step_min: float = 0.001
    qu_time_step_default: float = 0.02
    qu_time_step_slider_steps: int = 1000

    qu_min_bars: int = 5
    qu_max_bars: int = 1000
    qu_spline_points: int = 1000
    qu_bar_width: float = 0.75

    # Spectrogram:
    sg_cmap_name = 'plasma'

    sg_default_f_min = 20
    sg_default_f_max = 8000
    sg_frequency_slider_steps = 1000

    sg_default_norm = 'none'
    sg_default_window_size = 1024
    sg_default_step_size = 64
    sg_default_window_function = WindowFunction.Hanning

class Palette:
    dark = QPalette()
    dark.setColor(QPalette.Window, QColor(53, 53, 53))
    dark.setColor(QPalette.WindowText, Qt.white)
    dark.setColor(QPalette.Base, QColor(25, 25, 25))
    dark.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark.setColor(QPalette.ToolTipBase, Qt.black)
    dark.setColor(QPalette.ToolTipText, Qt.white)
    dark.setColor(QPalette.Text, Qt.white)
    dark.setColor(QPalette.Button, QColor(53, 53, 53))
    dark.setColor(QPalette.ButtonText, Qt.white)
    dark.setColor(QPalette.BrightText, Qt.red)
    dark.setColor(QPalette.Link, QColor(42, 130, 218))
    dark.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark.setColor(QPalette.HighlightedText, Qt.black)