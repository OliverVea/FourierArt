from fourierart.audio.processing import WindowFunction
from fourierart.gui.components.choice import CustomChoice
from fourierart.gui.components.slider import CustomSlider
from fourierart.gui.primitives.choice import Choice
from fourierart.gui.primitives.range import Range
from fourierart import Parameter, ApplicationSettings
from fourierart.gui.components import CustomTab, CustomRange
from fourierart.gui.plots.spectrogram import SpectrogramPlot

class Spectrogram(CustomTab):
    def __init__(self):
        super().__init__()
        
        self.audio_file = None
        self.parameters = {
            'frequency': Range(
                min=0, 
                max=1, 
                value=(0, 1), 
                step=1, 
                hard_min=True, 
                hard_max=True,
                 format=lambda v: f'{v:.1f} Hz'),

            'norm': Choice({'None': None, 'Log': 'log'}),

            'window_size': Parameter(
                min = ApplicationSettings.sg_window_size_min,
                max = ApplicationSettings.sg_window_size_max,
                step = (ApplicationSettings.sg_window_size_max - ApplicationSettings.sg_window_size_min) / ApplicationSettings.sg_window_size_steps,
                value = ApplicationSettings.sg_window_size_default,
                format = lambda v: f'{v}',
                dtype = int
            ),

            'step_size': Parameter(
                min = ApplicationSettings.sg_step_size_min,
                max = ApplicationSettings.sg_step_size_max,
                step = (ApplicationSettings.sg_step_size_max - ApplicationSettings.sg_step_size_min) / ApplicationSettings.sg_step_size_steps,
                value = ApplicationSettings.sg_step_size_default,
                format = lambda v: f'{v}',
                dtype = int
            ),

            'window_function': Choice({
                'None': None, 
                'Bartlett': WindowFunction.Bartlett, 
                'Blackman': WindowFunction.Blackman, 
                'Hamming': WindowFunction.Hamming, 
                'Hanning': WindowFunction.Hanning, 
                'Kaiser': WindowFunction.Kaiser,}),

            'interpolation': Choice({
                'Bicubic': 'bicubic', 
                'Bilinear': 'bilinear',
                'Nearest': 'nearest', 
                'Spline16': 'spline16', 
                'sinc': 'sinc', 
                'Catmull-Rom': 'catrom'})
        }

        # Plot
        self.plot = SpectrogramPlot()
        self.graph_layout.addWidget(self.plot)

        # Frequency slider
        self.frequency_slider = CustomRange('Frequency Band', self.parameters['frequency'], interpolator_type='exp')
        self.frequency_slider.connect(self.on_update)
        self.options_layout.addWidget(self.frequency_slider, 0, 0, 2, 1)

        # FFT Window size slider
        self.window_size_slider = CustomSlider('Window Size', self.parameters['window_size'], interpolator_type='exp')
        self.window_size_slider.connect(self.on_update)
        self.options_layout.addWidget(self.window_size_slider, 0, 1, 1, 3)

        # Step size slider
        self.step_size_slider = CustomSlider('Step Size', self.parameters['step_size'], interpolator_type='exp')
        self.step_size_slider.connect(self.on_update)
        self.options_layout.addWidget(self.step_size_slider, 1, 1, 1, 3)

        # Norm choice
        self.norm_choice = CustomChoice('Normalization', self.parameters['norm'])
        self.norm_choice.connect(self.on_update)
        self.options_layout.addWidget(self.norm_choice, 2, 1)

        # Norm choice
        self.window_function_choice = CustomChoice('Window Function', self.parameters['window_function'])
        self.window_function_choice.connect(self.on_update)
        self.options_layout.addWidget(self.window_function_choice, 2, 2)

        # Norm choice
        self.interpolation_choice = CustomChoice('Interpolation', self.parameters['interpolation'])
        self.interpolation_choice.connect(self.on_update)
        self.options_layout.addWidget(self.interpolation_choice, 2, 3)


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

            self.on_update()

    def on_update(self):
        self.plot.on_update(self.audio_file,
            freq_min = self.parameters['frequency'].get()[0],
            freq_max = self.parameters['frequency'].get()[1],
            window_size = self.parameters['window_size'].get(),
            step_size = self.parameters['step_size'].get(),
            norm = self.parameters['norm'].get(),
            window_function = self.parameters['window_function'].get(),
            interpolation = self.parameters['interpolation'].get(),
        )