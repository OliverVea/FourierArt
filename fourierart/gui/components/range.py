from fourierart.gui.primitives.callback import Callback
from fourierart import Range, ParameterInterpolator, Nop
from fourierart.gui.components.field import CustomField

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout
from qtrangeslider import QRangeSlider

class CustomRange(QGroupBox):
    def __init__(self, title, range: Range, interpolator_type: str = 'lin', interpolator_order: float = 50, input_width: int = 80):
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
        self.slider = QRangeSlider(Qt.Vertical) # TODO: Implement Horizontal.
        self.slider.sliderMoved.connect(self._on_slider_change)

        self.layout.addWidget(self.slider)

        # Input field
        self.input = CustomField('')
        self.input.setFixedWidth(input_width)
        self.input.returnPressed.connect(self._on_input_change)
        
        self.layout.addWidget(self.input)

        # Update range, interpolator and UI elements.
        self.set_range(range)

    def set_range(self, range):
        self.range = range
        self.interpolator = ParameterInterpolator(range, self.interpolator_type, self.interpolator_order)

        # TODO: Update UI elements
        print(Exception('UI not updated!'))

    def _on_slider_change(self, value):
        print(Exception('Not implemented.'))

        self.callback()

    def _on_input_change(self):
        print(Exception('Not implemented.'))

        self.callback()