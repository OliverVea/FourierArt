from fourierart import Parameter, Choice, Nop, db_to_lin
from fourierart.gui.components import CustomSlider, CustomChoice, CustomTab
from fourierart.gui.plots.waveform import WaveformPlot

import numpy as np

class Waveform(CustomTab):

    def __init__(self, completion_callback = Nop, time_step_min: float = 0.001, time_step_default: float = 0.02):
        super().__init__(completion_callback=completion_callback)

        self.spline = None
        self.audio_file = None
        self.time_step_default = time_step_default

        self.parameters = {
            'gain': Parameter(min=-30, max=30, value=0, step=0.1, hard_min=True, hard_max=False, format=lambda v: f'{v:.1f} dB'),
            'time_step': Parameter(min=time_step_min, max=1, value=0, step=1, hard_min=True, hard_max=True, format= lambda v: f'{v*1000:.1f} ms'),
            'bar_method': np.max,
            'normalization': 'max'
        }

        self.waveform_plot = WaveformPlot()
        self.graph_layout.addWidget(self.waveform_plot)

        # Options
        self.gain = CustomSlider('Gain', self.parameters['gain'])
        self.gain.connect(lambda v: self.set_parameter('gain', v))
        self.options_layout.addWidget(self.gain, 0, 0, 1, 2)

        self.time_step = CustomSlider('Bar width', self.parameters['time_step'], 'exp')
        self.time_step.connect(lambda v: self.set_parameter('time_step', v))
        self.options_layout.addWidget(self.time_step, 0, 2, 1, 2)

        self.normalization_type = CustomChoice(Choice('Normalization', {'Max': 'max', 'Peak': 'peak'}))
        self.normalization_type.connect(lambda v: self.set_parameter('normalization', v))
        self.options_layout.addWidget(self.normalization_type, 1, 0)

        self.bar_method = CustomChoice('Bar Method', {'Max': np.max, 'Min': np.min, 'Average': np.average, 'Median': np.median})
        self.bar_method.connect(lambda v: self.set_parameter('bar_method', v))
        self.options_layout.addWidget(self.bar_method, 1, 1)

    def set_parameter(self, name, value):
        self.parameters[name].set(value)
        self.update_graph()

    def set_audio(self, audio_file):
        if self.audio_file == audio_file:
            self.audio_file = audio_file

            self.parameters['time_step'].max = audio_file.t / 5
            self.parameters['time_step'].step = (audio_file.t / 5 - 0.001) / 1000 
            self.parameters['time_step'].set(self.time_step_default)

            self.time_step.set_parameter(self.parameters['time_step'])

        self.update_graph()

    def update_graph(self):
        self.spline = self.waveform_plot.set_data(
            audio_file = self.audio_file,
            gain = db_to_lin(self.parameters['gain'].get()),
            time_step = self.parameters['time_step'].get(),
            normalization=self.parameters['normalization'],
            bar_method=self.parameters['bar_method']
        )

        self.enable_tab()