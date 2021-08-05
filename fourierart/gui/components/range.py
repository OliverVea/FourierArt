from fourierart.gui.primitives.callback import Callback
from fourierart import Range, ParameterInterpolator, Nop
from fourierart.gui.components.field import CustomField

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout
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
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Input field
        self.input_upper = CustomField('')
        self.input_upper.setFixedWidth(input_width)
        self.input_upper.returnPressed.connect(self._on_input_upper_change)
        
        self.layout.addWidget(self.input_upper)

        # Slider
        self.slider = QRangeSlider(Qt.Vertical) # TODO: Implement Horizontal.
        self.slider.sliderMoved.connect(self._on_slider_change)

        self.layout.addWidget(self.slider)

        # Input field
        self.input_lower = CustomField('')
        self.input_lower.setFixedWidth(input_width)
        self.input_lower.returnPressed.connect(self._on_input_lower_change)
        
        self.layout.addWidget(self.input_lower)

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

    def _on_input_upper_change(self):
        print(Exception('Not implemented.'))

        self.callback()

    def _on_input_lower_change(self):
        print(Exception('Not implemented.'))

        self.callback()