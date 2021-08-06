from fourierart.utility import to_float
from fourierart.gui.primitives.callback import Callback
from fourierart import Range, ParameterInterpolator, Nop
from fourierart.gui.components.field import CustomField

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QSizePolicy, QSpacerItem, QVBoxLayout
from qtrangeslider import QRangeSlider

class CustomRange(QGroupBox):
    def __init__(self, title, range: Range, interpolator_type: str = 'lin', interpolator_order: float = 50, field_width: int = 80):
        super().__init__()

        # Initializing attributes
        self.interpolator_type = interpolator_type
        self.interpolator_order = interpolator_order
        self.callback = Callback() # CustomRange and CustomSlider do not pass the value on callback. This has to be read from CustomRange.range or CustomSlider.parameter.

        # Layout
        self.setTitle(title)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)

        # Slider
        self.slider = QRangeSlider(Qt.Vertical) # TODO: Implement Horizontal.
        self.slider.setMinimumHeight(140)
        self.slider.sliderMoved.connect(self._on_slider_change)

        self.layout.addWidget(self.slider)

        # Field layout
        self.field_layout = QVBoxLayout()
        self.field_layout.expandingDirections()
        self.layout.addLayout(self.field_layout)

        # Upper field
        self.field_upper = CustomField('')
        self.field_upper.setFixedWidth(field_width)
        self.field_upper.returnPressed.connect(self._on_field_upper_change)
        
        self.field_layout.addWidget(self.field_upper, alignment=Qt.AlignmentFlag.AlignTop)

        # Lower field
        self.field_lower = CustomField('')
        self.field_lower.setFixedWidth(field_width)
        self.field_lower.returnPressed.connect(self._on_field_lower_change)
        
        self.field_layout.addWidget(self.field_lower, alignment=Qt.AlignmentFlag.AlignBottom)

        # Update range, interpolator and UI elements.
        self.set_range(range)

    def connect(self, callback):
        self.callback.register(callback)

    def set_range(self, range):
        self.range = range
        self.interpolator = ParameterInterpolator(range, self.interpolator_type, self.interpolator_order)

        value = self.range.get()
        max_slider_value = self.interpolator.slider_max()
        lower_slider_value = self.interpolator.to_slider(value[0])
        upper_slider_value = self.interpolator.to_slider(value[1])

        self.slider.setMaximum(max_slider_value)
        self.slider.setValue((lower_slider_value, upper_slider_value))

        self._set_field_text(value)

    def _set_field_text(self, value: tuple):
        field_lower_text = self.range.format(value[0])
        field_upper_text = self.range.format(value[1])

        self.field_lower.setText(field_lower_text)
        self.field_upper.setText(field_upper_text)

    def _on_slider_change(self, slider_value):
        value = tuple(self.interpolator.from_slider(v) for v in slider_value)
        value = self.range.set(value)

        self._set_field_text(value)

        self.callback()

    def _on_field_upper_change(self):
        value = to_float(self.field_upper.text())

        if not value is None and value > self.range.get()[0]: # If valid value was entered - apparently 0.0 is false, so value has to be compared to none.        
            range = (self.range.get()[0], value)
            range = self.range.set(range)

            slider_value = self.interpolator.to_slider(range[1])
            self.slider.setValue((self.slider.value()[0], slider_value))

            self.callback()

        self._set_field_text(self.range.get())
        self.field_upper.clearFocus()

    def _on_field_lower_change(self):
        value = to_float(self.field_lower.text())

        if not value is None and value < self.range.get()[1]: # If valid value was entered - apparently 0.0 is false, so value has to be compared to none.        
            range = (value, self.range.get()[1])
            range = self.range.set(range)

            slider_value = self.interpolator.to_slider(range[0])
            self.slider.setValue((slider_value, self.slider.value()[1]))
            
            self.callback()

        self._set_field_text(self.range.get())
        self.field_lower.clearFocus()