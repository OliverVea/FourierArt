from fourierart.gui.primitives.callback import Callback
from fourierart import Nop, Parameter, ParameterInterpolator, to_float
from fourierart.gui.components.field import CustomField

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QSlider

class CustomSlider(QGroupBox):
    def __init__(self, title, parameter: Parameter, interpolator: str = 'lin', interpolator_order: float = 50, input_width: int = 80):
        super().__init__()

        # Initializing attributes
        self.interpolator = ParameterInterpolator(parameter, interpolator, interpolator_order)
        self.callback = Callback() # CustomRange and CustomSlider do not pass the value on callback. This has to be read from CustomRange.range or CustomSlider.parameter.

        # Layout
        self.setTitle(title)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Slider
        self.slider = QSlider(Qt.Horizontal) # TODO: Implement Vertical.
        self.slider.sliderMoved.connect(self._on_slider_change)

        self.layout.addWidget(self.slider)

        # Input field
        self.input = CustomField('')
        self.input.setFixedWidth(input_width)
        self.input.returnPressed.connect(self._on_input_change)
        
        self.layout.addWidget(self.input)

    def connect(self, callback):
        self.callback.register(callback)

    def set_parameter(self, parameter):
        self.p = parameter

        value = self.p.get()
        slider_value = self.interpolator.to_slider(value)
        self.slider.setValue(slider_value)

    def _set_input_text(self, value):
        input_text = self.p.format(value)
        self.input.setText(input_text)

    def _on_slider_change(self, value):
        value = self.interpolator.from_slider(value) # Convert from slider space.
        value = self.p.set(value) # Set value and return resulting value which might be 
        
        self._set_input_text(value)

        self.callback()
    
    def _on_input_change(self):
        value = to_float(self.input.text())

        if value: # If valid value was entered.
            value = self.p.set(value)
            slider_value = self.interpolator.to_slider(value)
            self.slider.setValue(slider_value)
            self.callback()

        self._set_input_text(self.p.get())
        self.input.clearFocus()
