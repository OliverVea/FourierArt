from fourierart.gui.primitives.callback import Callback
from fourierart import Nop, Parameter, ParameterInterpolator, to_float
from fourierart.gui.components.field import CustomField

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QSlider

class CustomSlider(QGroupBox):
    def __init__(self, title, parameter: Parameter, interpolator_type: str = 'lin', interpolator_order: float = 50, input_width: int = 80):
        super().__init__()

        # Initializing attributes
        self.interpolator_type = interpolator_type
        self.interpolator_order = interpolator_order
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

        # Update parameter, interpolator and UI elements.
        self.set_parameter(parameter)

    def connect(self, callback):
        self.callback.register(callback)

    def set_parameter(self, parameter):
        self.parameter = parameter
        self.interpolator = ParameterInterpolator(parameter, self.interpolator_type, self.interpolator_order)

        value = self.parameter.get()
        slider_value = self.interpolator.to_slider(value)
        slider_max = self.interpolator.slider_max()

        self.slider.setMaximum(slider_max)
        self.slider.setValue(slider_value)
        self._set_input_text(value)

    def _set_input_text(self, value):
        input_text = self.parameter.format(value)
        self.input.setText(input_text)

    def _on_slider_change(self, value):
        value = self.interpolator.from_slider(value) # Convert from slider space.
        value = self.parameter.set(value) # Set value and return resulting value which might be 
        
        self._set_input_text(value)

        self.callback()
    
    def _on_input_change(self):
        value = to_float(self.input.text())

        if not value is None: # If valid value was entered - apparently 0.0 is false, so value has to be compared to none.
            value = self.parameter.set(value)
            slider_value = self.interpolator.to_slider(value)
            self.slider.setValue(slider_value)
            self.callback()

        self._set_input_text(self.parameter.get())
        self.input.clearFocus()
