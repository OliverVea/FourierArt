from fourierart.gui.primitives.callback import Callback
from fourierart.utility import Nop
from fourierart.gui.primitives import Choice

from PyQt5.QtWidgets import QComboBox, QGroupBox, QHBoxLayout

class CustomChoice(QGroupBox):
    def __init__(self, title, choice: Choice):
        super().__init__()

        self.choice = choice
        self.callback = Callback()

        # Layout
        self.setTitle(title)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Initialize dropdown
        self.dropdown = QComboBox()
        self.dropdown.addItems(choice.keys)
        self.dropdown.currentTextChanged.connect(self.on_text_changed)
        self.layout.addWidget(self.dropdown)

    def on_text_changed(self, text):
        self.choice.set(text)
        self.callback()

    def connect(self, callback):
        self.callback.register(callback)
