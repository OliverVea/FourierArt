from fourierart import Parameter, ParameterInterpolator
from fourierart.gui.components.field import CustomField

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QSlider

class OptionSlider(QGroupBox):
    def __init__(self, title, parameter: Parameter, interpolator: str = 'lin', interpolator_order: float = 50):
        super().__init__()

        self.interpolator = ParameterInterpolator(parameter, interpolator, interpolator_order)

        self.setTitle(title)

        self.input = CustomField('')
        self.input.setFixedWidth(80)

        self.input.returnPressed.connect(self.on_input_change)

        self.slider = QSlider(Qt.Horizontal)
        slider_value = self.convert_to_slider_value(self.p.get())
        self.update_parameter(slider_value)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.input)
        self.setLayout(self.layout)

        self.slider.sliderMoved.connect(self.on_slider_change)

    def callback(self, value):
        for fn in self.callbacks:
            fn(value)

    def on_slider_change(self, value):
        value = self.convert_slider_value(value)
        self.callback(value)
        self.input.setText(self.p.format(self.p.get()))
    
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