from fourierart import Nop, Parameter, ParameterInterpolator
from fourierart.gui.components.field import CustomField

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QSlider


class OptionSlider(QGroupBox):
    def __init__(self, title, parameter: Parameter, interpolator: str = 'lin', interpolator_order: float = 50, input_width: int = 80):
        super().__init__()

        # Initializing attributes
        self.interpolator = ParameterInterpolator(parameter, interpolator, interpolator_order)
        self.callback = Nop # CustomRange and CustomSlider do not pass the value on callback. This has to be read from CustomRange.range or CustomSlider.parameter.

        # Layout
        self.setTitle(title)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Slider
        self.slider = QSlider(Qt.Horizontal) # TODO: Implement Vertical.
        slider_value = self.convert_to_slider_value(self.p.get())
        self.update_parameter(slider_value)
        self.slider.sliderMoved.connect(self.on_slider_change)

        self.layout.addWidget(self.slider)

        # Input field
        self.input = CustomField('')
        self.input.setFixedWidth(input_width)
        self.input.returnPressed.connect(self.on_input_change)
        self.layout.addWidget(self.input)


    def on_slider_change(self, value):
        value = self.convert_slider_value(value)
        self.p.set(value)
        self.input.setText(self.p.format(self.p.get()))

        self.callback()
    
    def on_input_change(self):
        try:
            value = float(self.input.text())
            slider_value = self.convert_to_slider_value(value)

            self.slider.setValue(slider_value)

            self.callback(value)

        except Exception as e:
            print(e)

        self.input.setText(self.p.format(self.p.get()))
        self.input.clearFocus()