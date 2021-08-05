from fourierart import Range, ParameterInterpolator
from fourierart.gui.components.field import CustomField

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout
from qtrangeslider import QRangeSlider

class CustomRange(QGroupBox):
    def __init__(self, title, range: Range, interpolator: str = 'lin', interpolator_order: float = 50):
        super().__init__()

        self.interpolator = ParameterInterpolator(parameter=range, interpolator=interpolator, interpolator_order=interpolator_order)

        self.setTitle(title)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Slider
        self.slider = QRangeSlider(Qt.Vertical)
        slider_value = tuple(self.interpolator.to_slider(v) for v in self.p.get())
        self.update_parameter(slider_value)
        self.slider.sliderMoved.connect(self.on_slider_change)

        self.layout.addWidget(self.slider)

        # Input field
        self.input = CustomField('')
        self.input.setFixedWidth(80)
        self.input.returnPressed.connect(self.on_input_change)
        self.layout.addWidget(self.input)

    def callback(self, value):
        raise Exception('Not implemented.')

    def on_slider_change(self, value):
        raise Exception('Not implemented.')

    def on_input_change(self):
        raise Exception('Not implemented.')