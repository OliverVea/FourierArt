from fourierart import Parameter
from fourierart.gui.components import CustomTab, CustomRange
from fourierart.gui.plots.spectrogram import SpectrogramPlot

import numpy as np
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QWidget

class Spectrogram(CustomTab):
    def __init__(self):
        super().__init__()
        
        self.parameters = {
            'frequency': Parameter(min=0, max=1, value=(0,1), step=1, hard_min=True, hard_max=True, format=lambda v: f'{v[0]:.1f} Hz'),
        }

        # Plot
        self.plot = SpectrogramPlot()
        self.graph_layout.addWidget(self.plot)

        # Frequency slider
        self.frequency_slider = CustomRange('Frequency Band', self.parameters['frequency'], interpolator_type='log')

    def set_audio_segment(self, audio_file):
        if self.audio_file == None or audio_file.path != self.audio_file.path or audio_file.t != self.audio_file.t:
            self.audio_file = audio_file

            self.parameters['frequency'].min = 0
            self.parameters['frequency'].max = audio_file.fs / 2
            self.parameters['frequency'].step = (audio_file.fs / 2) / 1000 
            self.parameters['frequency'].value = (20, min(audio_file.fs / 2, 8000))

            a = self.time_step_slider.convert_to_slider_value(20)
            b = self.time_step_slider.convert_to_slider_value(min(audio_file.fs / 2, 8000))
            self.time_step_slider.update_parameter((a, b))

        self.plot.on_update(audio_file)