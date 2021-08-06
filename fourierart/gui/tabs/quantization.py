from fourierart.utility import time_func
from fourierart import ApplicationSettings, Parameter, Choice, db_to_lin
from fourierart.gui.primitives.callback import Callback
from fourierart.gui.components import CustomSlider, CustomChoice, CustomTab
from fourierart.gui.plots.quantization import QuantizationPlot

import numpy as np

class Quantization(CustomTab):
    def __init__(self, 
            completion_callback: Callback = Callback()):

        super().__init__(completion_callback=completion_callback)

        self.spline = None
        self.audio_file = None

        self.parameters = {
            'gain': Parameter(
                min=ApplicationSettings.qu_gain_min, 
                max=ApplicationSettings.qu_gain_max, 
                value=0, 
                step=0.1, 
                hard_min=True, 
                hard_max=False, 
                format=lambda v: f'{v:.1f} dB'
            ),

            'time_step': Parameter(
                min=0, 
                max=1, 
                value=0, 
                step=1, 
                hard_min=True, 
                hard_max=True, 
                format= lambda v: f'{v*1000:.1f} ms'
            ),

            'normalization': Choice({'Max': 'max', 'Peak': 'peak'}),

            'bar_method': Choice({'Max': np.max, 'Min': np.min, 'Average': np.average, 'Median': np.median}),
        }

        self.plot = QuantizationPlot()
        self.graph_layout.addWidget(self.plot)

        # Options
        self.gain = CustomSlider('Gain', self.parameters['gain'])
        self.gain.connect(self.update_graph)
        self.options_layout.addWidget(self.gain, 0, 0, 1, 2)

        self.time_step = CustomSlider('Bar width', self.parameters['time_step'], 'exp')
        self.time_step.connect(self.update_graph)
        self.options_layout.addWidget(self.time_step, 0, 2, 1, 2)

        self.normalization_type = CustomChoice('Normalization', self.parameters['normalization'])
        self.normalization_type.connect(self.update_graph)
        self.options_layout.addWidget(self.normalization_type, 1, 0)

        self.bar_method = CustomChoice('Bar Method', self.parameters['bar_method'])
        self.bar_method.connect(self.update_graph)
        self.options_layout.addWidget(self.bar_method, 1, 1)

    def set_audio_file(self, audio_file):
        if self.audio_file != audio_file:
            self.audio_file = audio_file

            slider_steps = ApplicationSettings.qu_time_step_slider_steps
            time_step_min = audio_file.t / (ApplicationSettings.qu_max_bars + 1)
            time_step_max = audio_file.t / (ApplicationSettings.qu_min_bars + 1)

            time_step_value = ApplicationSettings.qu_time_step_default
            time_step_value = np.clip(time_step_value, time_step_min, time_step_max)

            self.parameters['time_step'].min = time_step_min
            self.parameters['time_step'].max = time_step_max
            self.parameters['time_step'].step = (time_step_max - time_step_min) / slider_steps 
            self.parameters['time_step'].set(time_step_value)

            self.time_step.set_parameter(self.parameters['time_step'])

        self.update_graph()

    def update_graph(self):
        self.spline = time_func(self.plot.set_data, 
            audio_file = self.audio_file,
            gain = db_to_lin(self.parameters['gain'].get()),
            time_step = self.parameters['time_step'].get(),
            normalization=self.parameters['normalization'].get(),
            bar_method=self.parameters['bar_method'].get(),
        )

        self.completion_callback()