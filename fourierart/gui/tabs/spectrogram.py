from fourierart import Parameter, ApplicationSettings
from fourierart.gui.components import CustomTab, CustomRange
from fourierart.gui.plots.spectrogram import SpectrogramPlot

class Spectrogram(CustomTab):
    def __init__(self):
        super().__init__()
        
        self.audio_file = None
        self.parameters = {
            'frequency': Parameter(min=0, max=1, value=(0,1), step=1, hard_min=True, hard_max=True, format=lambda v: f'{v[0]:.1f} Hz'),
        }

        # Plot
        self.plot = SpectrogramPlot()
        self.graph_layout.addWidget(self.plot)

        # Frequency slider
        self.frequency_slider = CustomRange('Frequency Band', self.parameters['frequency'], interpolator_type='log')
        self.options_layout.addWidget(self.frequency_slider, 0, 0)

    def set_audio_file(self, audio_file):
        if self.audio_file != audio_file:
            self.audio_file = audio_file

            f_min = ApplicationSettings.sg_default_f_min
            f_max = ApplicationSettings.sg_default_f_max
            slider_steps = ApplicationSettings.sg_frequency_slider_steps

            f_max = min(f_max, audio_file.fs / 2)

            self.parameters['frequency'].min = 0
            self.parameters['frequency'].max = audio_file.fs / 2
            self.parameters['frequency'].step = audio_file.fs / (2 * slider_steps) 
            self.parameters['frequency'].value = (f_min, f_max)

            self.frequency_slider.set_range(self.parameters['frequency'])

        self.plot.on_update(audio_file)