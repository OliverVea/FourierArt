from fourierart.gui.plots.waveform import WaveformPlot
from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtCore import Qt

from fourierart.gui.primitives import QOptionChoice, QOptionSlider, Parameter
from fourierart.utility import db_to_lin

import numpy as np

class Waveform(QWidget):
    def update_parameter(self, name, value):
        if type(self.parameters[name]) == Parameter:
            self.parameters[name].set(value)

        else:
            self.parameters[name] = value

        self.set_data()

    def __init__(self, enable_tab):
        super(QWidget, self).__init__()

        self.spline = None
        self.enable_tab = enable_tab
        self.audio_file = None

        self.parameters = {
            'gain': Parameter(min=-30, max=30, value=0, step=0.1, hard_min=True, hard_max=False, format=lambda v: f'{v:.1f} dB'),
            'time_step': Parameter(min=0, max=1, value=0, step=1, hard_min=True, hard_max=True, format= lambda v: f'{v*1000:.1f} ms'),
            'bar_method': np.max,
            'normalization': 'max'
        }

        self.main_layout = QVBoxLayout()

        self.waveform_plot = WaveformPlot()

        self.main_layout.addWidget(self.waveform_plot, 1)

        # Options

        self.options_layout = QGridLayout()

        self.filter_tab = QTabWidget()

        self.tab_none_layout = QWidget()
        self.filter_tab.addTab(self.tab_none_layout, 'None')

        self.gain_slider = QOptionSlider('Gain', self.parameters['gain'])
        self.gain_slider.connect(lambda value: self.update_parameter('gain', value))

        self.time_step_slider = QOptionSlider('Bar width', self.parameters['time_step'], 'exp')
        self.time_step_slider.connect(lambda value: self.update_parameter('time_step', value))

        self.normalization_type = QOptionChoice('Normalization', {'Max': 'max', 'Peak': 'peak'})
        self.normalization_type.connect(lambda value: self.update_parameter('normalization', value))

        self.bar_method = QOptionChoice('Bar Method', {'Max': np.max, 'Min': np.min, 'Average': np.average, 'Median': np.median})
        self.bar_method.connect(lambda value: self.update_parameter('bar_method', value))

        self.options_layout.addWidget(self.gain_slider, 0, 0, 1, 2)
        self.options_layout.addWidget(self.time_step_slider, 0, 2, 1, 2)
        self.options_layout.addWidget(self.filter_tab, 0, 4, 3, 2)
        self.options_layout.addWidget(self.normalization_type, 1, 0)
        self.options_layout.addWidget(self.bar_method, 1, 1)

        self.main_layout.addLayout(self.options_layout)

        self.setLayout(self.main_layout)

    def set_audio(self, audio_file):
        if self.audio_file == None or audio_file.path != self.audio_file.path or audio_file.t != self.audio_file.t:
            self.audio_file = audio_file

            self.parameters['time_step'].min = 0.001
            self.parameters['time_step'].max = audio_file.t / 5
            self.parameters['time_step'].step = (audio_file.t / 5 - 0.001) / 1000 
            self.parameters['time_step'].value = 0.02

            slider_value = self.time_step_slider.convert_to_slider_value(0.02)
            self.time_step_slider.update_parameter(slider_value)

        self.set_data()

    def set_data(self):
        self.spline = self.waveform_plot.set_data(
            audio_file = self.audio_file,
            gain = db_to_lin(self.parameters['gain'].get()),
            time_step = self.parameters['time_step'].get(),
            normalization=self.parameters['normalization'],
            bar_method=self.parameters['bar_method']
        )

        self.enable_tab()