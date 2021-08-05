import numpy as np
from fourierart.gui.primitives import Parameter, QCustomRange

from fourierart.gui.plots.spectrogram import SpectrogramPlot
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QWidget

class Spectrogram(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        
        self.parameters = {
            'frequency': Parameter(min=0, max=1, value=(0,1), step=1, hard_min=True, hard_max=True, format=lambda v: f'{v[0]:.1f} Hz'),
        }

        # Main layout
        self.layout = QVBoxLayout()

        # Plot
        self.plot = SpectrogramPlot()
        self.layout.addWidget(self.plot)

        # Options
        self.options_layout = QGridLayout()

        # Frequency slider
        self.frequency_slider = QCustomRange('Frequency Band', self.parameters['frequency'], interpolator='log')
        #self.frequency_slider.connect(lambda v: )

        self.setLayout(self.layout)

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