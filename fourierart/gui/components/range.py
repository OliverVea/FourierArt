from fourierart import Range, ParameterInterpolator, Nop
from fourierart.gui.components.field import CustomField

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout
from qtrangeslider import QRangeSlider

class CustomRange(QGroupBox):
    def __init__(self, title, range: Range, interpolator: str = 'lin', interpolator_order: float = 50, input_width: int = 80):
        super().__init__()

        # Initializing attributes
        self.interpolator = ParameterInterpolator(parameter=range, interpolator=interpolator, interpolator_order=interpolator_order)
        self.callback = Callback() # CustomRange and CustomSlider do not pass the value on callback. This has to be read from CustomRange.range or CustomSlider.parameter.

        # Layout
        self.setTitle(title)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Slider
        self.slider = QRangeSlider(Qt.Vertical) # TODO: Implement Horizontal.
        slider_value = tuple(self.interpolator.to_slider(v) for v in self.p.get())
        self.update_parameter(slider_value)
        self.slider.sliderMoved.connect(self._on_slider_change)

        self.layout.addWidget(self.slider)

        # Input field
        self.input = CustomField('')
        self.input.setFixedWidth(input_width)
        self.input.returnPressed.connect(self._on_input_change)
        
        self.layout.addWidget(self.input)


    def _on_slider_change(self, value):
        raise Exception('Not implemented.')

        self.callback()

    def _on_input_change(self):
        raise Exception('Not implemented.')

        self.callback()